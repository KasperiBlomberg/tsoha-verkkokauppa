from flask import session
from sqlalchemy.sql import text
from db import db

def add_to_cart(product_id, amount):
    # If amount is 0, remove product from cart
    if amount == "0":
        remove_from_cart(product_id)
        return
    # If amount is -1, empty cart
    if amount == "-1":
        empty_cart()
        return
    # Check if user has a cart
    sql = text("SELECT id FROM carts WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":session["user_id"]})
    cart_id = result.fetchone()
    # If user doesn't have a cart, create one
    if not cart_id:
        sql_insert_cart = text("INSERT INTO carts (user_id) VALUES (:user_id)")
        db.session.execute(sql_insert_cart, {"user_id":session["user_id"]})
        db.session.commit()
        result = db.session.execute(sql, {"user_id":session["user_id"]})
        cart_id = result.fetchone()
    # Check if product is already in cart
    sql = text("SELECT quantity FROM cart_items WHERE cart_id=:cart_id AND product_id=:product_id")
    result = db.session.execute(sql, {"cart_id":cart_id[0], "product_id":product_id})
    product = result.fetchone()
    # If product is in cart, update amount
    if product:
        new_amount = product[0] + int(amount)
        sql = text("""UPDATE cart_items SET quantity=:new_amount
                   WHERE cart_id=:cart_id AND product_id=:product_id""")
        db.session.execute(sql, {"new_amount":new_amount, "cart_id":cart_id[0], \
                                  "product_id":product_id})
        db.session.commit()
    # If product is not in cart, add it
    else:
        sql = text("""INSERT INTO cart_items (cart_id, product_id, quantity)
                   VALUES (:cart_id, :product_id, :amount)""")
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
    sql = text("""DELETE FROM cart_items
            WHERE cart_id=(SELECT id FROM carts WHERE user_id=:user_id)
            AND product_id=:product_id""")
    db.session.execute(sql, {"user_id":session["user_id"], "product_id":product_id})
    db.session.commit()

def empty_cart():
    sql = text("DELETE FROM cart_items WHERE cart_id=(SELECT id FROM carts WHERE user_id=:user_id)")
    db.session.execute(sql, {"user_id":session["user_id"]})
    db.session.commit()
