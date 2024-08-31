from abc import ABC, abstractmethod
from typing import List
from models.context_model import Context
from models.filter_result_model import FilterResultModel
from services.logger import Logger
from abc import ABC, abstractmethod


class FilterBase(ABC):
    def __init__(self):
        self.logger = Logger()

    @abstractmethod
    def apply_filter(self, context: Context) -> FilterResultModel:
        """Apply filters using the context and return a FilterResults"""
        pass
