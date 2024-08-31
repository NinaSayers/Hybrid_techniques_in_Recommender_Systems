from abc import ABC
from typing import List
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

    def apply_filter(self, context: Context) -> FilterResultModel:
        session = SessionLocal()
        interactions_repository = InteractionRepository(session)
        self.logger.info("Applying content based filters")
        try:
            product_descriptions = [product.getProductDescribed() for product in context.products]

            tfidf_matrix = self.tfidf_vectorizer.fit_transform(product_descriptions)

            user_vector = self.get_user_vector(context.userId, context.products, tfidf_matrix)
            if user_vector is None:
                self.logger.info("No valid user vector found.")
                return []

            cosine_similarities = cosine_similarity([user_vector], tfidf_matrix).flatten()

            interacted_product_ids = {interaction.product_id for interaction in interactions_repository.get_interactions_by_user(context.userId)}
            recommendations = []
            for i in cosine_similarities.argsort()[::-1]:
                if context.products[i].unique_id not in interacted_product_ids:
                    recommendation = RecommendationModel(
                        product_id=context.products[i].unique_id,
                        similarity_score=cosine_similarities[i]
                    )
                    recommendations.append(recommendation)
                if len(recommendations) >= context.limit: 
                    break

            # Create the FilterResultModel with the list of recommendations
            filter_result = FilterResultModel(
                user_id=context.userId,
                recommendations=recommendations
            )

            return filter_result

        except Exception as e:
            self.logger.error(f"An error occurred while applying the Content Based filter: {str(e)}")
            return []
        finally:
            session.close()

    def get_user_vector(self, user_id, products, tfidf_matrix):
        session = SessionLocal()
        interactions_repository = InteractionRepository(session)
        try:
            interaction_weights = []
            product_vectors = []
            user_interactions = interactions_repository.get_interactions_by_user(user_id)
            for interaction in user_interactions:
                product = next((p for p in products if p.unique_id == interaction.product_id), None)
                if product:
                    index = products.index(product)
                    product_vectors.append(tfidf_matrix[index].toarray().flatten())
                    switcher = {
                        "view": 2,
                        "like": 3,
                        "purchase": 5
                    }
                    weight = switcher.get(interaction.interaction_type, 1)
                    interaction_weights.append(weight)

            if not product_vectors:
                self.logger.warn("No user interactions with the products were found.")
                return None

            user_vector = np.average(product_vectors, axis=0, weights=interaction_weights)
            return user_vector

        except Exception as e:
            self.logger.error(f"An error occurred when trying to get the user vector: {str(e)}")
            return None

        finally:
            session.close()
