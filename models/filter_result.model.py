
from typing import List
from services.logger import Logger


class FilterResultModel:
    def __init__(self, product_id: str, recommendations: List[RecommendationModel]):
        self.product_id = product_id
        self.recommendations = recommendations
        self.logger = Logger()