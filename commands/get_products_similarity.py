from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_access.db.db import SessionLocal
from data_access.db.repositories import ProductRepository
from services.logger import Logger

class Similarity: 
    def __init__(self, recommendations): 
        self.recommendations = recommendations 
    
    def get_closest_products(self, product_id, take):
        return self.recommendations[product_id][::-1][:take]



class GetProductSimilarityCommand: 
    def __init__(self): 
        self.logger = Logger()
    def execute(self):
        session = SessionLocal()
        product_repository = ProductRepository(session)

        self.logger.info("Fetching all the products.")
        products = product_repository.get_all()

        product_descriptions = [ product.getProductDescribed() for product in products ]

        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(product_descriptions)

        self.logger.info("Calculating cosine similarity among all the vectors")
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        recommendations = {}

        self.logger.info("Getting recommendations")
        for idx, product in enumerate(products):
            similar_indices = cosine_similarities[idx].argsort()[::-1][1:]
            similar_items = [
                (products[similar_idx].unique_id, cosine_similarities[idx][similar_idx])
                for similar_idx in similar_indices
            ]

            recommendations[product.unique_id] = similar_items

        session.close()

        return Similarity(recommendations)
