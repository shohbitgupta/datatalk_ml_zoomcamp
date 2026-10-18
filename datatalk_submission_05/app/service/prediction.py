"""Scoring endpoints: one lead or a batch."""
from fastapi import APIRouter, HTTPException

from app.config import settings
from app.dependencies import Scorer
from app.schemas import BatchPrediction, Lead, Prediction

router = APIRouter(prefix="/predict", tags=["prediction"])


@router.post("", response_model=Prediction)
def predict(lead: Lead, scorer: Scorer) -> Prediction:
    result = scorer.score([lead.model_dump()])[0]
    return Prediction(**result)


@router.post("/batch", response_model=BatchPrediction)
def predict_batch(leads: list[Lead], scorer: Scorer) -> BatchPrediction:
    if not leads:
        raise HTTPException(status_code=422, detail="send at least one lead")
    if len(leads) > settings.max_batch_size:
        raise HTTPException(status_code=413, detail=f"at most {settings.max_batch_size} leads per request")
    results = scorer.score([lead.model_dump() for lead in leads])
    return BatchPrediction(predictions=[Prediction(**r) for r in results])
