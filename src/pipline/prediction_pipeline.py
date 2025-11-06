import sys
import pandas as pd
from pandas import DataFrame

from src.exception import MyException
from src.logger import logging
from src.entity.s3_estimator import ProjEstimator
from src.entity.estimator import TargetValueMapping
from src.constants import MODEL_BUCKET_NAME,MODEL_PUSHER_S3_KEY

class VehiclePredictionConfig:
    def __init__(self):
        self.mode_bucket_name:str=MODEL_BUCKET_NAME
        self.mode_file_path:str=MODEL_PUSHER_S3_KEY

class VehicleData:
    def __init__(self,
        Gender:str,
        Age:int,
        Driving_License:int,
        Region_Code:float,
        Previously_Insured:int,
        Vehicle_Age:str,
        Vehicle_Damage:str,
        Annual_Premium:float,
        Policy_Sales_Channel:float,
        Vintage:int
        ):

        try:
            self.Gender = Gender
            self.Age = Age
            self.Driving_License = Driving_License
            self.Region_Code = Region_Code
            self.Previously_Insured = Previously_Insured
            self.Annual_Premium = Annual_Premium
            self.Policy_Sales_Channel = Policy_Sales_Channel
            self.Vintage = Vintage
            
            
            self.Vehicle_Age = Vehicle_Age
            self.Vehicle_Damage = Vehicle_Damage

        except Exception as e:
            raise MyException(e, sys) from e
    
    def get_vehicle_data_as_dict(self):
        logging.info("Entered get_vehicle_data_as_dict method in. prediction pipeline")

        try:
            input_data={
                "Gender": [self.Gender],
                "Age": [self.Age],
                "Driving_License": [self.Driving_License],
                "Region_Code": [self.Region_Code],
                "Previously_Insured": [self.Previously_Insured],
                "Annual_Premium": [self.Annual_Premium],
                "Policy_Sales_Channel": [self.Policy_Sales_Channel],
                "Vintage": [self.Vintage],
                "Vehicle_Age": [self.Vehicle_Age], 
                "Vehicle_Damage": [self.Vehicle_Damage]
            }
            logging.info("Created vehicle data dict")
            return input_data
        except Exception as e:
            raise MyException(e,sys) from e
        
    def get_vehicle_input_data_frame(self)->DataFrame:
        try:
            vehicle_input_dict = self.get_vehicle_data_as_dict()
            return DataFrame(vehicle_input_dict)
        except Exception as e:
            raise MyException(e,sys) from e

class VehicleDataClassifier:
    def __init__(self,prediction_pipeline_config:VehiclePredictionConfig=VehiclePredictionConfig())->None:
        try:
            self.prediction_pipeline_config = prediction_pipeline_config

            self.model = ProjEstimator(
                bucket_name=self.prediction_pipeline_config.mode_bucket_name,
                model_path=self.prediction_pipeline_config.mode_file_path
            )

            self.translator = TargetValueMapping().reverse_mapping()
            logging.info("Prediction pipeline loaded and ready")
        except Exception as e:
            raise MyException(e,sys)
    
    def predict(self,dataframe:DataFrame)->str:
        try:
            logging.info("Entered predict method of VehicleDataClassifier")

            numeric_prediction = self.model.predict(dataframe)
            prediction_value = numeric_prediction[0]

            string_prediction = self.translator[prediction_value]

            logging.info(f"FINAL PREDICTON : {string_prediction}")

            return string_prediction
        except Exception as e:
            raise MyException(e,sys)
        

