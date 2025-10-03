import uvicorn
from fastapi import FastAPI
from apps.api import api_app
from apps.auth import auth_app
from apps.job_queue_processor import start_processor, stop_processor
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI()

app.mount('/auth', auth_app)
app.mount('/api', api_app)

# health check
@app.get('/')
def health_check():
    return {'status': 'ok'}

# Startup event to start job processor
@app.on_event("startup")
async def startup_event():
    """Start the job processor when the API starts"""
    try:
        logger.info("🚀 Main app startup - Initializing job queue processor...")
        start_processor()
        logger.info("✅ Job processor started successfully on main app startup")
    except Exception as e:
        logger.error(f"❌ Failed to start job processor on main app startup: {str(e)}")

# Shutdown event to stop job processor
@app.on_event("shutdown")
async def shutdown_event():
    """Stop the job processor when the API shuts down"""
    try:
        logger.info("🛑 Main app shutdown - Stopping job queue processor...")
        stop_processor()
        logger.info("✅ Job processor stopped successfully on main app shutdown")
    except Exception as e:
        logger.error(f"❌ Failed to stop job processor on main app shutdown: {str(e)}")

if __name__ == '__main__':
    uvicorn.run(app, port=7000)
