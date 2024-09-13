from typing import List, Optional
from sqlalchemy.orm import Session
from data_access.db.repositories import CustomerRepository, InteractionRepository, ProductRepository
from filters.filter_base import FilterBase
from models.context_model import Context
from models.filter_result_model import FilterResultModel
from models.recommendation_model import RecommendationModel

class CollaborativeFilter(FilterBase):
    """
    A collaborative filtering recommendation system based on user interactions.
    """

    def __init__(self, session: Session) -> None:
        """
        Initializes the CollaborativeFilter with the given database session.

        Args:
            session (Session): The SQLAlchemy session used for database operations.
        """
        super().__init__()
        self.session = session
        self.customer_repository = CustomerRepository(session)
        self.interaction_repository = InteractionRepository(session)
        self.product_repository = ProductRepository(session)

    def apply_filter(self, context: Context) -> FilterResultModel:
        """
        Applies collaborative filtering to generate product recommendations for a user.

        Args:
            context (Context): The context containing user ID, product list, and limit for recommendations.

        Returns:
            FilterResultModel: The result model containing user ID and a list of recommended products.
        """
        self.logger.info(f"Applying collaborative filtering to {len(context.products)} products for user {context.userId} with limit {context.limit}.")

        # Retrieve user interactions
        user_interactions = self.interaction_repository.get_interactions_by_user(context.userId)
        if not user_interactions:
            self.logger.warn(f"No interactions found for user {context.userId}.")
            # Generate default recommendations if no interactions are found
            all_recommendations = [RecommendationModel(x.unique_id, 1) for x in context.products]
            recommendations = all_recommendations[:50]
            return FilterResultModel(user_id=context.userId, recommendations=recommendations)

        # Retrieve all products and build the interaction matrix
        all_products = self.product_repository.get_all()
        product_ids = [product.unique_id for product in all_products]

        # Build the interaction matrix for all products
        interaction_matrix = self._build_interaction_matrix(product_ids)

        # Find the index of the user in the interaction matrix
        user_index = self._get_user_index(context.userId)
        if user_index is None:
            self.logger.warn(f"User {context.userId} not found in the interaction matrix.")
            all_recommendations = [RecommendationModel(x.unique_id, 1) for x in context.products]
            recommendations = all_recommendations[:50]
            return FilterResultModel(user_id=context.userId, recommendations=recommendations)

        # Calculate user similarities based on interaction matrix
        user_similarities = self._calculate_user_similarities(user_index, interaction_matrix)

        # Generate product recommendations based on user similarities
        recommendations = self._generate_recommendations(user_index, user_similarities, product_ids, interaction_matrix, context)

        return FilterResultModel(user_id=context.userId, recommendations=recommendations)

    def _build_interaction_matrix(self, product_ids: List[str]) -> List[List[int]]:
        """
        Builds an interaction matrix from customer interactions.

        Args:
            product_ids (List[str]): List of product IDs to create the interaction matrix for.

        Returns:
            List[List[int]]: A matrix where each row represents a customer and each column represents a product.
        """
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
        """
        Returns the weight of an interaction based on its type.

        Args:
            interaction_type (str): The type of interaction (e.g., "view", "like", "purchase").

        Returns:
            int: The weight assigned to the interaction type.
        """
        weights = {
            "view": 1,
            "like": 2,
            "purchase": 3
        }
        return weights.get(interaction_type, 0)

    def _get_user_index(self, user_id: int) -> Optional[int]:
        """
        Finds the index of a user in the interaction matrix.

        Args:
            user_id (int): The ID of the user to find.

        Returns:
            Optional[int]: The index of the user in the interaction matrix or None if not found.
        """
        customers = self.customer_repository.get_all()
        for i, customer in enumerate(customers):
            if customer.customer_id == user_id:
                return i
        return None

    def _calculate_user_similarities(self, user_index: int, interaction_matrix: List[List[int]]) -> List[tuple]:
        """
        Calculates similarities between the specified user and other users.

        Args:
            user_index (int): The index of the user in the interaction matrix.
            interaction_matrix (List[List[int]]): The matrix of user interactions.

        Returns:
            List[tuple]: A list of tuples where each tuple contains a user index and the similarity score.
        """
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
        """
        Computes the cosine similarity between two vectors.

        Args:
            vector_a (List[int]): The first vector.
            vector_b (List[int]): The second vector.

        Returns:
            float: The cosine similarity score between the two vectors.
        """
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        magnitude_a = sum(a**2 for a in vector_a) ** 0.5
        magnitude_b = sum(b**2 for b in vector_b) ** 0.5
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
        return dot_product / (magnitude_a * magnitude_b)

    def _generate_recommendations(self, user_index: int, user_similarities: List[tuple], product_ids: List[str], interaction_matrix: List[List[int]], context: Context) -> List[RecommendationModel]:
        """
        Generates product recommendations based on user similarities and interactions.

        Args:
            user_index (int): The index of the user in the interaction matrix.
            user_similarities (List[tuple]): A list of user similarities with other users.
            product_ids (List[str]): List of product IDs for recommendation.
            interaction_matrix (List[List[int]]): The matrix of user interactions.
            context (Context): The context containing user ID, product list, and recommendation limit.

        Returns:
            List[RecommendationModel]: A list of recommendations for the user.
        """
        recommendations = []
        recommended_scores = {}

        # Normalize user similarities to the range [0, 1]
        max_similarity = max(similarity for _, similarity in user_similarities) if user_similarities else 1

        for similar_user_index, similarity in user_similarities:
            for i, interaction in enumerate(interaction_matrix[similar_user_index]):
                if interaction > 0 and interaction_matrix[user_index][i] == 0:
                    normalized_similarity = similarity / max_similarity if max_similarity != 0 else 0
                    
                    if product_ids[i] in recommended_scores:
                        recommended_scores[product_ids[i]] += interaction * normalized_similarity
                    else:
                        recommended_scores[product_ids[i]] = interaction * normalized_similarity

        # Sort recommendations by score and limit the number of recommendations
        sorted_recommendations = sorted(recommended_scores.items(), key=lambda x: x[1], reverse=True)
        for product_id, score in sorted_recommendations[:context.limit]:
            # Normalize the final score to the range [0, 1]
            max_score = max(recommended_scores.values(), default=1)
            normalized_score = score / max_score if max_score != 0 else 0
            recommendations.append(
                RecommendationModel(product_id=product_id, similarity_score=normalized_score)
            )

        return recommendations
