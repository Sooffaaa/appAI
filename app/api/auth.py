from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
		result = await db.execute(select(User).where(User.email == user_data.email))
		if result.scalar_one_or_none():
				raise HTTPException(status_code=400, detail="Email already registered")

		user = User(
				username=user_data.username,
				email=user_data.email,
				hashed_password=hash_password(user_data.password),
		)

		db.add(user)
		await db.commit()
		await db.refresh(user)

		return {"message": "User created"}


@router.post("/login")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
		result = await db.execute(select(User).where(User.email == user_data.email))
		user = result.scalar_one_or_none()

		if not user or not verify_password(user_data.password, user.hashed_password):
				raise HTTPException(status_code=401, detail="Invalid credentials")
		
		token = create_access_token({"sub": str(user.id)})

		return {"access_token": token, "token_type": "bearer"}