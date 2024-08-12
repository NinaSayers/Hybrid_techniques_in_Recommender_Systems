import json
import time
from data_access.data_source import DataSource
from services.logger import Logger

class DataAccess:
    '''With this class we gonna handle read and writing to persistent data'''
    data_sources: list[DataSource]
    def __init__(self, logger: Logger, json_config_path) -> None:
        self.data_sources = []
        self.logger = logger

        with open(json_config_path,'r') as config_file:
            config = json.load(config_file)
            
            for dataSource in config['DataSources']:
                name = dataSource['name']
                path = dataSource['path']
                if name is None:
                    raise ValueError("The field 'name' can't be null.")
                if path is None:
                    raise ValueError("The field 'path' can't be null.")
               
                self.logger.info(f'Adding data source {name} from {path}') 
                self.data_sources.append(DataSource(name,path))
    
    def load_resources(self):
        start_time = time.time()
        result = []
        self.logger.info(f'Loading data from resources...')
        
        for res in self.data_sources:
            result.append(res.get_data())
        
        elapsed_time = time.time() - start_time
        if elapsed_time > 2:
            self.logger.warn(f'Loading resources took too long: {elapsed_time:.2f} seconds.')
        else:
            self.logger.info(f'Resources loaded successfully in {elapsed_time:.2f} seconds.')
        
        return result
    
    def load_resource(self,name: str):
        start_time = time.time()
        self.logger.info(f'Loading data from resource {name}...')
        
        for res in self.data_sources: 
            if res.name == name:
                data = res.get_data()
                
                elapsed_time = time.time() - start_time
                if elapsed_time > 10:
                    self.logger.warn(f'Loading resources took too long: {elapsed_time:.2f} seconds.')
                else:
                    self.logger.info(f'Resources loaded successfully in {elapsed_time:.2f} seconds.')
                
                return data
        self.logger.error(f'Could not find any data source with name: {name}')        
        raise f"Could not find any data source with name: {name}"
