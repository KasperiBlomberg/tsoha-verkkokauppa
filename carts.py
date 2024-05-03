from flask import session
from sqlalchemy.sql import text
from db import db


def get_cart_id():
    sql = text("SELECT id FROM carts WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id": session["user_id"]})
    cart_id = result.fetchone()
    return cart_id[0] if cart_id else None


def create_cart():
    sql = text("INSERT INTO carts (user_id) VALUES (:user_id)")
    db.session.execute(sql, {"user_id": session["user_id"]})
    db.session.commit()


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
    cart_id = get_cart_id()
    # If user doesn't have a cart, create one
    if not cart_id:
        create_cart()
        cart_id = get_cart_id()
    # Check if product is already in cart
    product = get_product_in_cart(cart_id, product_id)
    # If product is in cart, update amount
    if product:
        update_product_in_cart(product[0] + int(amount), cart_id, product_id)
    # If product is not in cart, add it
    else:
        insert_product_into_cart(cart_id, product_id, amount)


def get_product_in_cart(cart_id, product_id):
    sql = text(
        "SELECT quantity FROM cart_items WHERE cart_id=:cart_id AND product_id=:product_id"
    )
    result = db.session.execute(sql, {"cart_id": cart_id, "product_id": product_id})
    return result.fetchone()


def update_product_in_cart(new_amount, cart_id, product_id):
    sql = text(
        """UPDATE cart_items SET quantity=:new_amount
                   WHERE cart_id=:cart_id AND product_id=:product_id"""
    )
    db.session.execute(
        sql,
        {"new_amount": new_amount, "cart_id": cart_id, "product_id": product_id},
    )
    db.session.commit()


def insert_product_into_cart(cart_id, product_id, amount):
    sql = text(
        """INSERT INTO cart_items (cart_id, product_id, quantity)
                   VALUES (:cart_id, :product_id, :amount)"""
    )
    db.session.execute(
        sql, {"cart_id": cart_id, "product_id": product_id, "amount": amount}
    )
    db.session.commit()


def get_cart():
    sql = text(
        """SELECT products.id, products.name, products.price, cart_items.quantity,
             SUM(products.price * cart_items.quantity) OVER () AS total
             FROM products
             JOIN cart_items ON products.id=cart_items.product_id
             JOIN carts ON cart_items.cart_id=carts.id
             WHERE carts.user_id=:user_id"""
    )
    result = db.session.execute(sql, {"user_id": session["user_id"]})
    cart = result.fetchall()
    return cart


def remove_from_cart(product_id):
    sql = text(
        """DELETE FROM cart_items
            WHERE cart_id=(SELECT id FROM carts WHERE user_id=:user_id)
            AND product_id=:product_id"""
    )
    db.session.execute(sql, {"user_id": session["user_id"], "product_id": product_id})
    db.session.commit()


def empty_cart():
    sql = text(
        "DELETE FROM cart_items WHERE cart_id=(SELECT id FROM carts WHERE user_id=:user_id)"
    )
    db.session.execute(sql, {"user_id": session["user_id"]})
    db.session.commit()
