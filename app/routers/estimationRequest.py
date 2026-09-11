from pydantic import BaseModel


class EstimationRequest(BaseModel):
    transcription: str
