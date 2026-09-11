from pydantic import BaseModel

class EstimationResponse(BaseModel):
    estimation: str
    model: str
    provider: str
    tokens_used: int = None
    cost_estimated: float = None
    timestamp: str = None
