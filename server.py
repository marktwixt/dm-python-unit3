from flask import Flask, render_template, flash, session, redirect, url_for
from melons import Melon, get_all, get_by_id

app = Flask(__name__)
app.secret_key = 'dev'

@app.route("/")
def homepage():
    return render_template("base.html")

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

if __name__ == "__main__":
   app.env = "development"
   app.run(debug=True, port=8000, host="localhost")