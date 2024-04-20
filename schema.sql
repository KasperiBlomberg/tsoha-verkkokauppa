CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    role INTEGER,
    password TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT,
    price NUMERIC
);

CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES carts(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    username TEXT,
    rating INTEGER,
    content TEXT,
    created_at TIMESTAMP
);