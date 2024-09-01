
from typing import List
from models.recommendation_model import RecommendationModel
from services.logger import Logger


class FilterResultModel:
    def __init__(self, user_id: str, recommendations: List[RecommendationModel]):
        self.user_id = user_id
        self.recommendations = recommendations
        self.logger = Logger()

    def show_recommendations(self):
        data = [[i+1, x.product_id, x.similarity_score] for i, x in enumerate(self.recommendations)]
        headers = ["Row", "Product", "Score"]
        self.logger.print_markdown_table(headers, data)