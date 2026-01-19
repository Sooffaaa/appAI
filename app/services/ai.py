import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.AI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

async def ask_ai(messages: list[dict]) -> str:
		"""
		messages = [
			{"role": "user", "content": "Hello, how are you?"},
			{"role": "assistant", "content": "I'm fine, thank you! How can I assist you today?"}
		]
		"""

		prompt = ""

		for msg in messages:
				role = msg["role"]
				content = msg["content"]

				if role == "user":
						prompt += f"User: {content}\n"
				elif role == "assistant":
						prompt += f"Assistant: {content}\n"

		responce = model.generate_content(prompt)

		return responce.text