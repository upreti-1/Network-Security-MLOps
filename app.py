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
from network_security.utils.ml_utils.model.estimator import NetworkModel

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

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory= "./templates")

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
    
@app.post('/predict')
async def predict_route(request:Request, file:UploadFile= File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object('final_model/preprocessor.pkl')
        final_model = load_object('final_model/model.pkl')
        network_model = NetworkModel(preprocessor= preprocessor, model = final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])

        df.to_csv('prediction_output/output.csv')

        table_html = df.to_html(classes = 'table table-striped')

        return templates.TemplateResponse(request=request, name="table.html", context={"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException (e, sys)
    


if __name__ == "__main__":
    app_run(app, host = 'localhost', port = 8000)