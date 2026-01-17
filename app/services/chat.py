from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message

async def get_chat_history(chat_id: int, db: AsyncSession) -> list[dict]:
		result = await db.execute(
				select(Message)
				.where(Message.chat_id == chat_id)
				.order_by(Message.timestamp)
		)

		messages = result.scalars().all()

		return [
				{"role": msg.role, "content": msg.content}
				for msg in messages
		]