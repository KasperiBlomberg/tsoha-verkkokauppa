from app import app
from flask import redirect, render_template, request, make_response
import users
import products
import carts

@app.route("/")
def index():
    result = products.products()
    return render_template("index.html", products = result)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None, username="")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error=True, username=username)
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", error=None, username="")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(password1) < 3:
            return render_template("register.html", error="Salasanan tulee olla vähintään 3 merkkiä pitkä.", username=username)
        if password1 != password2:
            return render_template("register.html", error="Salasanat eivät täsmää.", username=username)
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", error="Rekisteröinti epäonnistui.", username=username)
        
@app.route("/product/<int:id>")
def product(id):
    product = products.product(id)
    reviews = products.get_reviews(id)
    if reviews:
        average_rating = round(sum(review[1] for review in reviews) / len(reviews), 1)
    else:
        average_rating = None
    return render_template("product.html", id=id, product=product, reviews = reviews, average_rating = average_rating)

@app.route("/result", methods=["GET"])
def result():
    results = products.result()
    return render_template("result.html", results = results)

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        file = request.files["file"]
        products.new(name, price, description, file)
        return redirect("/")
    
@app.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method == "GET":
        cart = carts.get_cart()
        total = sum([float(i[2])*i[3] for i in cart])
        return render_template("cart.html", cart = cart, total = total)
    if request.method == "POST":
        product_id = request.form["product_id"]
        amount = request.form["amount"]
        carts.add_to_cart(product_id, amount)
        return redirect("/cart")
    
@app.route("/review", methods=["POST"])
def review():
    product_id = request.form["product_id"]
    rating = request.form["rating"]
    content = request.form["content"]
    username = users.username()
    products.review(product_id, username, rating, content)
    return redirect("/product/"+product_id)