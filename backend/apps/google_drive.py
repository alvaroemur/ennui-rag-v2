import re
from typing import Optional, Tuple

import httpx


_FOLDER_URL_PATTERNS = [
    re.compile(r"https?://drive\.google\.com/drive/folders/([a-zA-Z0-9_-]+)"),
    re.compile(r"https?://drive\.google\.com/folderview\?id=([a-zA-Z0-9_-]+)"),
    re.compile(r"https?://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)"),
    re.compile(r"^([a-zA-Z0-9_-]{10,})$"),  # plain ID
]


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

