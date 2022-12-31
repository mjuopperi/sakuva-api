from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.config import Settings

settings = Settings()

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
