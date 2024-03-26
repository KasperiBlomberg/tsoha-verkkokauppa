CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    role INTEGER,
    password TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    genre INTEGER REFERENCES genres(id),
    price TEXT
);

CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    data BYTEA
);

CREATE TABLE descriptions (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    data TEXT
);