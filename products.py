from db import db
from flask import session
from sqlalchemy.sql import text

def products():
    sql = text("SELECT * FROM products")
    result = db.session.execute(sql)
    products = result.fetchall()
    return products

def product(id):
    sql = text("SELECT name, price FROM products WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    product = result.fetchone()
    return product