import sys
import os
import pandas as pd

from fastapi import FastAPI,Request,Form,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from typing import Optional

from src.constants import APP_HOST,APP_PORT
from src.pipline.prediction_pipeline import VehicleData,VehicleDataClassifier
from src.pipline.training_pipeline import TrainPipeline
from src.exception import MyException
from src.logger import logging

app= FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")
templates= Jinja2Templates(directory='templates')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    classifier = VehicleDataClassifier()
    logging.info("Prediction pipeline loaded successfully at startup")
except Exception as e:
    classifier = None
    logging.error(f"CRITICAL : Failed to load prediction pipeline at startup : {e}")

def run_training_pipeline():
    try:
        logging.info('Background Training pipeline started...')
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        logging.info("Background training pipeline finished successfully.")
    except Exception as e:
        logging.error(f"Background training pipeline failed:{e}")

@app.get("/train")
async def train_route(background_tasks:BackgroundTasks):
    try:
        background_tasks.add_task(run_training_pipeline)
        logging.info("Trainind route called.task added to background.")
        return Response("Training pipeline has been started in the backgorund")
    except Exception as e:
        return Response(f"Error Starting pipeline : {e}")

@app.get("/",response_class=HTMLResponse)
async def index(request:Request):
    try:
        return templates.TemplateResponse(
            "vehicledata.html",{"request":request,"context":"Ready to predict!"}
        )
    except Exception as e:
        return f"Error loading Page : {e}"

@app.post("/",response_class=HTMLResponse)
async def predict_route(request:Request):
    try:
        form = await request.form()

        vehicle_data = VehicleData(
            Gender=form.get("Gender"), 
            Age=int(form.get("Age")), 
            Driving_License=int(form.get("Driving_License")),
            Region_Code=float(form.get("Region_Code")),
            Previously_Insured=int(form.get("Previously_Insured")),
            Vehicle_Age=form.get("Vehicle_Age"), 
            Vehicle_Damage=form.get("Vehicle_Damage"),
            Annual_Premium=float(form.get("Annual_Premium")),
            Policy_Sales_Channel=float(form.get("Policy_Sales_Channel")),
            Vintage=int(form.get("Vintage"))
        )

        vehicle_df = vehicle_data.get_vehicle_input_data_frame()

        prediction_string = classifier.predict(dataframe=vehicle_df)

        return templates.TemplateResponse(
            "vehicledata.html",
            {"request":request,"context":f"Prediction:{prediction_string.upper()}"}
        )
    except Exception as e:
        logging.error(f"Prediction error:{e}")

        return templates.TemplateResponse(
            "vehicledata.html",
            {"request":request,"context":f"error : {e}"},
        )
if __name__ =="__main__":
    try:
        app_run(app,host=APP_HOST,port = APP_PORT)
    except Exception as e:
        logging.error(f"Failed to start the app : {e}")
        sys.exit(1)