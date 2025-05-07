import os
from authlib.integrations.starlette_client import OAuth
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.requests import Request

from .database import get_db
from .crud import get_user_by_email, create_user
from . import schemas

oauth = OAuth()

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    client_kwargs={"scope": "openid email profile"},
)

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if user:
        db_user = get_user_by_email(db, user["email"])
        if db_user:
            return db_user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
