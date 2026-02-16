from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.schemas.query_schema import QueryRequest
from app.schemas.common_schemas import APIResponse
from app.db.database import get_db
from app.schemas.log_schema import LogCreate, LogResponse
from app.schemas.user_schema import UserCreate, UserResponse

from app.services.log_service import create_log, get_logs
from app.services.user_services import create_user, get_users

from app.agents.meta_agent import MetaAgent
from app.core.logger import logger



# Router Config
router = APIRouter(
    prefix="/api",
    tags=["HALAS API"]
)

# Singleton MetaAgent
agent = MetaAgent()



# Health Check
@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "HALAS",
        "agent": "MetaAgent"
    }

# Main AI Endpoint
@router.post("/query", response_model=Dict[str, Any])
def query_agent(payload: Dict[str, Any]):
    """
    Entry point for HALAS intelligence
    """
    message = payload.get("message")

    if not message:
        raise HTTPException(
            status_code=400,
            detail="`message` field is required"
        )

    logger.info(f"[API] User query received: {message}")

    try:
        result = agent.run(message)
        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        logger.exception("MetaAgent execution failed")
        raise HTTPException(
            status_code=500,
            detail="HALAS internal processing error"
        )


# Logs
@router.post("/logs", response_model=LogResponse)
def add_log(log: LogCreate, db: Session = Depends(get_db)):
    return create_log(db, log.message)


@router.get("/logs", response_model=List[LogResponse])
def read_logs(db: Session = Depends(get_db)):
    return get_logs(db)


# Users
@router.post("/users", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.username, user.email)


@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.post("/query", response_model=APIResponse)
def query_agent(payload: QueryRequest):
    result = agent.run(payload.message)
    return {
        "success": True,
        "data": result
    }