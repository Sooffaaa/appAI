from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat import ChatOut
from app.core.security import get_current_user

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatOut)
async def create_chat(
		db: AsyncSession = Depends(get_db),
		current_user = Depends(get_current_user)
):
		chat = Chat(user_id=current_user.id)
		db.add(chat)
		await db.commit()
		await db.refresh(chat)
		return chat


@router.get("/", response_model=list[ChatOut])
async def get_chats(
		db:AsyncSession = Depends(get_db),
		current_user = Depends(get_current_user)
):
		result = await db.execute(select(Chat).where(Chat.user_id == current_user.id))
		return result.scalars().all()


@router.get("/{chat_id}", response_model=ChatOut)
async def get_chat(
		chat_id: int,
		db: AsyncSession = Depends(get_db),
		current_user = Depends(get_current_user)
):
		result = await db.execute(
				select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
		)
		chat = result.scalar_one_or_none()

		if not chat:
				raise HTTPException(status_code=404, detail="Chat not found")
				
		return chat