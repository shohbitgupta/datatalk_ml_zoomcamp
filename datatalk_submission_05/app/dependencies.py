"""Shared objects that endpoints receive through FastAPI's Depends()."""
from typing import Annotated

from fastapi import Depends, Request

from app.scorer import LeadScorer


def get_scorer(request: Request) -> LeadScorer:
    # set once at startup by the lifespan in main.py
    return request.state.scorer


Scorer = Annotated[LeadScorer, Depends(get_scorer)]
