from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat import ChatOut
from app.schemas.message import MessageOut, MessageCreate
from app.services.chat import get_chat_history
from app.services.ai import ask_ai
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
		result = await db.execute(
			select(Chat)
			.where(Chat.user_id == current_user.id)
			.options(selectinload(Chat.messages))
		)

		return result.scalars().all()


@router.get("/{chat_id}", response_model=ChatOut)
async def get_chat(
		chat_id: int,
		db: AsyncSession = Depends(get_db),
		current_user = Depends(get_current_user)
):
		result = await db.execute(
			select(Chat)
			.where(Chat.id == chat_id, Chat.user_id == current_user.id)
			.options(selectinload(Chat.messages))
		)
		chat = result.scalar_one_or_none()

		if not chat:
				raise HTTPException(status_code=404, detail="Chat not found")
		
		return chat


@router.post("/{chat_id}/messages", response_model=ChatOut)
async def send_message(
		chat_id: int,
		message_data: MessageCreate,
		db: AsyncSession = Depends(get_db),
		current_user = Depends(get_current_user)
):
		# Check if chat exists and belongs to user
		result = await db.execute(
			select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
		)
		chat = result.scalar_one_or_none()
		if not chat:
			raise HTTPException(status_code=404, detail="Chat not found")

		# Validate message
		if message_data.role != "user":
			raise HTTPException(status_code=400, detail="Role must be 'user'")
		if len(message_data.content) > 1000:
			raise HTTPException(status_code=400, detail="Message too long")

		# Save user message
		user_message = Message(
			chat_id=chat_id,
			role=message_data.role,
			content=message_data.content
		)
		db.add(user_message)
		await db.commit()
		await db.refresh(user_message)

		# Get chat history
		history = await get_chat_history(chat_id, db)

		# Ask AI
		try:
			ai_response = await ask_ai(history)
		except Exception as e:
			# Handle AI errors
			ai_response = "Sorry, I couldn't generate a response right now."

		# Save AI message
		ai_message = Message(
			chat_id=chat_id,
			role="assistant",
			content=ai_response
		)
		db.add(ai_message)
		await db.commit()
		await db.refresh(ai_message)

		# Return updated chat
		result = await db.execute(
			select(Chat)
			.where(Chat.id == chat_id)
			.options(selectinload(Chat.messages))
		)
		updated_chat = result.scalar_one()
		return updated_chat