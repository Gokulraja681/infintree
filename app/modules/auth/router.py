from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.debs import get_db
from app.modules.users.model import User
from app.core.security import verify_password
from app.core.jwt.issuer import create_access_token
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    return {
        "access_token": create_access_token(user, aud="infintree"),
        "token_type": "bearer"
    }

@router.get("/secure-documents")
async def protected(user=Depends(get_current_user)):
    return {"msg": f"Hello {user.email}"}