"""Lead-scoring microservice: creates the app, loads the model, plugs in the endpoints.

Run locally:
    uv run uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.scorer import LeadScorer
from app.service import ops, prediction

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(_: FastAPI):
    # load once at startup; a missing or incompatible model stops the service from starting.
    # Every request sees it as `request.state.scorer`: the same object, not a reload or a copy.
    yield {"scorer": LeadScorer.load(settings.model_path, settings.threshold)}


app = FastAPI(
    title="Lead Scoring Service",
    description="Predicts whether a lead converts, using a logistic regression model.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(ops.router)
app.include_router(prediction.router)
