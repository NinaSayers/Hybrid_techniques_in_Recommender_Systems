from typing import List, Optional
from sqlalchemy.orm import Session

from services.logger import Logger
from .models import Customer, Product, Interaction

class BaseRepository:
    def __init__(self, session: Session) -> None:
        self.logger = Logger()
        self.session = session

    def add(self, entity: object) -> None:
        self.session.add(entity)
        self.session.commit()

    def remove(self, entity: object) -> None:
        self.session.delete(entity)
        self.session.commit()

    def update(self) -> None:
        self.session.commit()

    def get_all(self) -> List[object]:
        raise NotImplementedError

    def get_by_id(self, entity_id: int) -> Optional[object]:
        raise NotImplementedError


class CustomerRepository(BaseRepository):
    def get_all(self) -> List[Customer]:
        return self.session.query(Customer).all()

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.session.query(Customer).filter(Customer.customer_id == customer_id).first()


class ProductRepository(BaseRepository):
    def get_all_paginated(self, page: int = 1, page_size: int = 10) -> List[Product]:
        offset = (page - 1) * page_size
        return self.session.query(Product).offset(offset).limit(page_size).all()
    
    def get_all(self) -> List[Product]:
        return self.session.query(Product).all()

    def get_by_id(self, unique_id: str) -> Optional[Product]:
        return self.session.query(Product).filter(Product.unique_id == unique_id).first()


class InteractionRepository(BaseRepository):
    def get_all(self) -> List[Interaction]:
        return self.session.query(Interaction).all()

    def get_by_user_and_product(self, user_id: int, product_id: str) -> Optional[Interaction]:
        return self.session.query(Interaction).filter(
            Interaction.user_id == user_id,
            Interaction.product_id == product_id
        ).first()
    
    def get_interactions_by_user(self, user_id: int) -> Optional[Interaction]:
        return self.session.query(Interaction).filter(
            Interaction.user_id == user_id
        ).all()