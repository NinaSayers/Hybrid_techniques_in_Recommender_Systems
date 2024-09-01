SET datestyle = 'DMY, ISO';

CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,  
    age INTEGER,
    gender TEXT,
    item_purchased TEXT,
    category TEXT,
    purchase_amount_usd TEXT,
    location TEXT,
    size TEXT,
    color TEXT,
    season TEXT,
    review_rating TEXT,
    subscription_status TEXT,
    shipping_type TEXT,
    discount_applied TEXT,
    promo_code_used TEXT,
    previous_purchases TEXT,
    payment_method TEXT,
    frequency_of_purchases TEXT
);

CREATE TABLE IF NOT EXISTS products (
    unique_id TEXT PRIMARY KEY,
    product_name TEXT,
    brand_name TEXT,
    asin TEXT,
    category TEXT,
    upc_ean_code TEXT,
    list_price TEXT,
    selling_price TEXT,
    quantity INTEGER,
    model_number TEXT,
    about_product TEXT,
    product_specification TEXT,
    technical_details TEXT,
    shipping_weight TEXT,
    product_dimensions TEXT,
    image TEXT,
    variants TEXT,
    sku TEXT,
    product_url TEXT,
    stock INTEGER,
    product_details TEXT,
    dimensions TEXT,
    color TEXT,
    ingredients TEXT,
    direction_to_use TEXT,
    is_amazon_seller BOOLEAN,
    size_quantity_variant TEXT,
    product_description TEXT
);

CREATE TABLE IF NOT EXISTS interactions (
    user_id INTEGER,
    product_id TEXT,
    interaction_type TEXT,
    time_stamp TIMESTAMP,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(unique_id)
);

COPY customers (customer_id, age, gender, item_purchased, category, purchase_amount_usd, location, size, color, season, review_rating, subscription_status, shipping_type, discount_applied, promo_code_used, previous_purchases, payment_method, frequency_of_purchases)
FROM '/docker-entrypoint-initdb.d/customer_details.csv'
DELIMITER ','
CSV HEADER;

COPY products (unique_id, product_name, brand_name, asin, category, upc_ean_code, list_price, selling_price, quantity, model_number, about_product, product_specification, technical_details, shipping_weight, product_dimensions, image, variants, sku, product_url, stock, product_details, dimensions, color, ingredients, direction_to_use, is_amazon_seller, size_quantity_variant, product_description)
FROM '/docker-entrypoint-initdb.d/product_details.csv'
DELIMITER ','
CSV HEADER;

COPY interactions (user_id, product_id, interaction_type, time_stamp)
FROM '/docker-entrypoint-initdb.d/interactions_details.csv'
DELIMITER ','
CSV HEADER;

-- Sincronizando la llave autoincremental de la tabla customer 
DO $$ 
DECLARE sequence_name text;
BEGIN
    sequence_name := (SELECT pg_get_serial_sequence('customers', 'customer_id'));

    EXECUTE format('SELECT setval(%L, (SELECT COALESCE(MAX(customer_id), 0) + 1 FROM customers))', sequence_name);
END $$;
