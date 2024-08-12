import pandas as pd

class DataSource:
    '''This is meant to be used only with .csv files''' 
    name: str
    path: str
    def __init__(self, name: str , path: str) -> None:
        self.name = name
        self.path = path
    def get_data(self) -> pd.DataFrame:
        return pd.read_csv(self.path)        
