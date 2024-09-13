from abc import ABC, abstractmethod
from typing import List
from models.context_model import Context
from models.filter_result_model import FilterResultModel
from services.logger import Logger

class FilterBase(ABC):
    def __init__(self):
        """
        Initializes the FilterBase with a logger.

        The logger is used for logging messages and errors during filter operations.
        """
        self.logger = Logger()

    @abstractmethod
    def apply_filter(self, context: Context) -> FilterResultModel:
        """
        Apply filters to the provided context and return the results.

        This method must be implemented by subclasses to define specific filtering logic.

        Args:
            context (Context): The context containing information such as user ID,
                               product list, and any other relevant data for filtering.

        Returns:
            FilterResultModel: The results of the filtering operation, including recommended
                               products or any other relevant filtering outcomes.
        """
        pass
