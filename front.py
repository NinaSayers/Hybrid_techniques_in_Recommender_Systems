import streamlit as st
from data_access.db.db import SessionLocal
from data_access.db.models import Product, Customer
from data_access.db.repositories import ProductRepository, CustomerRepository, InteractionRepository
from filters.collaborative_filter import CollaborativeFilter
from filters.content_based_filter import ContentBaseFilter
from filters.filter_pipe import FilterPipe
from models.context_model import Context
from services.logger import Logger

# Crear una nueva instancia de la sesión  
session = SessionLocal()
logger = Logger()

def create_product_form():
    st.title("Product Form")

    # Formulario para ingresar los datos del producto
    with st.form("product_form"):
        product_name = st.text_input("Product Name", "")
        brand_name = st.text_input("Brand Name", "")
        asin = st.text_input("ASIN", "")
        category = st.text_input("Category", "")
        upc_ean_code = st.text_input("UPC/EAN Code", "")
        list_price = st.text_input("List Price", "")
        selling_price = st.text_input("Selling Price", "")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        model_number = st.text_input("Model Number", "")
        about_product = st.text_area("About Product", "")
        product_specification = st.text_area("Product Specification", "")
        technical_details = st.text_area("Technical Details", "")
        shipping_weight = st.text_input("Shipping Weight", "")
        product_dimensions = st.text_input("Product Dimensions", "")
        image = st.text_input("Image URL", "")
        variants = st.text_input("Variants", "")
        sku = st.text_input("SKU", "")
        product_url = st.text_input("Product URL", "")
        stock = st.number_input("Stock", min_value=0, step=1)
        product_details = st.text_area("Product Details", "")
        dimensions = st.text_input("Dimensions", "")
        color = st.text_input("Color", "")
        ingredients = st.text_input("Ingredients", "")
        direction_to_use = st.text_area("Direction to Use", "")
        is_amazon_seller = st.checkbox("Is Amazon Seller")
        size_quantity_variant = st.text_input("Size Quantity Variant", "")
        product_description = st.text_area("Product Description", "")

        # Botón para enviar el formulario
        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                # Crear una instancia del repositorio de productos
                product_repository = ProductRepository(session)

                # Crear una nueva instancia de Product
                new_product = Product(
                    product_name=product_name,
                    brand_name=brand_name,
                    asin=asin,
                    category=category,
                    upc_ean_code=upc_ean_code,
                    list_price=list_price,
                    selling_price=selling_price,
                    quantity=quantity,
                    model_number=model_number,
                    about_product=about_product,
                    product_specification=product_specification,
                    technical_details=technical_details,
                    shipping_weight=shipping_weight,
                    product_dimensions=product_dimensions,
                    image=image,
                    variants=variants,
                    sku=sku,
                    product_url=product_url,
                    stock=stock,
                    product_details=product_details,
                    dimensions=dimensions,
                    color=color,
                    ingredients=ingredients,
                    direction_to_use=direction_to_use,
                    is_amazon_seller=is_amazon_seller,
                    size_quantity_variant=size_quantity_variant,
                    product_description=product_description
                )

                # Agregar el producto al repositorio
                product_repository.add(new_product)
                session.commit()  # Guardar los cambios

                logger.info(f"Product successfully created with id: {new_product.unique_id}.")
                st.success("Product successfully created!")
            except Exception as e:
                session.rollback()  # Revertir si algo falla
                logger.error(f"An error occurred while creating the product: {str(e)}")
                st.error(f"An error occurred: {str(e)}")
            finally:
                session.close()  # Cerrar la sesión

def create_customer_form():
    st.title("Customer Form")

    # Formulario para ingresar los datos del usuario
    with st.form("customer_form"):
        age = st.number_input("Age", min_value=0, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        item_purchased = st.text_input("Item Purchased", "")
        category = st.text_input("Category", "")
        purchase_amount_usd = st.text_input("Purchase Amount (USD)", "")
        location = st.text_input("Location", "")
        size = st.text_input("Size", "")
        color = st.text_input("Color", "")
        season = st.text_input("Season", "")
        review_rating = st.text_input("Review Rating", "")
        subscription_status = st.text_input("Subscription Status", "")
        shipping_type = st.text_input("Shipping Type", "")
        discount_applied = st.text_input("Discount Applied", "")
        promo_code_used = st.text_input("Promo Code Used", "")
        previous_purchases = st.text_area("Previous Purchases", "")
        payment_method = st.text_input("Payment Method", "")
        frequency_of_purchases = st.text_input("Frequency of Purchases", "")

        # Botón para enviar el formulario
        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                # Crear una instancia del repositorio de usuarios
                customer_repository = CustomerRepository(session)

                # Crear una nueva instancia de Customer
                new_customer = Customer(
                    age=age,
                    gender=gender,
                    item_purchased=item_purchased,
                    category=category,
                    purchase_amount_usd=purchase_amount_usd,
                    location=location,
                    size=size,
                    color=color,
                    season=season,
                    review_rating=review_rating,
                    subscription_status=subscription_status,
                    shipping_type=shipping_type,
                    discount_applied=discount_applied,
                    promo_code_used=promo_code_used,
                    previous_purchases=previous_purchases,
                    payment_method=payment_method,
                    frequency_of_purchases=frequency_of_purchases
                )

                # Agregar el cliente al repositorio
                customer_repository.add(new_customer)
                session.commit()  # Guardar los cambios

                # Obtener el ID del cliente recién creado
                customer_id = new_customer.customer_id

                logger.info(f"User successfully created with id: {customer_id}")
                st.success(f"Customer successfully created with ID: {customer_id}!")
            except Exception as e:
                session.rollback()  # Revertir si algo falla
                logger.error(f"An error occurred while creating the customer: {str(e)}")
                st.error(f"An error occurred: {str(e)}")
            finally:
                session.close()  # Cerrar la sesión

def show_products(user_id, page=1, page_size=10):
    st.title("Product Recommendations")

    # Crear una instancia del repositorio de productos y el pipeline de filtros
    product_repository = ProductRepository(session)
    interaction_repository = InteractionRepository(session)
    filter_pipe = FilterPipe([
        ContentBaseFilter(session),
        CollaborativeFilter(session)
    ])

    try:
    # Crear una barra de búsqueda para el ID del producto
        search_id = st.text_input("Search for Product by ID")

        if search_id:
            # Buscar un producto específico por ID
            try:
                product_id = str(search_id)
                st.write(f"Searching for product with ID: {product_id}")  # Línea de depuración
                product = product_repository.get_by_id(product_id)
                
                if product:
                    # Mostrar detalles del producto específico
                    st.subheader(product.product_name if product.product_name else "No Name Available")
                    
                    if product.image:
                        st.image(product.image, width=200)  # Imagen del producto (ajustar tamaño si es necesario)
                    else:
                        st.image("path/to/placeholder/image.png", width=200)  # Imagen de placeholder
                    
                    st.write(product.about_product if product.about_product else "No description available.")
                    st.write(f"Price: ${product.selling_price if product.selling_price else 'N/A'}")
                    st.write(f"Stock: {product.stock if product.stock is not None else 'N/A'}")

                    # Botones de interacción
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"Buy {product.product_name}", key=f"buy_{product.unique_id}"):
                            # Acción para comprar
                            logger.info("Buyed")
                            interaction_repository.create_interaction(user_id, product_id, 'purchase', 'User purchased the product')
                            session.commit()
                            st.write(f"Purchased {product.product_name}!")
                    
                    with col2:
                        if st.button(f"Like {product.product_name}", key=f"like_{product.unique_id}"):
                            # Acción para dar like
                            logger.info("Liked")
                            interaction_repository.create_interaction(user_id, product_id, 'like', 'User liked the product')
                            session.commit()
                            st.write(f"Liked {product.product_name}!")
                    
                    with col3:
                        if st.button(f"Details {product.product_name}", key=f"details_{product.unique_id}"):                            
                            logger.info("Viewed")
                            # Acción para ver más detalles
                            interaction_repository.create_interaction(user_id, product_id, 'view', 'User viewed the product')
                            session.commit()
                            st.write(f"More details about {product.product_name}...")
                
                else:
                    st.write("Product not found.")
            except ValueError:
                st.write("Please enter a valid ID.")
            except Exception as e:
                logger.error(f"An error occurred while fetching the product: {str(e)}")
                st.error(f"An error occurred: {str(e)}")
        else:
            # Obtener todos los productos si no hay un ID de búsqueda
            products = product_repository.get_all()
            context = Context(products, user_id, page_size)

            # Aplicar filtros de recomendación
            filtered_products = filter_pipe.apply_filters(context)

            if not filtered_products:
                st.write("No products found.")
                return

            st.write(f"Showing product recommendations for user: {user_id}")
            
            first_10 = filtered_products.recommendations[:10]
            for rec in first_10:
                product = product_repository.get_by_id(rec.product_id)
                # Mostrar información del producto como una tarjeta
                with st.container():
                    st.subheader(product.product_name if product.product_name else "No Name Available")
                    
                    if product.image:
                        try: 
                            st.image(product.image, width=200)  # Imagen del producto (ajustar tamaño si es necesario)
                        except: 
                            st.image("https://tse1.mm.bing.net/th?id=OIP.XXWKhZZeWjrUPx-ZSfP0GAHaDt&pid=Api", width=200)  # Imagen de placeholder
                    else:
                        st.image("https://tse1.mm.bing.net/th?id=OIP.XXWKhZZeWjrUPx-ZSfP0GAHaDt&pid=Api", width=200)  # Imagen de placeholder
                    
                    st.write(product.about_product if product.about_product else "No description available.")
                    st.write(f"Product id: {rec.product_id}")
                    st.write(f"Ranking score: {rec.similarity_score if rec.similarity_score is not None else 'N/A'}")
                    st.write(f"Price: ${product.selling_price if product.selling_price else 'N/A'}")
                    st.write(f"Stock: {product.stock if product.stock is not None else 'N/A'}")

                    # Botones de acción para cada producto
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"Buy {product.product_name}", key=f"buy_{product.unique_id}"):
                            # Acción para comprar
                            logger.info("Buyed")
                            interaction_repository.create_interaction(user_id, product.unique_id, 'purchase', 'User purchased the product')
                            session.commit()
                            st.write(f"Purchased {product.product_name}!")
                    
                    with col2:
                        if st.button(f"Like {product.product_name}", key=f"like_{product.unique_id}"):
                            # Acción para dar like
                            logger.info("Liked")
                            interaction_repository.create_interaction(user_id, product.unique_id, 'like', 'User liked the product')
                            session.commit()
                            st.write(f"Liked {product.product_name}!")
                    
                    with col3:
                        if st.button(f"Details {product.product_name}", key=f"details_{product.unique_id}"):
                            # Acción para ver más detalles
                            logger.info("Viwed")
                            interaction_repository.create_interaction(user_id, product.unique_id, 'view', 'User viewed the product')
                            session.commit()
                            st.write(f"More details about {product.product_name}...")

            # Agregar controles de paginación
            col_prev, col_next = st.columns([1, 1])
            
            with col_prev:
                if st.button("Previous Page") and page > 1:
                    show_products(user_id, page - 1, page_size)
            with col_next:
                if st.button("Next Page"):
                    show_products(user_id, page + 1, page_size)

    except Exception as e:
        logger.error(f"An error occurred while fetching products: {str(e)}")
        st.error(f"An error occurred: {str(e)}")
    finally:
        session.close()

def main():
    st.sidebar.title("Navigation")
    user_id = st.sidebar.number_input("Enter User ID", min_value=1, step=1)
    options = st.sidebar.radio("Select a View", ("Create Product", "Create Customer", "Show Products"))

    if options == "Create Product":
        create_product_form()
    elif options == "Show Products":
        show_products(user_id=user_id, page=1, page_size=10)
    elif options == "Create Customer":
        create_customer_form()

if __name__ == "__main__":
    main()
