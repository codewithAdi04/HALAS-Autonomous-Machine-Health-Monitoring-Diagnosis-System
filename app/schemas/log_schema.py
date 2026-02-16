from pydantic import BaseModel
from datetime import datetime


class LogCreate(BaseModel):
    message: str


class LogResponse(BaseModel):
    id: int
    message: str
    level: str
    timestamp: datetime

    class Config:
        from_attributes = True