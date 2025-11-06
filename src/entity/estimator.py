import sys

import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.exception import MyException
from src.logger import logging
from src.constants import SCHEMA_FILE_PATH
from src.utils.main_utils import read_yaml_file

class TargetValueMapping:
    def __init__(self):
        self.yes:int=1
        self.no:int=0
    
    def _asdict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))
    
class MyModel:

    def __init__(self,preprocessing_object:Pipeline,trained_model_object:object):

        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
        self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
    def _map_gender_column(self, df):
        logging.info("Mapping 'Gender' column...")
        df['Gender'] = df['Gender'].fillna('Female')
        df['Gender'] = df['Gender'].map({'Female':0,'Male':1}).astype(int)
        return df
    
    def _drop_id_column(self, df):
        logging.info("Dropping '_id' column.")
        drop_col = self._schema_config['drop_columns']
        if drop_col in df.columns:
            df = df.drop(drop_col, axis=1)
        return df

    def _create_dummy_columns(self, df):
        logging.info('Creating dummy variables...')
        cat_cols = ['Vehicle_Age', 'Vehicle_Damage'] 
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
        return df
    
    def _rename_columns(self, df):
        logging.info("Renaming columns...")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })

        
        expected_cols = ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]
        for col in expected_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0).astype('int')
            else:
                logging.info(f"Creating missing dummy column: {col}")
                df[col] = 0 
        return df
    def predict(self,dataframe:pd.DataFrame)-> DataFrame:
        try:
            logging.info("Starting prediction process")
            dataframe = dataframe.copy()
            
            dataframe = self._map_gender_column(dataframe)
            dataframe = self._drop_id_column(dataframe)
            dataframe = self._create_dummy_columns(dataframe)
            dataframe = self._rename_columns(dataframe)  

            transform_feature = self.preprocessing_object.transform(dataframe)

            logging.info("using trained model to get predictions")
            prediction = self.trained_model_object.predict(transform_feature)

            return prediction
        
        except Exception as e:
            logging.error("Error occurred in predict method",exc_info= True)
            raise MyException(e,sys) from e
    
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    
    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"