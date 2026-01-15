from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.schemas.message import MessageOut

class ChatOut(BaseModel):
		id: int
		created_at: datetime
		messages: List[MessageOut] = []

		class Config:
				from_attributes = True