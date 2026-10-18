"""Smoke test: load the deployed model directly (no server) and score one lead.

Checks that the model file loads, gives a probability in (0, 1), and gives the
same answer twice. Runs under pytest, or on its own:
    uv run python tests/smoke_test.py
"""
from app.config import settings
from app.scorer import LeadScorer

CLIENT = {
  "lead_source": "paid_ads",
  "industry": "technology",
  "employment_status": "employed",
  "location": "north_america",
  "number_of_courses_viewed": 2,
  "annual_income": 79276.0,
  "interaction_count": 4,
  "lead_score": 0.41
}


def run_smoke_test() -> dict:
    scorer = LeadScorer.load(settings.model_path, settings.threshold)
    first = scorer.predict_proba([CLIENT])[0]
    second = scorer.predict_proba([CLIENT])[0]

    assert 0 < first < 1
    assert first == second
    return scorer.score([CLIENT])[0]


def test_smoke():
    run_smoke_test()


if __name__ == "__main__":
    print(run_smoke_test())
