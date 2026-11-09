import flask
import sqlite3

app = flask.Flask(__name__)

@app.route("/")
def spisok():
    shop = sqlite3.connect("shop.db")
    rows = shop.execute("SELECT name, price FROM products").fetchall()
    result = ""
    for row in rows:
        result = result + row[0] + ", " + str(row[1]) + " руб<br>"
    return result

@app.route("/search")
def search():
    word = flask.request.args.get("q")
    shop = sqlite3.connect("shop.db")
    rows = shop.execute("SELECT name, price FROM products WHERE name LIKE '%" + word + "%'").fetchall()
    result = ""
    for row in rows:
        result = result + row[0] + ", " + str(row[1]) + " руб<br>"
    return result

@app.route("/product")
def product_page():
    product_id = flask.request.args.get("id")
    new_review = flask.request.args.get("review")
    page = sqlite3.connect("shop.db")
    if new_review:
        page.execute("INSERT INTO reviews (product_id, text) VALUES (" + product_id + ", '" + new_review + "')")
        page.commit()        
    product_rows = page.execute("SELECT name, price FROM products WHERE id = " + product_id).fetchall()
    review_rows = page.execute("SELECT text FROM reviews WHERE product_id = " + product_id).fetchall()
    result = product_rows[0][0] + ", " + str(product_rows[0][1]) + " руб<br>"
    for row in review_rows:
        result = result + row[0] + "<br>"
    return result
    
app.run(port=5001)