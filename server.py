from flask import Flask, render_template, redirect, flash, request
import jinja2
import melons
from melons import get_all, get_by_id  # Import functions from melons.py

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined  # for debugging purposes

### Flask Routes ###
@app.route("/")
def homepage():
   return render_template("base.html")

@app.route("/melons")
def all_melons():
    """Return a page listing all the melons available for purchase."""

    melon_list = get_all()  # Call the get_all function to retrieve the list of melons
    return render_template("all_melons.html", melon_list=melon_list)

@app.route("/melon/<melon_id>")
def melon_details(melon_id):
   """Return a page showing all info about a melon. Also, provide a button to buy that melon."""

   melon = get_by_id(melon_id)
   return render_template("melon_details.html", melon=melon)

@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
   """Add a melon to the shopping cart."""

   return f"{melon_id} added to cart"

@app.route("/cart")
def show_shopping_cart():
   """Display contents of shopping cart."""

   # Need a function that returns cart items and total price
   # cart_items = get_cart_items()
   # total_price = get_total_price()

   # If not, you can use dummy data for now:
   cart_items = []
   total_price = 0.0

   return render_template("cart.html", cart_items=cart_items, total_price=total_price)

if __name__ == "__main__":
   app.env = "development"
   app.run(debug=True, port=8000, host="localhost")