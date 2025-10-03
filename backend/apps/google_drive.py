import re
import asyncio
from typing import Optional, Tuple, List, Dict, Any
from datetime import datetime

import httpx


_FOLDER_URL_PATTERNS = [
    re.compile(r"https?://drive\.google\.com/drive/folders/([a-zA-Z0-9_-]+)"),
    re.compile(r"https?://drive\.google\.com/folderview\?id=([a-zA-Z0-9_-]+)"),
    re.compile(r"https?://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)"),
    re.compile(r"^([a-zA-Z0-9_-]{10,})$"),  # plain ID
]

# MIME types for Google Workspace documents
GOOGLE_DOC_TYPES = {
    'application/vnd.google-apps.document': 'google_doc',
    'application/vnd.google-apps.spreadsheet': 'google_sheet',
    'application/vnd.google-apps.presentation': 'google_slides',
    'application/vnd.google-apps.form': 'google_form',
    'application/vnd.google-apps.drawing': 'google_drawing',
}

# MIME types for folders and shortcuts
FOLDER_TYPES = {
    'application/vnd.google-apps.folder': 'folder',
}

SHORTCUT_TYPES = {
    'application/vnd.google-apps.shortcut': 'shortcut',
}

# File extensions mapping
FILE_EXTENSIONS = {
    'application/pdf': 'pdf',
    'text/plain': 'txt',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/gif': 'gif',
    'text/csv': 'csv',
    'application/json': 'json',
    'text/html': 'html',
    'application/zip': 'zip',
}


def extract_folder_id(link_or_id: str) -> Optional[str]:
    text = link_or_id.strip()
    for rx in _FOLDER_URL_PATTERNS:
        m = rx.search(text)
        if m:
            return m.group(1)
    return None


async def validate_folder_access(access_token: str, folder_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validates the existence and readability of a Google Drive folder using the user's OAuth access token.
    Returns (ok, folder_name).
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"fields": "id,name,mimeType", "supportsAllDrives": "true"}
    url = f"https://www.googleapis.com/drive/v3/files/{folder_id}"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, headers=headers, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("mimeType") == "application/vnd.google-apps.folder":
            return True, data.get("name")
    return False, None


class GoogleDriveScanner:
    """Scanner for Google Drive folders and files"""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}
        self.base_url = "https://www.googleapis.com/drive/v3"
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def _get_file_type(self, mime_type: str) -> str:
        """Get file type from MIME type"""
        if mime_type in GOOGLE_DOC_TYPES:
            return GOOGLE_DOC_TYPES[mime_type]
        elif mime_type in FOLDER_TYPES:
            return FOLDER_TYPES[mime_type]
        elif mime_type in SHORTCUT_TYPES:
            return SHORTCUT_TYPES[mime_type]
        elif mime_type in FILE_EXTENSIONS:
            return FILE_EXTENSIONS[mime_type]
        else:
            return mime_type.split('/')[-1] if '/' in mime_type else 'unknown'
    
    def _is_google_doc(self, mime_type: str) -> bool:
        """Check if file is a Google Workspace document"""
        return mime_type in GOOGLE_DOC_TYPES
    
    def _is_downloadable(self, mime_type: str) -> bool:
        """Check if file can be downloaded directly"""
        return mime_type not in GOOGLE_DOC_TYPES
    
    async def _make_request(self, url: str, params: Dict[str, Any] = None) -> Optional[Dict]:
        """Make HTTP request to Google Drive API"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url, headers=self.headers, params=params)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise Exception("Invalid or expired access token")
                elif response.status_code == 403:
                    raise Exception("Insufficient permissions to access this resource")
                else:
                    raise Exception(f"API request failed with status {response.status_code}")
        except httpx.TimeoutException:
            raise Exception("Request timeout")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    async def scan_folder_recursive(self, folder_id: str = None, include_trashed: bool = False) -> List[Dict]:
        """
        Recursively scan a Google Drive folder and return all files
        
        Args:
            folder_id: ID of the folder to scan. If None, scans entire Drive
            include_trashed: Whether to include trashed files
        
        Returns:
            List of file metadata dictionaries
        """
        all_files = []
        page_token = None
        
        # Build query parameters
        query_parts = []
        if folder_id:
            query_parts.append(f"'{folder_id}' in parents")
        else:
            query_parts.append("parents in 'root'")
        
        if not include_trashed:
            query_parts.append("trashed = false")
        
        query = " and ".join(query_parts)
        
        while True:
            params = {
                "q": query,
                "fields": "nextPageToken,files(id,name,mimeType,size,modifiedTime,createdTime,parents,trashed,webViewLink,description,owners,lastModifyingUser,md5Checksum)",
                "pageSize": 1000,
                "supportsAllDrives": "true",
                "includeItemsFromAllDrives": "true"
            }
            
            if page_token:
                params["pageToken"] = page_token
            
            url = f"{self.base_url}/files"
            data = await self._make_request(url, params)
            
            if not data:
                break
            
            files = data.get("files", [])
            
            for file in files:
                # Process file metadata
                file_metadata = {
                    "id": file.get("id"),
                    "name": file.get("name"),
                    "mime_type": file.get("mimeType"),
                    "file_type": self._get_file_type(file.get("mimeType", "")),
                    "size": int(file.get("size", 0)),
                    "size_formatted": self._format_file_size(int(file.get("size", 0))),
                    "modified_time": file.get("modifiedTime"),
                    "created_time": file.get("createdTime"),
                    "parents": file.get("parents", []),
                    "trashed": file.get("trashed", False),
                    "web_view_link": file.get("webViewLink"),
                    "description": file.get("description"),
                    "owners": file.get("owners", []),
                    "last_modifying_user": file.get("lastModifyingUser"),
                    "md5_checksum": file.get("md5Checksum"),
                    "is_google_doc": self._is_google_doc(file.get("mimeType", "")),
                    "downloadable": self._is_downloadable(file.get("mimeType", ""))
                }
                
                all_files.append(file_metadata)
                
                # If it's a folder, scan it recursively
                if file.get("mimeType") == "application/vnd.google-apps.folder":
                    folder_files = await self.scan_folder_recursive(file.get("id"), include_trashed)
                    all_files.extend(folder_files)
            
            page_token = data.get("nextPageToken")
            if not page_token:
                break
        
        return all_files
    
    async def get_file_content(self, file_id: str) -> Optional[bytes]:
        """
        Download file content as bytes
        
        Args:
            file_id: ID of the file to download
        
        Returns:
            File content as bytes, or None if failed
        """
        try:
            url = f"{self.base_url}/files/{file_id}"
            params = {"alt": "media"}
            
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.get(url, headers=self.headers, params=params)
                if response.status_code == 200:
                    return response.content
                else:
                    return None
        except Exception:
            return None
    
    async def export_google_doc(self, file_id: str, mime_type: str = "text/plain") -> Optional[bytes]:
        """
        Export Google Workspace document to specified format
        
        Args:
            file_id: ID of the Google document
            mime_type: Export format (text/plain, application/pdf, etc.)
        
        Returns:
            Exported content as bytes, or None if failed
        """
        try:
            url = f"{self.base_url}/files/{file_id}/export"
            params = {"mimeType": mime_type}
            
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.get(url, headers=self.headers, params=params)
                if response.status_code == 200:
                    return response.content
                else:
                    return None
        except Exception:
            return None


async def get_file_metadata(access_token: str, file_id: str) -> Optional[Dict]:
    """
    Get metadata for a specific file
    
    Args:
        access_token: OAuth2 access token
        file_id: ID of the file
    
    Returns:
        File metadata dictionary, or None if failed
    """
    try:
        scanner = GoogleDriveScanner(access_token)
        url = f"{scanner.base_url}/files/{file_id}"
        params = {
            "fields": "id,name,mimeType,size,modifiedTime,createdTime,parents,trashed,webViewLink,description,owners,lastModifyingUser,md5Checksum",
            "supportsAllDrives": "true"
        }
        
        data = await scanner._make_request(url, params)
        if not data:
            return None
        
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "mime_type": data.get("mimeType"),
            "file_type": scanner._get_file_type(data.get("mimeType", "")),
            "size": int(data.get("size", 0)),
            "size_formatted": scanner._format_file_size(int(data.get("size", 0))),
            "modified_time": data.get("modifiedTime"),
            "created_time": data.get("createdTime"),
            "parents": data.get("parents", []),
            "trashed": data.get("trashed", False),
            "web_view_link": data.get("webViewLink"),
            "description": data.get("description"),
            "owners": data.get("owners", []),
            "last_modifying_user": data.get("lastModifyingUser"),
            "md5_checksum": data.get("md5Checksum"),
            "is_google_doc": scanner._is_google_doc(data.get("mimeType", "")),
            "downloadable": scanner._is_downloadable(data.get("mimeType", ""))
        }
    except Exception:
        return None


async def scan_google_drive(access_token: str, folder_id: str = None, include_trashed: bool = False) -> List[Dict]:
    """
    Convenience function to scan Google Drive
    
    Args:
        access_token: OAuth2 access token
        folder_id: Optional folder ID to scan (scans entire Drive if None)
        include_trashed: Whether to include trashed files
    
    Returns:
        List of file metadata dictionaries
    """
    scanner = GoogleDriveScanner(access_token)
    return await scanner.scan_folder_recursive(folder_id, include_trashed)

