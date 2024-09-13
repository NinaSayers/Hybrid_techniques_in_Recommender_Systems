# app/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base class for declarative models
Base = declarative_base()

class Customer(Base):
    """
    Represents a customer in the system.

    Attributes:
        customer_id (int): Unique identifier for the customer.
        age (int): Age of the customer.
        gender (str): Gender of the customer.
        item_purchased (str): Description of the item purchased.
        category (str): Category of the item purchased.
        purchase_amount_usd (str): Amount of purchase in USD.
        location (str): Location of the customer.
        size (str): Size preference of the customer.
        color (str): Color preference of the customer.
        season (str): Season of the purchase.
        review_rating (str): Rating given by the customer.
        subscription_status (str): Subscription status of the customer.
        shipping_type (str): Shipping method used.
        discount_applied (str): Discount applied to the purchase.
        promo_code_used (str): Promo code used for the purchase.
        previous_purchases (str): Details of previous purchases.
        payment_method (str): Method of payment used.
        frequency_of_purchases (str): Frequency of purchases made by the customer.

    Relationships:
        interactions (relationship): Link to the interactions related to the customer.
    """
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer)
    gender = Column(String)
    item_purchased = Column(Text)
    category = Column(Text)
    purchase_amount_usd = Column(Text)
    location = Column(Text)
    size = Column(Text)
    color = Column(Text)
    season = Column(Text)
    review_rating = Column(Text)
    subscription_status = Column(Text)
    shipping_type = Column(Text)
    discount_applied = Column(Text)
    promo_code_used = Column(Text)
    previous_purchases = Column(Text)
    payment_method = Column(Text)
    frequency_of_purchases = Column(Text)

    interactions = relationship('Interaction', back_populates='customer')


class Product(Base):
    """
    Represents a product in the system.

    Attributes:
        unique_id (str): Unique identifier for the product.
        product_name (str): Name of the product.
        brand_name (str): Brand of the product.
        asin (str): Amazon Standard Identification Number.
        category (str): Category of the product.
        upc_ean_code (str): UPC or EAN code of the product.
        list_price (str): List price of the product.
        selling_price (str): Selling price of the product.
        quantity (int): Quantity of the product available.
        model_number (str): Model number of the product.
        about_product (str): Description of the product.
        product_specification (str): Product specifications.
        technical_details (str): Technical details of the product.
        shipping_weight (str): Shipping weight of the product.
        product_dimensions (str): Dimensions of the product.
        image (str): URL of the product image.
        variants (str): Variants of the product.
        sku (str): Stock Keeping Unit identifier.
        product_url (str): URL of the product page.
        stock (int): Number of items in stock.
        product_details (str): Additional details about the product.
        dimensions (str): Dimensions of the product.
        color (str): Color of the product.
        ingredients (str): Ingredients of the product (if applicable).
        direction_to_use (str): Instructions for using the product.
        is_amazon_seller (bool): Indicates if the product is sold by Amazon.
        size_quantity_variant (str): Size and quantity variant of the product.
        product_description (str): Detailed description of the product.

    Relationships:
        interactions (relationship): Link to the interactions related to the product.
    """
    __tablename__ = 'products'
    
    unique_id = Column(String, primary_key=True)
    product_name = Column(Text)
    brand_name = Column(Text)
    asin = Column(Text)
    category = Column(Text)
    upc_ean_code = Column(Text)
    list_price = Column(Text)
    selling_price = Column(Text)
    quantity = Column(Integer)
    model_number = Column(Text)
    about_product = Column(Text)
    product_specification = Column(Text)
    technical_details = Column(Text)
    shipping_weight = Column(Text)
    product_dimensions = Column(Text)
    image = Column(Text)
    variants = Column(Text)
    sku = Column(Text)
    product_url = Column(Text)
    stock = Column(Integer)
    product_details = Column(Text)
    dimensions = Column(Text)
    color = Column(Text)
    ingredients = Column(Text)
    direction_to_use = Column(Text)
    is_amazon_seller = Column(Boolean)
    size_quantity_variant = Column(Text)
    product_description = Column(Text)

    interactions = relationship('Interaction', back_populates='product')

    def getProductDescribed(self):
        """
        Returns a descriptive string for the product.

        Returns:
            str: A formatted string containing product details.
        """
        return f"{self.product_name}  {self.about_product} {self.category} {self.brand_name} {self.product_specification}"


class Interaction(Base):
    """
    Represents an interaction between a customer and a product.

    Attributes:
        user_id (int): ID of the customer involved in the interaction.
        product_id (str): ID of the product involved in the interaction.
        interaction_type (str): Type of interaction (e.g., view, purchase).
        time_stamp (datetime): Timestamp of the interaction.
        description (str): Optional description of the interaction.

    Relationships:
        customer (relationship): Link to the customer involved in the interaction.
        product (relationship): Link to the product involved in the interaction.
    """
    __tablename__ = 'interactions'
    
    user_id = Column(Integer, ForeignKey('customers.customer_id'), primary_key=True)
    product_id = Column(String, ForeignKey('products.unique_id'), primary_key=True)
    interaction_type = Column(Text)
    time_stamp = Column(DateTime)
    description = Column(Text)

    customer = relationship('Customer', back_populates='interactions')
    product = relationship('Product', back_populates='interactions')
