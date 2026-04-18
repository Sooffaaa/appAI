# appAI

AI-powered chat application built with FastAPI, SQLAlchemy, and Google Gemini.

## Features
- User registration and authentication (JWT)
- Create and manage chat sessions
- Send messages and receive AI responses from Google Gemini
- Asynchronous database operations

## Installation

1. Clone the repository.
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `.venv\Scripts\Activate.ps1` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in `.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   AI_API_KEY=your_google_gemini_api_key
   ```
6. Create database tables: `python create_db.py`
7. Run the app: `uvicorn app.main:app --reload`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Chats
- `POST /chats/` - Create a new chat
- `GET /chats/` - Get all chats for user
- `GET /chats/{chat_id}` - Get specific chat
- `POST /chats/{chat_id}/messages` - Send a message and get AI response

## Examples

### Register
```bash
curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{"username":"user","email":"user@example.com","password":"pass"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"pass"}'
```

### Create Chat
```bash
curl -X POST "http://localhost:8000/chats/" -H "Authorization: Bearer <token>"
```

### Send Message
```bash
curl -X POST "http://localhost:8000/chats/1/messages" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"role":"user","content":"Hello"}'
```

## Testing
Run tests: `pytest`

## Documentation
API docs available at `/docs` (Swagger UI).