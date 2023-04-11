from flask import Flask, render_template, flash, session, redirect, url_for
from melons import Melon, get_all, get_by_id
from customers import get_by_username
from forms import LoginForm

app = Flask(__name__)
app.secret_key = 'dev'

@app.route("/")
def homepage():
    return render_template("base.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if user exists and password is correct
        user = get_by_username(username)
        if user and user['password'] == password:
            session["username"] = username
            flash("Login successful")
            return redirect(url_for("list_melons"))
        else:
            flash("Invalid username or password")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    if "username" in session:
        del session["username"]
        flash("You have logged out")
    return redirect(url_for("login"))

@app.route('/melons')
def list_melons():
    all_melons = get_all()
    return render_template('all_melons.html', melons=all_melons, int=int)

@app.route("/melons/<melon_id>")
def show_melon(melon_id):
    melon = get_by_id(melon_id)
    return render_template("melon_details.html", melon=melon)

@app.route("/cart")
def show_shopping_cart():
    if "username" not in session:
        flash("Please log in to view your shopping cart")
        return redirect(url_for("login"))
    order_total = 0
    cart_melons = []

    cart = session.get("cart", {})

    for melon_id, qty in cart.items():
        melon = get_by_id(melon_id)
        total_cost = melon.price * qty
        order_total += total_cost

        melon.quantity = qty
        melon.total_cost = total_cost
        cart_melons.append(melon)

    return render_template("cart.html", cart_melons=cart_melons, order_total=order_total)

@app.route("/add-to-cart/<melon_id>")
def add_to_cart(melon_id):
    if "username" not in session:
        flash("Please log in to add items to your shopping cart")
        return redirect(url_for("login"))
    if 'cart' not in session:
        session['cart'] = {}

    session['cart'][str(melon_id)] = session['cart'].get(str(melon_id), 0) + 1
    session.modified = True

    flash(f"Melon {melon_id} successfully added to cart.")
    return redirect(url_for("show_shopping_cart"))

@app.route("/empty-cart")
def empty_cart():
    session['cart'] = {}
    session.modified = True
    return redirect(url_for("show_shopping_cart"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
   app.env = "development"
   app.run(debug=True, port=8000, host="localhost")