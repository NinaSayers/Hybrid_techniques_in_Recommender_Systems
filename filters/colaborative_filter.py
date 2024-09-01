from typing import List, Optional
from sqlalchemy.orm import Session
from data_access.db.repositories import CustomerRepository, InteractionRepository, ProductRepository
from filters.filter_base import FilterBase
from models.context_model import Context
from models.filter_result_model import FilterResultModel
from models.recommendation_model import RecommendationModel

class CollaborativeFilter(FilterBase):
    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session
        self.customer_repository = CustomerRepository(session)
        self.interaction_repository = InteractionRepository(session)
        self.product_repository = ProductRepository(session)

    def apply_filter(self, context: Context) -> FilterResultModel:
        self.logger.info(f"Applying collaborative filtering to {len(context.products)} products for user {context.userId} with limit {context.limit}.")

        # Get user interactions
        user_interactions = self.interaction_repository.get_interactions_by_user(context.userId)
        if not user_interactions:
            self.logger.warn(f"No interactions found for user {context.userId}.")
            return FilterResultModel(user_id=context.userId, recommendations=[])

        # Get all products and generate an interaction matrix
        all_products = self.product_repository.get_all()
        product_ids = [product.unique_id for product in all_products]

        # Build the interaction matrix
        interaction_matrix = self._build_interaction_matrix(product_ids)

        # Calculate user similarities
        user_index = self._get_user_index(context.userId, interaction_matrix)
        if user_index is None:
            self.logger.warn(f"User {context.userId} not found in the interaction matrix.")
            return FilterResultModel(user_id=context.userId, recommendations=[])

        user_similarities = self._calculate_user_similarities(user_index, interaction_matrix)

        # Generate recommendations
        recommendations = self._generate_recommendations(user_index, user_similarities, product_ids, interaction_matrix, context)

        return FilterResultModel(user_id=context.userId, recommendations=recommendations)

    def _build_interaction_matrix(self, product_ids: List[str]) -> List[List[int]]:
        customers = self.customer_repository.get_all()
        interaction_matrix = []

        for customer in customers:
            interactions = self.interaction_repository.get_interactions_by_user(customer.customer_id)
            interaction_row = [0] * len(product_ids)
            for interaction in interactions:
                if interaction.product_id in product_ids:
                    index = product_ids.index(interaction.product_id)
                    interaction_row[index] = self._get_interaction_weight(interaction.interaction_type)
            interaction_matrix.append(interaction_row)

        return interaction_matrix

    def _get_interaction_weight(self, interaction_type: str) -> int:
        weights = {
            "view": 1,
            "like": 2,
            "purchase": 3
        }
        return weights.get(interaction_type, 0)

    def _get_user_index(self, user_id: int, interaction_matrix: List[List[int]]) -> Optional[int]:
        customers = self.customer_repository.get_all()
        for i, customer in enumerate(customers):
            # print(str(customer.customer_id) + str(i))
            if customer.customer_id == user_id:
                return i
        return None

    def _calculate_user_similarities(self, user_index: int, interaction_matrix: List[List[int]]) -> List[float]:
        user_vector = interaction_matrix[user_index]
        similarities = []

        for i, other_user_vector in enumerate(interaction_matrix):
            if i == user_index:
                continue
            similarity = self._cosine_similarity(user_vector, other_user_vector)
            similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities

    def _cosine_similarity(self, vector_a: List[int], vector_b: List[int]) -> float:
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        magnitude_a = sum(a**2 for a in vector_a) ** 0.5
        magnitude_b = sum(b**2 for b in vector_b) ** 0.5
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
        return dot_product / (magnitude_a * magnitude_b)

    def _generate_recommendations(self, user_index: int, user_similarities: List[float], product_ids: List[str], interaction_matrix: List[List[int]], context: Context) -> List[RecommendationModel]:
        recommendations = []
        for similar_user_index, _ in user_similarities:
            for i, interaction in enumerate(interaction_matrix[similar_user_index]):
                if interaction > 0 and interaction_matrix[user_index][i] == 0:
                    recommendations.append(
                        RecommendationModel(product_id=product_ids[i], similarity_score=interaction)
                    )
                    if len(recommendations) >= context.limit:
                        return recommendations
        return recommendations
