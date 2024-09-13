class RecommendationModel:
    def __init__(self, product_id: str, similarity_score: float):
        """
        Initializes the RecommendationModel with a product ID and its similarity score.

        Args:
            product_id (str): The ID of the product being recommended.
            similarity_score (float): The similarity score of the product, indicating how relevant the recommendation is.
        """
        self.product_id = product_id
        self.similarity_score = similarity_score

    def __repr__(self) -> str:
        """
        Provides a string representation of the RecommendationModel instance.

        Returns:
            str: A string representation of the RecommendationModel, showing product_id and similarity_score.
        """
        return f"RecommendationModel(product_id='{self.product_id}', similarity_score={self.similarity_score})"
