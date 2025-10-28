# VEHICLE-INSURANCE-DOMAIN

Project Introduction 



--------------------------------------------------------------------------------------------------------------
                                               Project Introduction 
**Tools and Techniques i used in this project ->**
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
                                            MONGO DB SETUP
I now created a GitHub repo with .gitignore(python) , ReadMe.md(the birth of this file :D) , Liscence(MIT)
in Local Computer i opened my code editor( i use vscode) and cloned the Github.
now in the project folder i create a virtual python environment(named mlops) and source/bin/activate it :D
i add the virtual environment to .gitignore as venvs are huge storage and often not pushed to github
I create a template.py which contains the fodler structure of mlops project i acquire this from internet as folder structures are often common i run this python script to create empty folder and files the template.py is also pushed on github

Now the official project begins
i began with writing setup.py and pyproject.toml
But First what are they?
lets start with setup.py
setup.py - This is the original,classic method for creating a package.Its a python script that uses the setuptools library
Why use it? - Its a script which makes it extremely powerful and flexible

explanation of the script
name = 'src' -> it tells how pip sees your project ex pip install <name>
version -> the version number important for tracking changes
author and author_email -> simple metadata
packages=find_packages() -> it tells setup.py what code to include in the package in our case find_packages() automatically finds all folders that have an __init__.py file in our case src and all its subfolders contain __init__.py so it includes all those code

now about pyproject.toml(the modern way) ->It's the modern standard. It not only defines your package but also configures all your development tools toml stands for (toms obvious minimal language)
from file we can see  [tool.setuptools] -> section tells your build tool
packages={find={}}->this line is the new,declarative wat to say find_packages()
[tool.setuptools.dynamic] -> this is for settings that are dynamically loaded from other files
dependencies = {file = "requirements.txt} -> this is a key feature it tells setuptools to find the dependencies(like pandas ,fastapi) go and read the requirements.txt file 

WHy do we have BOTH?
mine pyproject.toml file is complete it has all the infor from setup.py and more(like dependencies part)
when we have both modern pip and other setuptools will prefer pyproject.toml
the setup.py is not often kept for backward compatibility or for complex logix that pyproject.toml cant handle for this project it's reduntant

Now i added requirements.txt file to our project root folder
it contains the following libraries
#Data Science and ML
pandas -> for data manipulation and analysis(think it as excel sheer of python)
numpy -> the fundamental package for scientific computing and working with arrays
matplotlib -> a standard library for creating static plots and graphs
plotly -> for creating modern interactive plots
seaborn -> built on top of matplotlib,makes creating beautiful statistical plots easier
scikit-learn -> this the machine learning library(ofc everyone knows it)
imblearn -> a spl sklearn add on to handle imbalanced datasets(like 99% no fraud and 1% fraud samples)
#API & Web Server
fastapi -> the waiter we use to build high speed prediction api
uvicorn -> the web server that runs the fastAPI application
python-multipart -> required by FastAPI to handle file uploads
jinja2 -> a tempalting engine(allows api to serve anHTML webpage like a demo dashboard)
#Database & Cloud
pymongo -> the official driver to connect to and interact with mongoDB database
boto3 -> the official AWS SDK for python allows code to talk with AWS services like S3 EC2 ECR
botocore -> the low level library that boto3 is built on
mypy-boto3-s3 -> provides type-hinting for boto3(auto completiomn and error checking)
#Core project & Utilities
ipykernel -> the kernel allows Jupyter notebooks to run your mlops virtual env
from_root -> a small utility to manage file paths ,making easy to find files relative to projects root directory
dill -> an advanced version of Python's pickle used to serialize(save) complex python objects like trained ML models
certifi -> orivides an up to date bundle of SSL certificates which pymongo and other web libraries need to make secure (httpS) connections
pyYAML -> a lib for reading and writing .yaml files 

-e . -> is an instructin for pip tells pip to install the project in the current directory(.) in editable mode(-e) this command that installs my src folder inside my mlops virtual env

The command pip install -e . is crucial for our project because it installs our src folder as a locally editable package within our virtual environment. The primary problem this solves is the ModuleNotFoundError that would otherwise happen when scripts outside src (like app.py) try to import code from inside it. Python doesn't automatically know to look in the src folder, but running this command using our pyproject.toml file fixes that. It creates a link in Python's main site-packages directory that points directly to our src folder, effectively teaching Python to treat src just like any other installed library, such as pandas or numpy. This makes our project's code importable from anywhere. The -e (or "editable") flag is the most important part, as it installs a link instead of a copy. This means any edits we make to our source code are immediately effective on the next run, with no re-installation required. This is the standard, clean way to make our project's modules available during development.

when you type pip list it shows currently installed packages i.e. for me it showed just pip but after running pip install -r requirements.txt pip will install all the listed librariesp
and when you type pip list all the libararies and their dependencies show up but here a point to notice is that in the list we can also see src show up this is due to -e . part instruction

here comes the database part where i setup mongoDB organisation and then i create a project inside that project i create a cluster i used email to login into MongoDB atlas, the project name is vehicle_proj, now we create a cluster we use free plan as for now and then select mumbai server and create a cluster we get a username and password that are required to gain access to that cluster save that username and password somewhere in the notepad now go to network access and add ip address so that we can access it from anywhere i.e., 0.0.0.0/0 now we head back to project site and click on get connection string now we select python as the driver and Version as 3.12 and later as it is a stable version now copy the connection string and paste it inside your project folder now i create a folder called notebook which contains data.csv file of our project also now i create a file called monoDB_demo.ipynb this is for pushing dataset folder from local to mongoDB cloud inside mongoDB_demo file we import pandas and pymongo libraries we create a df of data.csv and use head() function to check first five rows of dataset, now df should be converted in to dict before we push it to mongoDB as mongoDB is no relational database so we should upload it into key-value pair we use to_dict(orient='records') function for it now our next step is to setup cloud database with DB_NAME = 'Proj1' and COLLECTION_NAME='Proj1-Data' CONNECTION_URL = "the url that you saved in notepad no i am not dumb enough to put it here in a public repository" now we use pymongo.MongoClient to create a client object which is used to connect to entire MongoDB server(cluster) and use that client object to connect to the data_base.I encountered a problem here where i used @ in password for database and struggled for 2 hours but finally debugged it yeah a simple mistake and now i pushed the data.csv to mongoDB cluster using collection.insert_manY(data), we can see the uploaded data in mongoDB atlas and see all the collection/documents.

Now i move on to the next part i.e., Logging of the data so now go to src folder and open logger folder and open init.py 
--------------------------------------------------------------------------------------------------------------



