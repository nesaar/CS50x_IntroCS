import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        passwordcheck = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure password check was submitted
        if not passwordcheck:
            return apology("must provide password", 400)

        # check the user knows their password
        if password != passwordcheck:
            return apology("password must be the same", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?",  username)
        if len(rows) > 0:
            return apology("user already exists", 400)

        password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

        # insert database user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",  username, password)

        return redirect("/")

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute(
        "SELECT stocksymbol, stockname, SUM(sharespurchased) FROM transactions WHERE user_id = ? GROUP BY stocksymbol, stockname",
        session["user_id"])

    for row in rows:
        row['price'] = "%.2f" % round(lookup(row['stocksymbol'])['price'], 2)
        row['total'] = round(lookup(row['stocksymbol'])['price'] * row['SUM(sharespurchased)'], 2)
        print(row['total'])

    remainingcash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    print(remainingcash)
    cash = float(remainingcash[0]['cash'])
    investmenttotal = 0.00

    for row in rows:
        investmenttotal += float(row['total'])

    totalinvestment = float(cash + investmenttotal)

    return render_template("index.html", data=rows, remainingcash=cash, suminvcash=totalinvestment)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM transactions WHERE user_id=?", session["user_id"])

    return render_template("history.html", data=rows)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stocksymbol = request.form.get("symbol")

        # check if the stock symbol is filled in
        if not stocksymbol:
            return apology("must provide a stock symbol", 400)
        else:
            stockquote = lookup(stocksymbol)
            if not stockquote:
                return apology("must provide a valid stock symbol", 400)
            else:
                return render_template("quoted.html", stockquote=stockquote)

    elif request.method == "GET":
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stocksymbol = request.form.get("symbol")
        quantity = request.form.get("shares")

        # check if the stock symbol is filled in
        if not stocksymbol:
            return apology("must provide a stock symbol", 400)

        if not quantity:
            return apology("must provide a valid quantity of shares to purchase", 400)

        try:
            quantity = int(quantity)
        except:
            return apology("shares should be an integer")

        if quantity <= 0:
            return apology("must provide a valid quantity of shares to purchase", 400)

        stockquote = lookup(stocksymbol)
        if not stockquote:
            return apology("must provide a valid share to buy", 400)
        else:
            print(quantity)
            print(stockquote['price'])
            txnval = '{:.2f}'.format(round(float(quantity) * float(stockquote["price"]), 2))
            print(txnval)
            rows = db.execute(
                "INSERT INTO transactions (user_id, stocksymbol, stockname, sharespurchased, txnprice, purchasevalue) VALUES (?,?,?,?,?,?)",
                session["user_id"], stocksymbol, stockquote["name"], quantity, stockquote["price"], str(txnval))

            db.execute("UPDATE users SET cash = (cash - ?) WHERE id = ?", txnval, session["user_id"])

    elif request.method == "GET":
        return render_template("buy.html")

    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        stocksymbol = request.form.get("symbol")
        quantity = int(request.form.get("shares"))

        # check if the stock symbol is filled in
        if not stocksymbol:
            return apology("must provide a stock symbol", 400)

        if not quantity:
            return apology("must provide a valid quantity of shares to purchase", 400)

        try:
            quantity = int(quantity)
        except:
            return apology("shares should be an integer")

        if quantity <= 0:
            return apology("must provide a valid quantity of shares to purchase", 400)

        availquantity = db.execute(
            "SELECT SUM(sharespurchased) FROM transactions WHERE user_id = ? AND stocksymbol = ?",
            session["user_id"], stocksymbol)

        if not availquantity:
            return apology("must provide a valid share to sell", 400)
        elif availquantity[0]['SUM(sharespurchased)'] < quantity:
            return apology("cannot sell more than you hold", 400)

        stockquote = lookup(stocksymbol)
        if not stockquote:
            return apology("must provide a valid share to sell", 400)
        else:
            txnval = int(quantity) * stockquote["price"]
            txnval *= -1
            quantity *= -1

            checkrow = db.execute(
                "SELECT * FROM transactions WHERE user_id = ? AND stocksymbol = ?",
                session["user_id"], stocksymbol)

            if len(checkrow) > 0:
                rows = db.execute(
                    "INSERT INTO transactions (user_id, stocksymbol, stockname, sharespurchased, txnprice, purchasevalue) VALUES (?,?,?,?,?,?)",
                    session["user_id"], stocksymbol, stockquote["name"], quantity, stockquote["price"], txnval)

                db.execute("UPDATE users SET cash = (cash - ?) WHERE id = ?", txnval, session["user_id"])
            else:
                return apology("must provide a validly owned share to sell", 400)

    elif request.method == "GET":
        symbols = db.execute("SELECT DISTINCT stocksymbol FROM transactions WHERE user_id = ?", session["user_id"])
        print(symbols)
        return render_template("sell.html", data=symbols)

    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)