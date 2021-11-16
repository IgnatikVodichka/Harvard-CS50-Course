import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id= ?", user)[0]["cash"]
    user_stocks = db.execute("SELECT symbol, SUM(shares) AS shares, name FROM transactions WHERE user_id = ? GROUP BY symbol", user)

    grand_total = cash
    for stock in user_stocks:
        price = lookup(stock["symbol"])["price"]
        total = stock["shares"] * price
        grand_total += total
        stock.update({'price': price, 'total': total})
    return render_template("index.html", user_stocks=user_stocks, cash=cash, grand_total=grand_total)


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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username is unique
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        duplicates = len(db.execute('SELECT username FROM users WHERE username = ?', username))
        if not username:
            return apology("Username is empty, or already exists")
        elif not password:
            return apology("Invalid password or password field is empty")
        elif not password:
            return apology("Invalid password confirmation")
        if password != confirmation:
            return apology("Password and confirmation are not same")
        # register user in database
        pwhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, pwhash)
            return redirect("/")
        except:
            return apology("User already exists")
    else:
        return render_template("register.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Quote field can't be empty")
        quotation = lookup(symbol)
        if not quotation:
            return apology("No stocks found")
        else:
            return render_template("quoted.html", quotation=quotation)
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        quotation = lookup(symbol)
        user = session["user_id"]
        if not symbol:
            return apology("Dont't leave symbol field emty")
        try:
            shares = int(shares)
        except:
            return apology("Shares must be a number")
        if shares <= 0:
            return apology("Shares can't be 0 or negative number")
        if not quotation:
            return apology("No stocks found")
        cash = db.execute("SELECT cash FROM users WHERE id= ?", user)[0]["cash"]
        stock = quotation["name"]
        symbol = quotation["symbol"]
        price = quotation["price"]
        total = price * shares
        if cash < total:
            return apology("Not enough cash")
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total, user)
            db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, type) VALUES (?, ? , ?, ?, ?, ?)",
                       user, symbol, stock, shares, price, "buy")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user = session["user_id"]
    symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        user_shares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE (user_id = ? AND symbol = ?)", user, symbol)[
            0]["shares"]

        try:
            shares = int(shares)
        except:
            return apology("Shares must be a number")
        if not shares:
            return apology("Shares can't be empty")
        elif shares <= 0:
            return apology("Shares shoud be a positive integer")
        elif shares > user_shares:
            return apology("You don't have that many shares")
        elif not symbol:
            return apology("You must choose what to sell")
        elif not db.execute("SELECT symbol FROM transactions WHERE symbol = ? AND user_id = ?", symbol, user):
            return apology("You don't have this stock")
        else:
            quotation = lookup(symbol)
            stock = quotation["name"]
            symbol = quotation["symbol"]
            price = quotation["price"]
            total = price * shares
            cash = db.execute("SELECT cash FROM users WHERE id= ?", user)[0]["cash"]
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + total, user)
            db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, type) VALUES (?, ? , ?, ?, ?, ?)",
                       user, symbol, stock, 0 - shares, price, "sell")
            return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    if request.method == "POST":
        user = session["user_id"]
        # sorting
        bought = request.form.get("bought")
        sold = request.form.get("sold")
        all_t = request.form.get("all")
        if bought:
            user_stocks = db.execute("SELECT * FROM transactions WHERE user_id = ? AND type = 'buy'", user)
            return render_template("history.html", stocks=user_stocks)
        elif sold:
            user_stocks = db.execute("SELECT * FROM transactions WHERE user_id = ? AND type = 'sell'", user)
            return render_template("history.html", stocks=user_stocks)
        elif all_t:
            user_stocks = db.execute("SELECT * FROM transactions WHERE user_id = ?", user)
            return render_template("history.html", stocks=user_stocks)
    else:
        user = session["user_id"]
        user_stocks = db.execute("SELECT * FROM transactions WHERE user_id = ?", user)
        return render_template("history.html", stocks=user_stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
