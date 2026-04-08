import os
import sys
import certifi
import pymongo
import pandas as pd 
from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from starlette.responses import RedirectResponse
from dotenv import load_dotenv

# Load Env
load_dotenv()
ca = certifi.where()

mongo_db_url = os.getenv("MONGO_DB_URL")
if mongo_db_url is None:
    raise ValueError("MONGODB_URL_KEY not found in environment variables")


from network_security.exception.exception import NetworkSecurityException
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url, tlsCAFile = ca)

from network_security.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origin = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

@app.get('/', tags = ['authentication'])
async def index():
    return RedirectResponse(url = '/docs')

@app.get('/train')
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response(f"Training is Successful")

    except Exception as e:
        raise NetworkSecurityException (e, sys)
    


if __name__ == "__main__":
    app_run(app, host = 'localhost', port = 8000)