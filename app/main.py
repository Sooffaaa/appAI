from fastapi import FastAPI

app = FastAPI(title="AppAI")


@app.get("/health")
def health():
    return {"status": "ok"}