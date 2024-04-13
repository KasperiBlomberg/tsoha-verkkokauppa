from db import db
from flask import session
from sqlalchemy.sql import text

def add_to_cart(product_id, amount):
    sql = text("SELECT id FROM carts WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":session["user_id"]})
    cart_id = result.fetchone()
    if not cart_id:
        sql_insert_cart = text("INSERT INTO carts (user_id) VALUES (:user_id)")
        db.session.execute(sql_insert_cart, {"user_id":session["user_id"]})
        db.session.commit()
        result = db.session.execute(sql, {"user_id":session["user_id"]})
        cart_id = result.fetchone()
    sql = text("INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (:cart_id, :product_id, :amount)")
    db.session.execute(sql, {"cart_id":cart_id[0], "product_id":product_id, "amount":amount})
    db.session.commit()

def get_cart():
    sql = text("""SELECT products.id, products.name, products.price, cart_items.quantity
            FROM products, cart_items, carts 
            WHERE products.id=cart_items.product_id
            AND cart_items.cart_id=carts.id AND carts.user_id=:user_id""")
    result = db.session.execute(sql, {"user_id":session["user_id"]})
    cart = result.fetchall()
    return cart

def remove_from_cart(product_id):
    pass
    # TODO

def empty_cart():
    pass
    # TODO