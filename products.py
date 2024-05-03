import os
from flask import request
from sqlalchemy.sql import text
from db import db


def products():
    sql = text("SELECT id, name, price FROM products")
    result = db.session.execute(sql)
    products = result.fetchall()
    return products


def product(product_id):
    sql = text("SELECT name, price, description FROM products WHERE id=:id")
    result = db.session.execute(sql, {"id": product_id})
    product = result.fetchone()
    return product


def result():
    query = request.args["query"]
    sql = text("SELECT id, name, price FROM products WHERE name ILIKE :query")
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    results = result.fetchall()
    return results


def new(name, price, description, file):
    sql = text(
        """INSERT INTO products (name, price, description)
               VALUES (:name, :price, :description)"""
    )
    db.session.execute(sql, {"name": name, "price": price, "description": description})
    db.session.commit()
    filename = (
        str(db.session.execute(text("SELECT MAX(id) FROM products")).fetchone()[0])
        + ".jpg"
    )
    file.save(os.path.join("static/images", filename))


def review(product_id, username, rating, content):
    sql = text(
        """INSERT INTO reviews (product_id, username, rating, content, created_at)
               VALUES (:product_id, :username, :rating, :content, NOW())"""
    )
    db.session.execute(
        sql,
        {
            "product_id": product_id,
            "username": username,
            "rating": rating,
            "content": content,
        },
    )
    db.session.commit()


def get_reviews(product_id):
    sql = text(
        """SELECT username, rating, content,
               TO_CHAR(created_at, 'DD-MM-YYYY HH24:MI') as created_at
               FROM reviews WHERE product_id=:product_id ORDER BY created_at DESC"""
    )
    result = db.session.execute(sql, {"product_id": product_id})
    reviews = result.fetchall()
    return reviews
