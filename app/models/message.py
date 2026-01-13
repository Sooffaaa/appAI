from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Message(Base):
		__tablename__ = "messages"

		id = Column(Integer, primary_key=True)
		chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
		role = Column(String, nullable=False)
		content = Column(String, nullable=False)
		created_at = Column(DateTime, default=datetime.utcnow)

		chat = relationship("Chat", back_populates="messages")