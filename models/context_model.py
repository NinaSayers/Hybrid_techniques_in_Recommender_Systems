from typing import List
from data_access.db.models import Product

class Context:
    def __init__(self, products: List[Product], userId: int, limit=10):
        """
        Initializes the Context with products, user ID, and a limit.

        Args:
            products (List[Product]): A list of Product instances that the filters will operate on.
            userId (int): The ID of the user for whom recommendations are being generated.
            limit (int, optional): The maximum number of recommendations to return. Defaults to 10.
        """
        self.products = products
        self.userId = userId
        self.limit = limit
