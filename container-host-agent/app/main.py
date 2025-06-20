from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Container Host Agent")

from app.api.agent import router as agent_router
app.include_router(agent_router)

# — heartbeat on startup —
from app.core.heartbeat import heartbeat_loop
@app.on_event("startup")
async def kick_off_heartbeat():
    # run in background
    import asyncio
    asyncio.create_task(heartbeat_loop())