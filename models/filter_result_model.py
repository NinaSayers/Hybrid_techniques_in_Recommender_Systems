
from typing import List
from models.recommendation_model import RecommendationModel
from services.logger import Logger


class FilterResultModel:
    def __init__(self, user_id: str, recommendations: List[RecommendationModel]):
        self.user_id = user_id
        self.recommendations = recommendations
        self.logger = Logger()