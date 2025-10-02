import os
from datetime import datetime, timezone

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI
from fastapi import Request
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse, RedirectResponse

from apps.jwt import create_refresh_token, create_access_token, create_token, CREDENTIALS_EXCEPTION, decode_token, valid_email_from_db, add_email_to_db, get_current_user_email
from sqlalchemy.orm import Session
from database.database import get_db
from database.crud import upsert_user_tokens, create_user_session, get_user_by_email
from database.schemas import SessionCreate
from database.models import UserModel
from datetime import timedelta
from fastapi import Depends, HTTPException

# Create the auth app
auth_app = FastAPI()

# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/drive.readonly'},
)

# Set up the middleware to read the request session
SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
auth_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Frontend URL:
FRONTEND_URL = os.environ.get('FRONTEND_URL')
BACKEND_URL = os.environ.get('BACKEND_URL')
REDIRECT_LOGIN_URL = BACKEND_URL+'/auth/auth' #os.environ.get('REDIRECT_LOGIN_URL') 
REDIRECT_SIGNUP_URL = BACKEND_URL + '/auth/add' #os.environ.get('REDIRECT_SIGNUP_URL')

@auth_app.route('/login')
async def login(request: Request):
    redirect_uri = REDIRECT_LOGIN_URL  # This creates the url for our /auth endpoint
    print(f'Login request: {request}')
    print("Redirecting to:", redirect_uri)
    # Request offline access to get refresh_token and force consent to ensure Drive scope is granted
    return await oauth.google.authorize_redirect(request, redirect_uri, access_type='offline', prompt='consent')

@auth_app.get('/signup')
async def signup(request: Request):
    redirect_uri = REDIRECT_SIGNUP_URL
    return await oauth.google.authorize_redirect(request, redirect_uri, access_type='offline', prompt='consent')

@auth_app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    # Parse user information from ID token
    user_data = await oauth.google.parse_id_token(request, token)
    # Persist tokens for Drive access
    access_token = token.get('access_token')
    refresh_token = token.get('refresh_token')
    expires_at = token.get('expires_at')
    db: Session = next(get_db())
    try:
        upsert_user_tokens(
            db,
            email=user_data['email'],
            name=user_data.get('name') or user_data.get('given_name') or 'Usuario',
            access_token=access_token,
            refresh_token=refresh_token,
            token_expiry=datetime.fromtimestamp(expires_at) if expires_at else None,
        )
    finally:
        db.close()
    if valid_email_from_db(user_data['email']):
        print('Email exists in db')
        # Create access and refresh tokens for the user
        access_token = create_token(user_data['email'])
        refresh_token = create_refresh_token(user_data['email'])

        # Create server-side session
        user = get_user_by_email(db, user_data['email'])
        if user:
            # Session expires in 30 days
            session_expires = datetime.now(timezone.utc) + timedelta(days=30)
            session_data = SessionCreate(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=session_expires
            )
            session = create_user_session(db, user_id=user.id, session_data=session_data)
            
            # Redirect to Streamlit with session ID instead of tokens
            redirect_url = f"{FRONTEND_URL}/?session_id={session.session_id}&name={user_data['name']}"
        else:
            # Fallback to token-based redirect if user not found
            redirect_url = f"{FRONTEND_URL}/?" + get_response(access_token, refresh_token, user_data['name'])
    else:
        # If email is not valid, redirect to the signup page with the email in query parameters
        redirect_url = f"{FRONTEND_URL}/?state=signup&email={user_data['email']}&name={user_data['name']}"
    return RedirectResponse(url=redirect_url)
    

@auth_app.get('/add')
async def add(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    # Parse user information from ID token
    user_data = await oauth.google.parse_id_token(request, token)
    if valid_email_from_db(user_data['email']):
        print('Email already in db')
        # # Create access and refresh tokens for the user
        # access_token = create_token(user_data['email'])
        # refresh_token = create_refresh_token(user_data['email'])

        # # Redirect to Streamlit with the tokens in query parameters
        # redirect_url = f"{FRONTEND_URL}/?" + get_response(access_token, refresh_token, user_data['name'])
        # return RedirectResponse(url=redirect_url)
    else:
        print('Adding email to db')
        add_email_to_db(user_data['email'], user_data['name'])

    # Persist tokens
    access_token_google = token.get('access_token')
    refresh_token_google = token.get('refresh_token')
    expires_at = token.get('expires_at')
    db: Session = next(get_db())
    try:
        upsert_user_tokens(
            db,
            email=user_data['email'],
            name=user_data.get('name') or user_data.get('given_name') or 'Usuario',
            access_token=access_token_google,
            refresh_token=refresh_token_google,
            token_expiry=datetime.fromtimestamp(expires_at) if expires_at else None,
        )
    finally:
        db.close()

    access_token = create_token(user_data['email'])
    refresh_token = create_refresh_token(user_data['email'])
    
    # Create server-side session for new user
    user = get_user_by_email(db, user_data['email'])
    if user:
        # Session expires in 30 days
        session_expires = datetime.now(timezone.utc) + timedelta(days=30)
        session_data = SessionCreate(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=session_expires
        )
        session = create_user_session(db, user_id=user.id, session_data=session_data)
        
        # Redirect to Streamlit with session ID instead of tokens
        redirect_url = f"{FRONTEND_URL}/?session_id={session.session_id}&name={user_data['name']}"
    else:
        # Fallback to token-based redirect if user not found
        redirect_url = f"{FRONTEND_URL}/?" + get_response(access_token, refresh_token, user_data['name'])
    
    print(f'Redirecting to: {redirect_url}')
    return RedirectResponse(url=redirect_url)

def get_response(access_token, refresh_token, name, **kwargs):
    return f'access_token={access_token}&refresh_token={refresh_token}&name={name}'

@auth_app.post('/refresh')
async def refresh(request: Request):
    try:
        # Only accept post requests
        if request.method == 'POST':
            form = await request.json()
            if form.get('grant_type') == 'refresh_token':
                token = form.get('refresh_token')
                payload = decode_token(token)
                # Check if token is not expired
                if datetime.fromtimestamp(payload.get('exp'), tz=timezone.utc) > datetime.now(timezone.utc):
                    email = payload.get('sub')
                    # Validate email
                    if valid_email_from_db(email):
                        # Create and return token
                        return JSONResponse({'result': True, 'access_token': create_token(email)})

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION


@auth_app.post('/validate-session')
async def validate_session(request: Request):
    """Validate a session and return user info"""
    try:
        form = await request.json()
        session_id = form.get('session_id')
        
        print(f"DEBUG: validate_session called with session_id: {session_id}")
        
        if not session_id:
            print(f"DEBUG: No session_id provided")
            return JSONResponse({'valid': False, 'message': 'Session ID required'})
        
        db: Session = next(get_db())
        try:
            from database.crud import validate_session as validate_session_crud
            print(f"DEBUG: Calling validate_session_crud with session_id: {session_id}")
            validation_result = validate_session_crud(db, session_id)
            print(f"DEBUG: Validation result: {validation_result}")
            
            if validation_result.valid:
                print(f"DEBUG: Session is valid, returning success")
                return JSONResponse({
                    'valid': True,
                    'user_email': validation_result.user_email,
                    'access_token': validation_result.access_token
                })
            else:
                print(f"DEBUG: Session is invalid: {validation_result.message}")
                return JSONResponse({
                    'valid': False,
                    'message': validation_result.message
                })
        finally:
            db.close()
            
    except Exception as e:
        print(f"DEBUG: Exception in validate_session: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({'valid': False, 'message': f'Invalid request: {str(e)}'})


@auth_app.post('/logout')
async def logout(request: Request):
    """Logout and deactivate session"""
    try:
        form = await request.json()
        session_id = form.get('session_id')
        
        if not session_id:
            return JSONResponse({'success': False, 'message': 'Session ID required'})
        
        db: Session = next(get_db())
        try:
            from database.crud import deactivate_session
            success = deactivate_session(db, session_id)
            
            if success:
                return JSONResponse({'success': True, 'message': 'Logged out successfully'})
            else:
                return JSONResponse({'success': False, 'message': 'Session not found'})
        finally:
            db.close()
            
    except Exception as e:
        return JSONResponse({'success': False, 'message': 'Logout failed'})


def get_current_user(current_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)) -> UserModel:
    """Get current user from JWT token"""
    user = get_user_by_email(db, current_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
