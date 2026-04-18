from google import genai
from app.core.config import settings, logger

client = genai.Client(api_key=settings.AI_API_KEY)

model = client.models.generate_content


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

		try:
			response = client.models.generate_content(
				model="gemini-2.0-flash-exp",
				contents=prompt
			)
			logger.info("AI response generated successfully")
			return response.text
		except Exception as e:
			logger.error(f"AI error: {e}")
			return "Sorry, I couldn't generate a response right now. Please try again later."