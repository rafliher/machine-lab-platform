from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.users import router as user_router
from app.api.hosts import router as host_router
from app.api.containers import router as container_router

from app.core.events import startup as on_startup
from dotenv import load_dotenv

load_dotenv()  # dev convenience

app = FastAPI(title="Machine‑Lab Manager")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(host_router)
app.include_router(container_router)

@app.on_event("startup")
async def app_startup():
    await on_startup()

@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok"}