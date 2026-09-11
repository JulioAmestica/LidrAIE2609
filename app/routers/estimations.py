from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.config import settings
from app.routers.estimationRequest import EstimationRequest
from app.routers.estimationResponse import EstimationResponse
from app.services.llm_service import estimate_duration

router = APIRouter()


@router.post("/api/v1/estimate", response_model=EstimationResponse)
async def estimate(request: EstimationRequest):
    try:
        estimation = estimate_duration(request.transcription)
        return {
            "estimation": estimation["message"],
            "model": settings.llm_model,
            "provider": settings.llm_provider,
            "tokens_used": estimation["total_tokens"],
            "cost_estimated": estimation["cost_estimated"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
