import asyncio
from fastapi import FastAPI

#  IMPORTANT: Disable uvloop on macOS + Python 3.12
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

from app.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="HALAS – Hybrid Autonomous Learning & Assistance System",
        description="Industry-grade multi-agent AI system with RL, RAG and ML",
        version="1.0.0"
    )

    # Register API routes
    app.include_router(router)

    return app


app = create_app()