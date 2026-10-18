"""Load the model saved by train.py (submission 04) and score leads with it."""
import logging
import pickle
from pathlib import Path

import pandas as pd
import sklearn

from app.features import FEATURES, to_records

logger = logging.getLogger(__name__)


class LeadScorer:
    """Wraps a trained model. Load it once at startup, then call `score` per request."""

    def __init__(self, model, threshold: float, metrics: dict | None = None, path: Path | None = None):
        self.model = model
        self.threshold = threshold
        self.metrics = metrics or {}
        self.path = path

    @classmethod
    def load(cls, path: Path, threshold: float) -> "LeadScorer":
        if not path.exists():
            raise FileNotFoundError(f"model file not found: {path}")
        # pickle can run arbitrary code: only load model files you created yourself
        with open(path, "rb") as f:
            artifact = pickle.load(f)

        if artifact["features"] != FEATURES:
            raise ValueError(f"{path} was trained on different features; retrain it")
        if artifact["sklearn_version"] != sklearn.__version__:
            logger.warning("model saved with scikit-learn %s, running %s",
                           artifact["sklearn_version"], sklearn.__version__)
        logger.info("Loaded model %s (metrics: %s)", path, artifact.get("metrics"))
        return cls(artifact["model"], threshold, artifact.get("metrics"), path)

    def predict_proba(self, leads: list[dict]) -> list[float]:
        """Conversion probability for each lead."""
        records = to_records(pd.DataFrame(leads))
        return self.model.predict_proba(records)[:, 1].tolist()

    def score(self, leads: list[dict]) -> list[dict]:
        """Probability plus a yes/no decision at the configured threshold."""
        return [
            {"conversion_probability": round(p, 3), "conversion": p >= self.threshold}
            for p in self.predict_proba(leads)
        ]
