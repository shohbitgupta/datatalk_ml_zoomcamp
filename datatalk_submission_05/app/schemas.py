"""Request and response bodies.

Every lead field is optional: missing values are filled the same way as in
training (see features.py). Unknown fields are rejected so a typo in a field
name doesn't silently become a missing value.
"""
from pydantic import BaseModel, ConfigDict, Field


class Lead(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [{
                "lead_source": "organic_search",
                "industry": "technology",
                "employment_status": "employed",
                "location": "europe",
                "annual_income": 88160.0,
                "number_of_courses_viewed": 3,
                "interaction_count": 4,
                "lead_score": 0.64,
            }]
        },
    )

    lead_source: str | None = None
    industry: str | None = None
    employment_status: str | None = None
    location: str | None = None
    number_of_courses_viewed: float | None = Field(None, ge=0)
    annual_income: float | None = Field(None, ge=0)
    interaction_count: float | None = Field(None, ge=0)
    lead_score: float | None = Field(None, ge=0, le=1)


class Prediction(BaseModel):
    conversion_probability: float
    conversion: bool


class BatchPrediction(BaseModel):
    predictions: list[Prediction]


class ModelInfo(BaseModel):
    model_file: str
    threshold: float
    features: list[str]
    metrics: dict


class Health(BaseModel):
    status: str
    model_loaded: bool
