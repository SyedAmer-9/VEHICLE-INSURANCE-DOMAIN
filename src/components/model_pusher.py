import sys
import os
from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifact,ModelTrainerArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.s3_estimator import ProjEstimator


class ModelPusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact,model_pusher_config:ModelPusherConfig,model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_evaluation_artifact = model_evaluation_artifact
            self.model_pusher_config=model_pusher_config
            self.model_trainer_artifact = model_trainer_artifact

            self.proj_estimator = ProjEstimator(
                bucket_name=self.model_pusher_config.bucket_name,
                model_path=self.model_pusher_config.s3_model_key
            )
        except Exception as e:
            raise MyException(e,sys) from e
    
    def initiate_model_pusher(self)->ModelPusherArtifact:
        logging.info("Enterd initiate_model_pusher method of ModelPusher class")

        try:
            if not self.model_evaluation_artifact.is_model_accepted:
                logging.info("Model was not accepted by evaluation componen.Skipping push to s3")
                return None
        
            local_model_path = self.model_trainer_artifact.trained_model_path

            logging.info(f"Uploading the new model to S3 from {local_model_path}")

            self.proj_estimator.save_model(from_file=local_model_path)

            logging.info("Model saved successfully to S3")

            model_pusher_artifact = ModelPusherArtifact(
                pushed_model_s3_uri = f"s3://{self.model_pusher_config.bucket_name}/{self.model_pusher_config.s3_model_key}",
                saved_model_path=local_model_path
            )

            logging.info(f"Model Pusher Artifact : [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")

            return model_pusher_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        

