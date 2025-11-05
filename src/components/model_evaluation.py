import sys 
import os
import pandas as pd
from sklearn.metrics import f1_score

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import load_object,read_yaml_file
from src.constants import TARGET_COLUMN
from src.entity.artifact_entity import ModelTrainerArtifact,DataIngestionArtifact,ModelEvaluationArtifact,ClassificationMetricArtifact
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.s3_estimator import ProjEstimator
from src.entity.estimator import MyModel

from dataclasses import dataclass
from typing import Optional

@dataclass
class EvaluateModelResponse:
    trained_model_f1_score:float
    best_model_f1_score:float
    is_model_accepted:bool
    difference:float

class ModelEvaluation:

    def __init__(self,model_eval_config:ModelEvaluationConfig,data_ingestion_artifact:DataIngestionArtifact,model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys) from e
    
    def get_champion_model(self)-> Optional[ProjEstimator]:
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.s3_model_key

            proj_estimator = ProjEstimator(bucket_name=bucket_name,model_path=model_path)

            if proj_estimator.is_model_present(model_path=model_path):
                logging.info("Champion model found in S3.")
                return proj_estimator
            
            logging.info("No champion model found in S3.This must be the first model")
            return None
        except Exception as e:
            raise MyException(e,sys)
        
    def evaluate_model(self)-> EvaluateModelResponse:
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            x_test,y_test = test_df.drop(TARGET_COLUMN,axis=1),test_df[TARGET_COLUMN]
            
            logging.info("Loading Challenger(newly Trained) model from local artifact")
            
            challenger_model:MyModel = load_object(file_path=self.model_trainer_artifact.trained_model_path)

            y_pred_challenger=challenger_model.predict(x_test)

            challenger_f1_score = f1_score(y_test,y_pred_challenger)
            logging.info(f"Challenger Model F1 score : {challenger_f1_score}")

            champion_model:ProjEstimator = self.get_champion_model()

            if champion_model is None:
                logging.info("No champion Model to compare against .Challenger wins by default")
                best_model_f1_score = 0.0
                is_accepted=True
                difference = challenger_f1_score - best_model_f1_score
            else:
                logging.info("Evaluating Champion(production) model...")

                y_pred_champion = champion_model.predict(x_test)
                best_model_f1_score = f1_score(y_test,y_pred_champion)
                logging.info(f"Champion Model F1 score : {best_model_f1_score}")
                
                difference = challenger_f1_score - best_model_f1_score

                if difference > self.model_eval_config.changed_threshold_score:
                    is_accepted = True
                    logging.info(f"Challenger is better by {difference} (threshold is {self.model_eval_config.changed_threshold_score}.)Model Accepted!")
                else:
                    is_accepted=False
                    logging.info(f"Challenger F1 {challenger_f1_score}is not better than champion F1 {best_model_f1_score} by the required threshold New Model rejected")   

            response = EvaluateModelResponse(
                trained_model_f1_score=challenger_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=is_accepted,
                difference=difference
            )
            logging.info(f"Model Evaluation Response : {response}")
            return response
        except Exception as e:
            raise MyException(e,sys)
    
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            logging.info("MODEL EVALUATION component Started")
            evaluate_model_response = self.evaluate_model()

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                changed_accuracy=evaluate_model_response.difference,
                s3_model_path=self.model_eval_config.s3_model_key,
                trained_model_path=self.model_trainer_artifact.trained_model_path
            )
            logging.info(f"Model Evaluation Artifact : {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e,sys) from e