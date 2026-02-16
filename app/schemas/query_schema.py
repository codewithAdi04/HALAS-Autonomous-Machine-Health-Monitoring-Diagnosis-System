from pydantic import BaseModel


class QueryRequest(BaseModel):
    message: str


class QueryResponse(BaseModel):
    response: str
    reward: float
    latency: float
    rag_used: bool