from typing import List, Dict
from data_access.db.db import SessionLocal
from data_access.db.repositories import ProductRepository
from filters.filter_base import FilterBase
from models.context_model import Context
from models.filter_result_model import FilterResultModel
from models.recommendation_model import RecommendationModel
from services.logger import Logger

class FilterPipe:
    def __init__(self, filters: List[FilterBase]):
        self.logger = Logger()
        self.filters = filters

    def apply_filters(self, context: Context) -> FilterResultModel:
        """Apply filters using the context and return a FilterResultModel with combined scores."""
        self.logger.info("Applying filters in sequence.")
        filtered_products = context.products
        product_scores: Dict[str, List[float]] = {}

        with SessionLocal() as session: 
            product_repo = ProductRepository(session)
            
            for filter in self.filters:
                self.logger.info(f"Applying filter: {filter.__class__.__name__}")            
                context.products = filtered_products
                
                # Apply the filter
                filter_result = filter.apply_filter(context)
                
                # Check if the filter result is valid
                if not filter_result or not filter_result.recommendations:
                    self.logger.warn(f"No recommendations from filter: {filter.__class__.__name__}")
                    return FilterResultModel(user_id=context.userId, recommendations=[RecommendationModel(x.unique_id,1) for x in filtered_products])

                # Update the scores for the filtered products
                for rec in filter_result.recommendations:
                    product_id = rec.product_id
                    score = rec.similarity_score
                    
                    if product_id in product_scores:
                        product_scores[product_id].append(score)
                    else:
                        product_scores[product_id] = [score]

                # Update the list of filtered products with the results from the current filter
                filtered_products = [product_repo.get_by_id(rec.product_id) for rec in filter_result.recommendations]

        # Convert the product_scores to RecommendationModel with combined scores
        final_recommendations = []
        for product_id, scores in product_scores.items():
            combined_score = sum(scores) / len(scores)  # Example: average of the scores
            final_recommendations.append(
                RecommendationModel(product_id=product_id, similarity_score=combined_score)
            )

        # Sort recommendations by score in descending order
        final_recommendations.sort(key=lambda x: x.similarity_score, reverse=True)

        return FilterResultModel(user_id=context.userId, recommendations=final_recommendations)
