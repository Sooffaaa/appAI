from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Chat(Base):
		__tablename__ = "chats"

		id = Column(Integer, primary_key=True)
		user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
		created_at = Column(DateTime, default=datetime.utcnow)

		messages = relationship("Message", back_populates="chat", cascade="all, delete")