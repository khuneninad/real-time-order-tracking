CREATE DATABASE orders_db;
USE orders_db;

CREATE TABLE fact_orders (
    order_id INT,
    customer VARCHAR(100),
    location VARCHAR(100),
    status VARCHAR(50),
    timestamp VARCHAR(50),
    price_factor DOUBLE,
    weather VARCHAR(50),
    delay INT
);