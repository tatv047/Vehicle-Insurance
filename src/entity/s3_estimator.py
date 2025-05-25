from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.entity.estimator import MyModel
import sys
from pandas import DataFrame

class Proj1Estimator:
    """
    This class is used to save and retrieve models in a s3 bucket and to do prediction 
    """
    def __init__(self,bucket_name,model_path,):
        """
        bucket_name : name of your model bucket
        model_path: Location of your model in bucket
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: MyModel = None
        
    def is_model_present(self,model_path):
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name,s3_key=model_path)
        except Exception as e:
            print(e)
            return False
        
    def load_model(self,)->MyModel:
        """
        Load the model from the model_path
        """
        return self.s3.load_model(self.model_path,bucket_name=self.bucket_name)
    
    def save_model(self,from_file,remove:bool = False)->None:
        """
        Save the model to the model_path
        from_file: your local system model path
        remove: by default it is false that mean you will have your model locally available in your system
        folder
        """
        try:
            self.s3.upload_file(
                from_file,
                to_filename=self.model_path,
                bucket_name= self.bucket_name,
                remove= remove
            )
        except Exception as e:
            raise MyException(e,sys)
        
    def predict(self,dataframe: DataFrame):
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise MyException(e,sys)

        