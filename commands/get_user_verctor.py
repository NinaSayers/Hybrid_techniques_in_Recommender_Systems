from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from data_access.db.db import SessionLocal
from data_access.db.repositories import ProductRepository, InteractionRepository
from services.logger import Logger

class GetUserVectorCommand:
    def __init__(self):
        self.logger = Logger()

    def get_user_vector(self, user_id, tfidf_vectorizer):
        session = SessionLocal()
        try:
            product_repository = ProductRepository(session)
            interaction_repository = InteractionRepository(session)

            # Fetch all products the user has interacted with
            interactions = interaction_repository.get_interactions_by_user(user_id)
            
            # Get product descriptions and interaction weights
            product_descriptions = []
            interaction_weights = []
            for interaction in interactions:
                product = product_repository.get_by_id(interaction.product_id)
                if product:
                    product_descriptions.append(product.getProductDescribed())
                    switcher = {
                        "view": 2,
                        "like": 3,
                        "purchase": 5
                    }
                    weight = switcher.get(interaction.interaction_type, 1)
                    interaction_weights.append(weight)

            if not product_descriptions:
                self.logger.info("No product descriptions found for user interactions.")
                return None

            # Vectorize the product descriptions using the provided vectorizer
            tfidf_matrix = tfidf_vectorizer.transform(product_descriptions)

            if len(interaction_weights) != tfidf_matrix.shape[0]:
                self.logger.error("Mismatch in the number of interaction weights and product descriptions.")
                return None

            # Compute the user vector as a weighted sum of product vectors
            user_vector = np.average(tfidf_matrix.toarray(), axis=0, weights=interaction_weights)
            return user_vector
        except Exception as e:
            self.logger.error(f"An error occurred while getting the user vector: {str(e)}")
            return None
        finally:
            session.close()

    def recommend_products(self, user_id, top_n=5):
        session = SessionLocal()
        try:
            product_repository = ProductRepository(session)
            interaction_repository = InteractionRepository(session)
            
            # Get all products
            products = product_repository.get_all()
            product_descriptions = [product.getProductDescribed() for product in products]

            # Initialize the TF-IDF vectorizer and fit it on all product descriptions
            tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(product_descriptions)

            # Get the user vector using the same vectorizer
            user_vector = self.get_user_vector(user_id, tfidf_vectorizer)
            if user_vector is None:
                self.logger.info("No valid user vector found.")
                return []

            # Calculate cosine similarity between the user vector and all product vectors
            cosine_similarities = cosine_similarity([user_vector], tfidf_matrix).flatten()

            # Fetch all products the user has interacted with
            user_interactions = interaction_repository.get_interactions_by_user(user_id)
            interacted_product_ids = {interaction.product_id for interaction in user_interactions}

            # Filter out products the user has already interacted with
            recommended_products = []
            for i in cosine_similarities.argsort()[::-1]:
                if products[i].unique_id not in interacted_product_ids:
                    recommended_products.append((products[i].unique_id, cosine_similarities[i]))
                if len(recommended_products) >= top_n:
                    break

            return recommended_products
        except Exception as e:
            self.logger.error(f"An error occurred while recommending products: {str(e)}")
            return []
        finally:
            session.close()
