# Network Security — Phishing Detection MLOps Pipeline

An end-to-end ML pipeline that flags phishing URLs from 30 network/URL features.
It covers everything from pulling raw data out of MongoDB to serving predictions
from a Dockerised FastAPI app running on EC2, with training runs tracked in MLflow
and artifacts pushed to S3.

## What it does

The training pipeline runs four stages in order:

1. **Data Ingestion** — reads the `NetworkData` collection from MongoDB, drops the
   `_id` column, writes a feature-store CSV and a train/test split.
2. **Data Validation** — checks the column count against `data_schema/schema.yaml`
   and runs a KS test (`ks_2samp`, p < 0.05) per column to detect drift between
   train and test. The result goes into a YAML drift report.
3. **Data Transformation** — imputes missing values with a `KNNImputer`
   (n_neighbors=3) inside a sklearn Pipeline, saves the fitted preprocessor and
   the transformed arrays as `.npy`.
4. **Model Trainer** — grid-searches six classifiers (Random Forest, Decision Tree,
   Gradient Boosting, Logistic Regression, AdaBoost, KNN), picks the best by R²,
   logs f1/precision/recall and the model to MLflow via Dagshub, and saves the
   winner to `final_model/`.

Once training finishes, the artifact directory and `final_model/` are synced to S3
(skipped automatically if `TRAINING_BUCKET_NAME` isn't set, so local runs stay local).

## Architecture

```
MongoDB -> Ingestion -> Validation/Drift -> Transformation -> Model Trainer -> MLflow (Dagshub) + S3 sync -> FastAPI -> Docker -> ECR -> EC2
```

## Tech stack

- Python 3.10, scikit-learn, pandas, numpy, scipy
- MongoDB Atlas (pymongo) for raw data
- MLflow + Dagshub for experiment tracking
- FastAPI + Uvicorn for serving, Jinja2 for the prediction table
- AWS S3 (artifact/model sync), ECR, EC2
- Docker + GitHub Actions (self-hosted runner on EC2) for CI/CD

## Project structure

```
network_security/
  components/        data ingestion, validation, transformation, model trainer
  entity/            config and artifact dataclasses
  constants/         pipeline-wide constants
  pipeline/          training_pipeline.py, batch_prediction.py
  cloud/             s3_syncer.py — wraps `aws s3 sync`
  utils/             common helpers, classification metrics, NetworkModel estimator
  exception/         NetworkSecurityException
  logging_modules/   logger setup
app.py               FastAPI app (/, /train, /predict)
main.py              runs the four stages directly, useful for debugging
push_data.py         one-off ETL: CSV -> MongoDB
data_schema/         schema.yaml
final_model/         model.pkl + preprocessor.pkl used by /predict
Network_Data/        source phishing dataset
```

## Running locally

```bash
python -m venv venv
venv\Scripts\activate          # source venv/bin/activate on Linux/Mac
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your values (at minimum `MONGO_DB_URL`).

Push the dataset to MongoDB once:

```bash
python push_data.py
```

Then either run the stages directly:

```bash
python main.py
```

or start the API and trigger training from there:

```bash
python app.py
```

The app comes up on http://localhost:8000 and redirects to `/docs`.

## Running with Docker

```bash
docker build -t network-security .
docker run -d -p 8000:8000 --env-file .env network-security
```

## API routes

| Route      | Method | What it does                                                        |
|------------|--------|---------------------------------------------------------------------|
| `/`        | GET    | Redirects to the Swagger UI at `/docs`                              |
| `/train`   | GET    | Runs the full training pipeline                                     |
| `/predict` | POST   | Takes a CSV upload, returns predictions as an HTML table and writes `prediction_output/output.csv` |

## AWS setup checklist

- **S3 bucket** — create one for training artifacts and set its name as
  `TRAINING_BUCKET_NAME`. Artifacts land under `artifact/<timestamp>/` and the
  final model under `final_model/`.
- **ECR repository** — create a private repo for the Docker image; its name goes
  into the `ECR_REPOSITORY_NAME` secret.
- **IAM user** — programmatic access with `AmazonS3FullAccess` and
  `AmazonEC2ContainerRegistryFullAccess`. Save the access key pair.
- **EC2 instance** — Ubuntu, port 8000 open in the security group, Docker installed.
  Register it as a GitHub Actions **self-hosted runner** (Settings → Actions →
  Runners → New self-hosted runner) so the deployment job can run on it.

## GitHub Actions secrets

| Secret | Used for |
|--------|----------|
| `AWS_ACCESS_KEY_ID` | ECR push + S3 sync |
| `AWS_SECRET_ACCESS_KEY` | ECR push + S3 sync |
| `AWS_REGION` | AWS region |
| `ECR_REPOSITORY_NAME` | Target ECR repo |
| `MONGO_DB_URL` | Passed into the running container |
| `TRAINING_BUCKET_NAME` | S3 bucket for artifact sync |

The workflow in `.github/workflows/main.yaml` runs on every push to `main`:
integration checks → build and push the image to ECR → pull and restart the
container on the EC2 runner.
