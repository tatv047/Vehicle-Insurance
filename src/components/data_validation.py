import json
import sys
import os

import pandas as pd

from pandas import DataFrame

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import read_yaml_file
from src.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from src.entity.config_entity import DataValidationConfig
from src.constants import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config: DataValidationConfig):
        """
        data_ingestion_artifact: output reference of data ingestion artifact stage
        data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)
        
    def validate_number_of_columns(self,dataframe:DataFrame)->bool:
        """
        Method name: validate_number_of_columns
        Description: Validates the no. of columns

        Output: Returns bool based on validation results
        On Failure: Write an exception log and then raise an exception
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Are required columns present?: [{status}]")
            return status
        except Exception as e:
            raise MyException(e,sys)
        
    def do_columns_exist(self,df: DataFrame)->bool:
        """
        Method name: do_columns_exist
        Description: Validates the existence of a numerical and catgeorical column

        Output: Returns bool based on validation results
        On Failure: Write an exception log and then raise an exception
        """        
        try:
            dataframe_columns = df.columns
            missing_numerical_cols = []
            missing_categorical_cols = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_cols.append(column)
            
            if len(missing_numerical_cols)>0:
                logging.info(f"Missing numerical columns: {missing_numerical_cols}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_cols.append(column)
            
            if len(missing_categorical_cols)>0:
                logging.info(f"Missing categorical columns: {missing_categorical_cols}")

            return False if len(missing_numerical_cols)>0 or len(missing_categorical_cols)>0 else True
        except Exception as e:
            raise MyException(e,sys)


    @staticmethod
    def read_data(file_path)->DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        """
        Method name: initiate_data_validation
        Description: Initiates the data validation component of the training pipeline

        Output: Returns bool based on validation results
        On Failure: Write an exception log and then raise an exception
        """  
        try:
            validation_error_msg = ""
            logging.info("starting Data Validation")
            train_df,test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))
            
            #checking column length of test/train df
            status = self.validate_number_of_columns(dataframe=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe"
            else:
                logging.info(f"All required columns are present in training dataframe: {status}")

            status = self.validate_number_of_columns(dataframe=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in testing dataframe. "
            else:
                logging.info(f"All required columns are present in testing dataframe: {status}")

            # Validating column type for train/test df
            status = self.do_columns_exist(df = train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            else:
                logging.info(f"All int/categorical columns are present in training dataframe: {status}")

            status = self.do_columns_exist(df=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in testing dataframe"
            else:
                logging.info(f"All int/categorical columns are present in testing dataframe: {status}")

            validation_status = len(validation_error_msg) == 0

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )


            # ensure the directory of validation_report_file_path exists
            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            # save validation status and message to a JSON file
            validation_report = {
                "validation_status" : validation_status,
                "message" : validation_error_msg.strip()
            }
            
            with open(self.data_validation_config.validation_report_file_path,"w") as report_file:
                json.dump(validation_report,report_file,indent = 4)

            logging.info("Data Validation artifact created and saved to JSON file")
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys) from e 

            