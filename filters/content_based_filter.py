from abc import ABC
from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from data_access.db.db import SessionLocal
from data_access.db.repositories import InteractionRepository
from filters.filter_base import FilterBase
from models.context_model import Context
from models.filter_result_model import FilterResultModel
from models.recommendation_model import RecommendationModel

class ContentBaseFilter(FilterBase):
    def __init__(self):
        super().__init__()
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    def apply_filter(self, context: Context) -> Optional[FilterResultModel]:
        """Apply content-based filtering to generate product recommendations."""
        if not context.products:
            self.logger.warn("No products provided in context.")
            return None

        if not context.userId:
            self.logger.warn("No user ID provided in context.")
            return None

        self.logger.info(f"Applying content-based filters to {len(context.products)} products, expecting {context.limit} filtered.")

        with SessionLocal() as session:
            interactions_repository = InteractionRepository(session)
            try:
                product_descriptions = self.get_product_descriptions(context.products)
                tfidf_matrix = self.tfidf_vectorizer.fit_transform(product_descriptions)

                user_vector = self.get_user_vector(context.userId, context.products, tfidf_matrix, interactions_repository)
                if user_vector is None:
                    self.logger.warn("No valid user vector found.")
                    return None

                recommendations = self.get_recommendations(context, tfidf_matrix, user_vector, interactions_repository)

                return FilterResultModel(user_id=context.userId, recommendations=recommendations)

            except Exception as e:
                self.logger.error(f"An error occurred while applying the Content-Based filter: {str(e)}")
                return None

    def get_product_descriptions(self, products: List) -> List[str]:
        """Extract descriptions from a list of products."""
        return [product.getProductDescribed() for product in products]

    def get_user_vector(self, user_id: int, products: List, tfidf_matrix: np.ndarray, interactions_repository: InteractionRepository) -> Optional[np.ndarray]:
        """Calculate the user's vector based on their interactions with products."""
        try:
            interaction_weights = []
            product_vectors = []

            user_interactions = interactions_repository.get_interactions_by_user(user_id)
            for interaction in user_interactions:
                product = next((p for p in products if p.unique_id == interaction.product_id), None)
                if product:
                    index = products.index(product)
                    product_vectors.append(tfidf_matrix[index].toarray().flatten())

                    weight = self.get_interaction_weight(interaction.interaction_type)
                    interaction_weights.append(weight)

            if not product_vectors:
                self.logger.warn("No user interactions with the products were found.")
                return None

            user_vector = np.average(product_vectors, axis=0, weights=interaction_weights)
            return user_vector

        except Exception as e:
            self.logger.error(f"An error occurred when trying to get the user vector: {str(e)}")
            return None

    def get_interaction_weight(self, interaction_type: str) -> int:
        """Map interaction types to their corresponding weights."""
        return {
            "view": 2,
            "like": 3,
            "purchase": 5
        }.get(interaction_type, 1)

    def get_recommendations(self, context: Context, tfidf_matrix: np.ndarray, user_vector: np.ndarray, interactions_repository: InteractionRepository) -> List[RecommendationModel]:
        """Generate a list of recommendations based on cosine similarity."""
        cosine_similarities = cosine_similarity([user_vector], tfidf_matrix).flatten()

        interacted_product_ids = {
            interaction.product_id
            for interaction in interactions_repository.get_interactions_by_user(context.userId)
        }

        recommendations = []
        for i in cosine_similarities.argsort()[::-1]:
            if context.products[i].unique_id not in interacted_product_ids:
                recommendations.append(
                    RecommendationModel(
                        product_id=context.products[i].unique_id,
                        similarity_score=cosine_similarities[i]
                    )
                )
            if len(recommendations) >= context.limit:
                break

        return recommendations
