from typing import List, Tuple
from filters.filter_base import FilterBase, FilterResult, Recommendation
from services.logger import Logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedFiltering(FilterBase):
    def apply_filter(self, products: List) -> List[Recommendation]:
        if not products:
            self.logger.warning("No products provided.")
            return []
        
        product_descriptions = [product.getProductDescribed() for product in products]
        product_ids = [product.unique_id for product in products]

        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(product_descriptions)

        self.logger.info("Calculating cosine similarity among all the vectors")
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

        recommendations = []
        self.logger.info("Getting recommendations")

        for idx, product in enumerate(products):
            similar_indices = cosine_similarities[idx].argsort()[::-1][1:]
            similar_items = [
                (product_ids[similar_idx], cosine_similarities[idx][similar_idx])
                for similar_idx in similar_indices
            ]
            recommendations.append(Recommendation(product.unique_id, similar_items))

        return recommendations


