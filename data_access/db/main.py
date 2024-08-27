# # app/main.py
# from .db import SessionLocal
# from .repositories import CustomerRepository, ProductRepository, InteractionRepository

# def initilize():
#     # Crear una sesión
#     session = SessionLocal()

#     # Crear instancias de los repositorios
#     customer_repo = CustomerRepository(session)
#     product_repo = ProductRepository(session)
#     interaction_repo = InteractionRepository(session)

#     # Ejemplos de uso:

#     # Agregar un nuevo cliente
#     nuevo_cliente = Customer(
#         age=30,
#         gender="Male",
#         item_purchased="Laptop",
#         category="Electronics",
#         purchase_amount_usd="1000",
#         location="New York",
#         size="Medium",
#         color="Black",
#         season="Winter",
#         review_rating="5 stars",
#         subscription_status="Active",
#         shipping_type="Express",
#         discount_applied="Yes",
#         promo_code_used="DISCOUNT2024",
#         previous_purchases="3",
#         payment_method="Credit Card",
#         frequency_of_purchases="Monthly"
#     )
#     customer_repo.add(nuevo_cliente)

#     # Obtener todos los clientes
#     clientes = customer_repo.get_all()
#     for cliente in clientes:
#         print(cliente.customer_id, cliente.age, cliente.gender)

# if __name__ == "__main__":
#     main()
