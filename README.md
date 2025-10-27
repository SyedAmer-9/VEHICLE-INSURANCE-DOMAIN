# VEHICLE-INSURANCE-DOMAIN

Project Introduction 



--------------------------------------------------------------------------------------------------------------
                                               Project Introduction 
**Tools and Techniques Used in this project ->**
*MongoDB - for data storage
*Robust pipeline - Training/Prediction
*FastApi - For high performance prediction API ( acts as a waiter sits inside a docker which is stored on ECR)
*CICD - Github Actions
*AWS - IAM,ECR,EC2(IAM for managing permissions securely,ECR(Elastic Container Registry - to store docker images ,EC2(Elastic Compute Cloud - a cloud to host and run your application(i.e FastAPI inside a Docker container)
*No conventional mlops tools used ( i.e no Kubeflow , MLflow or sagemaker)

overview - 
FastApi is the waiter,its a python framework that creates an API 
you sent an HTTP request to specific URL and FastAPI receives the order and carries it to the ML model
Then the Fast API takes this answer and delivers it back to as an HTTP response

ECR is like an App store that just stores the Docker image
EC2 is a virtual computer that we rent from AWS,EC2 instance is a blank computer

**Discussing System Design**
Components -> Data Ingestion,Data Validation,Data Transformation,Model Training,Model Evaluation,Model Pusher
Data Ingestion - attaching multiple files,connects to mongoDb and fetches desired data
Data Validation - check columns, consistency etc
Data Transformation - feature engineering
Model training - Trian the model
Model Evaluation - adjusting paramenters , Hypertuning
Model Pusher - push the model to cloud

**Workflow**
constants->config_entity->artifact_entity->component->pipeline->demo.py/app.py

--------------------------------------------------------------------------------------------------------------




