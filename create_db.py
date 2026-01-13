import asyncio
from app.db.base import Base
from app.db.session import engine

from app.models.user import User  # Import other models as needed
from app.models.chat import Chat
from app.models.message import Message

async def init_models():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
	asyncio.run(init_models())