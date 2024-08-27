# app/repositories.py
from .models import Customer, Product, Interaction

class BaseRepository:
    def __init__(self, session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def remove(self, entity):
        self.session.delete(entity)
        self.session.commit()

    def update(self):
        self.session.commit()

    def get_all(self):
        raise NotImplementedError

    def get_by_id(self, entity_id):
        raise NotImplementedError


class CustomerRepository(BaseRepository):
    def get_all(self):
        return self.session.query(Customer).all()

    def get_by_id(self, customer_id):
        return self.session.query(Customer).filter(Customer.customer_id == customer_id).first()


class ProductRepository(BaseRepository):
    def get_all(self):
        return self.session.query(Product).all()

    def get_by_id(self, unique_id):
        return self.session.query(Product).filter(Product.unique_id == unique_id).first()


class InteractionRepository(BaseRepository):
    def get_all(self):
        return self.session.query(Interaction).all()

    def get_by_user_and_product(self, user_id, product_id):
        return self.session.query(Interaction).filter(
            Interaction.user_id == user_id,
            Interaction.product_id == product_id
        ).first()
