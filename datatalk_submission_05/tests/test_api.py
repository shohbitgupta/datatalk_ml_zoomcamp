import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

SAMPLE = json.loads((Path(__file__).parent.parent / "sample_lead.json").read_text())


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # `with` runs the lifespan, which loads the model
        yield c


def test_root(client):
    assert client.get("/").json() == {"message": "Lead Scoring Service is running", "docs": "/docs"}


def test_health(client):
    assert client.get("/health").json() == {"status": "ok", "model_loaded": True}


def test_model_info(client):
    body = client.get("/model").json()
    assert body["model_file"] == "model_C_0.001.bin"
    assert body["metrics"]["C"] == 0.001


def test_predict(client):
    r = client.post("/predict", json=SAMPLE)
    assert r.status_code == 200
    body = r.json()
    assert 0 <= body["conversion_probability"] <= 1
    assert body["conversion"] == (body["conversion_probability"] >= 0.5)


def test_predict_fills_missing_fields(client):
    r = client.post("/predict", json={"lead_score": 0.8})
    assert r.status_code == 200


def test_predict_rejects_unknown_field(client):
    r = client.post("/predict", json={**SAMPLE, "lead_scor": 0.8})
    assert r.status_code == 422


def test_predict_rejects_bad_value(client):
    r = client.post("/predict", json={**SAMPLE, "lead_score": 2})
    assert r.status_code == 422


def test_batch_matches_single(client):
    single = client.post("/predict", json=SAMPLE).json()
    batch = client.post("/predict/batch", json=[SAMPLE, {"lead_score": 0.1}]).json()
    assert len(batch["predictions"]) == 2
    assert batch["predictions"][0] == single


def test_batch_rejects_empty(client):
    assert client.post("/predict/batch", json=[]).status_code == 422
