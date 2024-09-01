from typing import List
from data_access.db.models import Product

class Context:
    def __init__(self, products: List[Product], userId: int, limit=10):
        self.products = products
        self.userId = userId
        self.limit = limit
