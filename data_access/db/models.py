# app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True,autoincrement=True)
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
        return f"{self.category} {self.brand_name} {self.product_name} {self.product_specification}"


class Interaction(Base):
    __tablename__ = 'interactions'
    user_id = Column(Integer, ForeignKey('customers.customer_id'), primary_key=True)
    product_id = Column(String, ForeignKey('products.unique_id'), primary_key=True)
    interaction_type = Column(Text)
    time_stamp = Column(DateTime)
    description = Column(Text)

    customer = relationship('Customer', back_populates='interactions')
    product = relationship('Product', back_populates='interactions')
