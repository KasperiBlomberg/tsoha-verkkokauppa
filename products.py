from db import db
from flask import request
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

def result():
    query = request.args["query"]
    sql = text("SELECT id, name, price FROM products WHERE name LIKE :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    results = result.fetchall()
    return results