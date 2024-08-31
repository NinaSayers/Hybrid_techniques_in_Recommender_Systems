
class RecommendationModel:
    def __init__(self, product_id: str, similarity_score: float):
        self.product_id = product_id
        self.similarity_score = similarity_score
