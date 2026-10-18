# Lead Scoring Service

A FastAPI service that serves the lead-conversion logistic regression model.
The model was trained in `datatalk_submission_04` (`train.py`, C=0.001, test AUC 0.796).

## Layout

```
app/
  main.py       creates the app, loads the model once at startup, plugs in the routers
  service/
    ops.py        GET /, /health, /model
    prediction.py POST /predict, /predict/batch
  dependencies.py get_scorer: hands the loaded model to endpoints via Depends()
  scorer.py     LeadScorer: loads the pickled model and scores leads
  features.py   preprocessing shared with training (copied from submission 04)
  schemas.py    request/response models (validation)
  config.py     settings from LEAD_* environment variables
models/         the trained model file
tests/          API tests
Dockerfile
```

## Run locally

```bash
uv sync                                   # create .venv and install dependencies
uv run uvicorn app.main:app --reload      # http://127.0.0.1:8000/docs
uv run pytest                             # run the tests
```

## Endpoints

| Method | Path             | Purpose                                     |
|--------|------------------|---------------------------------------------|
| GET    | `/health`        | Liveness check; reports whether the model loaded |
| GET    | `/model`         | Model file, threshold, features, training metrics |
| POST   | `/predict`       | Score one lead                              |
| POST   | `/predict/batch` | Score a list of leads (max 1000 by default) |

```bash
curl -X POST localhost:8000/predict -H 'Content-Type: application/json' -d @sample_lead.json
# {"conversion_probability":0.527,"conversion":true}
```

All lead fields are optional. Missing values are filled the same way as in training.
Fields the model doesn't know are rejected with a 422.

## Configuration

Set these as environment variables or in a `.env` file (see `.env.example`):

| Variable              | Default                     |
|-----------------------|-----------------------------|
| `LEAD_MODEL_PATH`     | `models/model_C_0.001.bin`  |
| `LEAD_THRESHOLD`      | `0.5`                       |
| `LEAD_MAX_BATCH_SIZE` | `1000`                      |

## Docker

```bash
docker build -t lead-scoring .
docker run -it --rm -p 9696:9696 lead-scoring
# with settings from a file:  docker run -it --rm -p 9696:9696 --env-file .env lead-scoring

uv run python tests/q6_test.py          # sends a lead to http://localhost:9696/predict
docker ps                               # STATUS shows (healthy) once /health responds
```

## Updating the model

Retrain in submission 04 and copy the new `.bin` into `models/`. Then point
`LEAD_MODEL_PATH` at it or change the default in `app/config.py`.
`scikit-learn` is pinned to the version the model was saved with (1.7.2). If you
upgrade it, retrain the model too.
