from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from services.logger import Logger
from .models import Customer, Product, Interaction

class BaseRepository:
    """
    Base repository class providing common database operations.

    Attributes:
        logger (Logger): Logger instance for logging operations.
        session (Session): SQLAlchemy session for database operations.
    """
    def __init__(self, session: Session) -> None:
        """
        Initializes the repository with a SQLAlchemy session.

        Args:
            session (Session): SQLAlchemy session object.
        """
        self.logger = Logger()
        self.session = session

    def add(self, entity: object) -> None:
        """
        Adds an entity to the session and commits the transaction.

        Args:
            entity (object): Entity object to be added to the session.
        """
        self.session.add(entity)
        self.session.commit()

    def remove(self, entity: object) -> None:
        """
        Removes an entity from the session and commits the transaction.

        Args:
            entity (object): Entity object to be removed from the session.
        """
        self.session.delete(entity)
        self.session.commit()

    def update(self) -> None:
        """
        Commits the transaction to update the session.
        """
        self.session.commit()

    def get_all(self) -> List[object]:
        """
        Retrieves all entities of a specific type from the database.

        Returns:
            List[object]: List of entities.

        Raises:
            NotImplementedError: This method should be implemented in derived classes.
        """
        raise NotImplementedError

    def get_by_id(self, entity_id: int) -> Optional[object]:
        """
        Retrieves an entity by its ID from the database.

        Args:
            entity_id (int): ID of the entity to be retrieved.

        Returns:
            Optional[object]: The entity if found, otherwise None.

        Raises:
            NotImplementedError: This method should be implemented in derived classes.
        """
        raise NotImplementedError


class CustomerRepository(BaseRepository):
    """
    Repository class for managing `Customer` entities.
    """
    def get_all(self) -> List[Customer]:
        """
        Retrieves all customers from the database.

        Returns:
            List[Customer]: List of all Customer entities.
        """
        return self.session.query(Customer).all()

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """
        Retrieves a customer by its ID from the database.

        Args:
            customer_id (int): ID of the customer to be retrieved.

        Returns:
            Optional[Customer]: The Customer entity if found, otherwise None.
        """
        return self.session.query(Customer).filter(Customer.customer_id == customer_id).first()


class ProductRepository(BaseRepository):
    """
    Repository class for managing `Product` entities.
    """
    def get_all_paginated(self, page: int = 1, page_size: int = 10) -> List[Product]:
        """
        Retrieves a paginated list of products from the database.

        Args:
            page (int): The page number to retrieve (default is 1).
            page_size (int): Number of products per page (default is 10).

        Returns:
            List[Product]: List of products for the specified page.
        """
        offset = (page - 1) * page_size
        return self.session.query(Product).offset(offset).limit(page_size).all()
    
    def get_all(self) -> List[Product]:
        """
        Retrieves all products from the database.

        Returns:
            List[Product]: List of all Product entities.
        """
        return self.session.query(Product).all()

    def get_by_id(self, unique_id: str) -> Optional[Product]:
        """
        Retrieves a product by its unique ID from the database.

        Args:
            unique_id (str): Unique ID of the product to be retrieved.

        Returns:
            Optional[Product]: The Product entity if found, otherwise None.
        """
        return self.session.query(Product).filter(Product.unique_id == unique_id).first()


class InteractionRepository(BaseRepository):
    """
    Repository class for managing `Interaction` entities.
    """
    def get_all(self) -> List[Interaction]:
        """
        Retrieves all interactions from the database.

        Returns:
            List[Interaction]: List of all Interaction entities.
        """
        return self.session.query(Interaction).all()

    def get_by_user_and_product(self, user_id: int, product_id: str) -> Optional[Interaction]:
        """
        Retrieves an interaction by user ID and product ID from the database.

        Args:
            user_id (int): ID of the user.
            product_id (str): ID of the product.

        Returns:
            Optional[Interaction]: The Interaction entity if found, otherwise None.
        """
        return self.session.query(Interaction).filter(
            Interaction.user_id == user_id,
            Interaction.product_id == product_id
        ).first()
    
    def get_interactions_by_user(self, user_id: int) -> List[Interaction]:
        """
        Retrieves all interactions for a specific user from the database.

        Args:
            user_id (int): ID of the user.

        Returns:
            List[Interaction]: List of interactions for the specified user.
        """
        return self.session.query(Interaction).filter(
            Interaction.user_id == user_id
        ).all()

    def create_interaction(self, user_id: int, product_id: str, interaction_type: str, description: Optional[str] = None) -> None:
        """
        Creates a new interaction and adds it to the session.

        Args:
            user_id (int): ID of the user.
            product_id (str): ID of the product.
            interaction_type (str): Type of interaction.
            description (Optional[str]): Optional description of the interaction.
        """
        new_interaction = Interaction(
            user_id=user_id,
            product_id=product_id,
            interaction_type=interaction_type,
            time_stamp=datetime.now(),
            description=description
        )
        self.add(new_interaction)
