import secrets
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = text("SELECT id, role, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        session["user_id"] = user[0]
        session["user_role"] = user[1]
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False

def logout():
    del session["username"]
    del session["user_role"]
    del session["csrf_token"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, role, password) VALUES (:username, 0, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def username():
    return session.get("username", 0)
