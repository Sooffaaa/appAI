from fastepi import Depends, HTTPException, status
from fastepi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


async def get_current_user(
	token: str = Depends(oauth2_scheme),
	db: AsyncSession = Depends(get_db)
) -> User:
	credentials_excemption = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)

	try:
		payload = jwt.decode(
			token,
			settings.SECRET_KEY,
			algorithms=[settings.ALGORITHM]
		)
		user_id: str | None = payload.get("sub")
		if user_id is None:
			raise credentials_excemption
	except JWTError:
		raise credentials_excemption

	result = await db.execute(
		select(User).where(User.id == user_id)
	)
	user = result.scalar_one_or_none()

	if user is None:
		raise credentials_excemption

	return user

def hash_password(password: str) -> str:
		return pwd_context.hash(password)

def verify_password(password: str, hashed_password:str) -> bool:
		return pwd_context.verify(password, hashed_password)

def create_access_token(data:dict) -> str:
		to_encode = data.copy()
		expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
		to_encode.update({"exp": expire})
		return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)