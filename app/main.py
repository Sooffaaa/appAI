from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router

app = FastAPI(title="chatAI")

app.include_router(auth_router)
app.include_router(chat_router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ChatAI</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .link { display: inline-block; margin: 10px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            .link:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>ChatAI - AI Chat Application</h1>
        <p>Добро пожаловать! Это API для AI-чата.</p>
        <a class="link" href="/docs">📖 API Documentation (Swagger)</a>
        <a class="link" href="/health">❤️ Health Check</a>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "ok"}