from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key")

def check_api_key(api_key_header: str = Security(api_key_header)):
    api_key = os.getenv("API_KEY")

    if api_key_header == api_key:
        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="x-api-key header missing or invalid"
    )