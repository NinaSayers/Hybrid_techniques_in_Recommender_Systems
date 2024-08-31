from abc import ABC, abstractmethod
from typing import List
from services.logger import Logger
from models.filter_result.model import FilterResultModel 

class FilterBase(ABC):
    def __init__(self):
        self.logger = Logger()

    @abstractmethod
    def apply_filter(self, products: List) -> List[FilterResultModel]:
        """Apply filters and return a list of FilterResults"""
        pass
