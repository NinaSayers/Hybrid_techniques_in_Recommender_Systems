from typing import List
from data_access.db.models import Product

class Context:
    def __init__(self, products: List[Product], userId: str):
        self.products = products
        self.userId = userId
