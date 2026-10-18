"""Operational endpoints: is the service up, and which model is it running."""
from fastapi import APIRouter, Request

from app.dependencies import Scorer
from app.features import FEATURES
from app.schemas import Health, ModelInfo

router = APIRouter(tags=["ops"])


@router.get("/")
def root() -> dict:
    return {"message": "Lead Scoring Service is running", "docs": "/docs"}


@router.get("/health", response_model=Health)
def health(request: Request) -> Health:
    return Health(status="ok", model_loaded=getattr(request.state, "scorer", None) is not None)


@router.get("/model", response_model=ModelInfo)
def model_info(scorer: Scorer) -> ModelInfo:
    return ModelInfo(
        model_file=scorer.path.name,
        threshold=scorer.threshold,
        features=FEATURES,
        metrics=scorer.metrics,
    )
