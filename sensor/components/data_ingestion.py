from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
import os, sys
from pandas import DataFrame
from sensor.data_access.sensordata import SensorData
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            #self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)

    def export_data_into_feature_store(self)-> DataFrame:
        """
        Export data from MongoDB collection as Dataframe
        """
        try:
            logging.info("Exporting Data from mongodb to feature store")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)

            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating feature_store folder from feature store file path

            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)

            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise SensorException(e,sys)




    def split_data_into_train_test(self,dataframe:DataFrame):

        """
        Splits the dataframe into train and test, converts to .csv and makes dir's to store them
        """

        try:
            train_set, test_set = train_test_split(dataframe,
            test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Train Test Split activity completed on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Exporting the train and test file path started")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info(f"Exporting the train and test path completed.")
        except Exception as e:
            raise SensorException(e,sys)


    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_into_train_test(dataframe=dataframe)
            data_ingestion_artifact= DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.test_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)

