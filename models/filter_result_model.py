from typing import List
from models.recommendation_model import RecommendationModel
from services.logger import Logger

class FilterResultModel:
    def __init__(self, user_id: str, recommendations: List[RecommendationModel]):
        """
        Initializes the FilterResultModel with user ID and a list of recommendations.

        Args:
            user_id (str): The ID of the user for whom the recommendations are generated.
            recommendations (List[RecommendationModel]): A list of RecommendationModel instances.
        """
        self.user_id = user_id
        self.recommendations = recommendations
        self.logger = Logger()

    def show_recommendations(self):
        """
        Displays the recommendations in a markdown table format using the logger.
        
        The table includes columns for row number, product ID, and similarity score.
        """
        # Prepare data for the markdown table
        data = [[i + 1, x.product_id, x.similarity_score] for i, x in enumerate(self.recommendations)]
        headers = ["Row", "Product", "Score"]
        
        # Use the logger to print the markdown table
        self.logger.print_markdown_table(headers, data)
