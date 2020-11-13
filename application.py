import os
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

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

# Configure Flask to use SQLAlchemy (SQLite3) database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'finances.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure marshmallow
ma = Marshmallow(app)

# Create classes/models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    hash = db.Column(db.String)
    cash = db.Column(db.Integer)
    # Create initializer/constructor
    def __init__(self, username, hash, cash):
        self.username = username
        self.hash = hash
        self.cash = cash
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    symbol = db.Column(db.String(5))
    current_shares = db.Column(db.Integer)
    # Create initializer/constructor
    def __init__(self, user_id, symbol, current_shares):
        self.user_id = user_id
        self.symbol = symbol
        self.current_shares = current_shares
class Bought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer)
    time = db.Column(db.String)
    symbol = db.Column(db.String(5))
    shares_bought = db.Column(db.Integer)
    price_bought = db.Column(db.Float)
    # Create initializer/constructor
    def __init__(self, buyer_id, time, symbol, shares_bought, price_bought):
        self.buyer_id = buyer_id
        self.time = time
        self.symbol = symbol
        self.shares_bought = shares_bought
        self.price_bought = price_bought
class Sold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer)
    time = db.Column(db.String)
    symbol = db.Column(db.String(5))
    shares_sold = db.Column(db.Integer)
    price_sold = db.Column(db.Float)
    # Create initializer/constructor
    def __init__(self, seller_id, time, symbol, shares_sold, price_sold):
        self.seller_id = seller_id
        self.time = time
        self.symbol = symbol
        self.shares_sold = shares_sold
        self.price_sold = price_sold

# Create Schemas (only include data you want to show)
class UsersSchema(ma.Schema):
    class Meta:
        fields = ('username', 'cash')
class PortfolioSchema(ma.Schema):
    class Meta:
        fields = ('symbol', 'current_shares')
class BoughtSchema(ma.Schema):
    class Meta:
        fields = ('time', 'symbol', 'shares_bought', 'price_bought')
class SoldSchema(ma.Schema):
    class Meta:
        fields = ('time', 'symbol', 'shares_sold', 'price_sold')
        
# Initialize Schemas
users_schema = UsersSchema
portfolio_schema = PortfolioSchema(many=True)
bought_schema = BoughtSchema(many=True)
sold_schema = SoldSchema(many=True)

# To create database in python shell:
# Python
# from application import db
# db.create_all()

# To create database with SQL command-line arguemnts
#("CREATE TABLE portfolio (user_id INTEGER, symbol TEXT, current_shares INTEGER)")
#("CREATE TABLE bought (buyer_id INTEGER, time NUMERIC, symbol TEXT, shares_bought INTEGER, price_bought INTEGER)")
#("CREATE TABLE sold (seller_id INTEGER, time NUMERIC, symbol TEXT, shares_sold INTEGER, price_sold INTEGER)")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    # Obtain user id
    user = session["user_id"]
    print("user: ", user)

    # Obtain available cash
    available = (Users.query.filter_by(id = user).first()).cash
    print("available: ", available)

    # Obtain at least one stock symbol that the user possesses
    symbol_list = Portfolio.query.filter_by(user_id = user).all()
    print("symbol list: ", symbol_list)

    # If user has no stocks return minimum information
    if symbol_list == []:
        return render_template("index.html", available = usd(available), grand_total = usd(available),  total = [], shares = [], price = [], symbols = [], symbol_list_length = 0)
    # If user owns stocks return the remaining information
    else:
        # Calculate symbol list length for iteration in index.html
        symbol_list_length = len(symbol_list)
        print("symbol_list_length: ", symbol_list_length)

        # Create empty arrays to store values
        symbols = []
        price = []
        shares = []
        total = []
        # Calculate value of each holding of stock in portfolio
        for i in range(len(symbol_list)):
            symbol_index = symbol_list[i].symbol
            print("symbol_index:", symbol_index)
            symbols.append(symbol_index)
            # Obtain price of stock using iex API
            price_index = float(lookup(symbol_index).get('price'))
            print("price_index:", price_index)
            price.append(price_index)
            # Obtain number of shares that the user possesses to calculate total value
            shares_list = Portfolio.query.filter_by(user_id = user, symbol = symbol_index).all()
            print("shares_list:", shares_list)
            #("SELECT current_shares FROM portfolio WHERE user_id = :id AND symbol = :symbol", id = user, symbol = symbol_index)
            # Iterate over list of dicts
            for i in range(len(shares_list)):
                share_index = shares_list[i].current_shares
                print("share_index:", share_index)
                shares.append(share_index)
            # Calculate total value of stocks
            calc = share_index * price_index
            print("calc:", calc)
            total.append(calc)
        print("symbols:", symbols)
        print("price:", price)
        print("shares:", shares)
        print("total:", total)
        # Calculate grand total value of all assets
        grand_total = sum(total) + available

        # Render page with information
        return render_template("index.html", symbol_list = symbol_list, symbol_list_length = symbol_list_length, shares = shares, price = price, total = total, available = usd(available), grand_total = usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol").upper()

        # User error handling: stop empty symbol and shares fields, stop invalid symbols, and negative share numbers
        if not symbol:
            return apology("Please enter a stock symbol, i.e. AMZN", 403)
        result = lookup(symbol)
        if result == str:
             return apology("Please enter a valid stock symbol", 403)
        shares = int(request.form.get("shares"))
        if shares < 0:
             return apology("Please enter a positive number", 403)
        if shares == 0:
             return apology("Transaction will not proceed", 403)

        # Obtain user id
        user = session["user_id"]
        print("user:", user)

        # Obtain available cash
        available = (Users.query.filter_by(id = user).first()).cash
        print("available:", available)

        # Use IEX API to get price of stock
        price = lookup(symbol).get('price')
        print("price:", price)

        # Calculate total cost
        total = shares * price
        
        # User error handling: stop user if seeking to buy beyond cash balance
        if available < total:
             return apology("Insufficient funds to complete transaction", 403)
        
        # Continue with transaction and calculate remaining cash
        remaining = available - total

        # Obtain year, month, day, hour, minute, second
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")

        # Update cash field in Users Table and create entry into Bought Table
        update_cash = Users.query.filter_by(id = user).first()
        update_cash.cash = remaining
        db.session.commit()
        #"UPDATE users SET cash = :remaining WHERE id = :id", remaining = remaining, id = user)

        # Log transaction history
        log_purchase = Bought(user, time, symbol, shares, price)
        db.session.add(log_purchase)
        db.session.commit()
        #("INSERT INTO bought (buyer_id, time, symbol, shares_bought, price_bought) VALUES (:buyer_id, :time, :symbol, :shares_bought, :price_bought)", time = datetime.datetime.now(), symbol = symbol, shares_bought = shares, price_bought = price, buyer_id = user)

        # If buyer never bought this stock before
        portfolio = Portfolio.query.filter(Portfolio.user_id == user, Portfolio.symbol == symbol).first()
        print("portfolio", portfolio)

        #("SELECT symbol FROM portfolio WHERE user_id = :id AND symbol = :symbol", id = user, symbol = symbol)
        if portfolio == None:
            db.session.add(Portfolio(user, symbol, shares))
            db.session.commit()
            #("INSERT INTO portfolio (user_id, symbol, current_shares) VALUES (:user_id, :symbol, :current_shares)", user_id = user, symbol = symbol, current_shares = shares)
        else:
            stock_owned = portfolio.symbol
            print("stock_owned", stock_owned)
            # Obtain current number of shares from portfolio
            current_shares = portfolio.current_shares
            print("current shares", current_shares)
            #("SELECT current_shares FROM portfolio WHERE user_id = :id AND symbol = :symbol", id = user, symbol = symbol)

            # Calculate new amount of shares
            new_shares = shares + current_shares
            print("Total shares now:", new_shares)

            # Update portfolio table with new amount of shares
            portfolio.current_shares = new_shares
            print("Update db with new total:", portfolio.current_shares)
            db.session.commit()
            #("UPDATE portfolio SET current_shares = :new_shares WHERE user_id = :id", new_shares = new_shares, id = user)

        return render_template("bought.html", symbol = symbol, shares = shares, total = usd(total))


@app.route("/history")
@login_required
def history():
    # Obtain user id
    user = session["user_id"]

    # Obtain purchase history
    bought_list = Bought.query.filter_by(buyer_id = user).all()
    print("bought_list:", bought_list)
    #("SELECT time, symbol, shares_bought, price_bought FROM bought WHERE buyer_id = :id", id = user)

    # If user didn't sell stocks, only query bought table, if didn't buy anything, return empty
    if bought_list == []:
        # Will return empty list if user didn't buy anything
        return render_template("history.html", bought_list_length = 0, bought_list = [], sold_list_length = 0, sold_list = [])
        
    # Else query sold table
    else:
        # Obtain sell history
        sold_list = Sold.query.filter_by(seller_id = user).all()
        print("sold_list:", sold_list)
        #("SELECT time, symbol, shares_sold, price_sold FROM sold WHERE seller_id = :id", id = user)

        # Calculate length of bought_list and sold_list
        bought_list_length = len(bought_list)
        sold_list_length = len(sold_list)

        return render_template("history.html", bought_list = bought_list, sold_list = sold_list, bought_list_length = bought_list_length, sold_list_length = sold_list_length)


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
        rows = Users.query.filter_by(username=request.form.get("username")).first()
        #("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if rows.username != request.form.get("username") or not check_password_hash(rows.hash, request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows.id

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        data = lookup(symbol)
        return render_template("quoted.html", data = data)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Obtain username inputted
        username = request.form.get("username")

        # User error handling: stop empty username and password fields, stop usernames already taken, stop non-matching passwords
        if not username:
            return apology("Please enter a username", 403)
        existing = Users.query.filter_by(username=username)

        #("SELECT * FROM users WHERE username = :username", username=username)
        if existing == username:
            return apology("Username already taken", 403)
        password = request.form.get("password")
        if not password:
            return apology("Please enter a password", 403)
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("Passwords do not match", 403)
        hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # All users automatically recieve $10,000 to start with
        cash = 10000

        # Add and commit the data into database
        db.session.add(Users(username, hashed, cash))
        db.session.commit()
        #("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hashed)

        # Bring user to login page
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Obtain user id
    user = session["user_id"]

    if request.method == "GET":
        # Obtain stock symbols that the user possesses
        symbol_list = Portfolio.query.filter_by(user_id = user).all()
        #("SELECT symbol FROM portfolio WHERE user_id = :id", id = user)

        # If user never bought anaything, return empty values
        if symbol_list == []:
            return render_template("sell.html", symbol_list_length = 0)
        # Else display stock symbols in drop-down menu
        else:
            symbol_list_length = len(symbol_list)
            # Render sell page with list of stocks the user owns
            return render_template("sell.html", symbol_list = symbol_list, symbol_list_length = symbol_list_length)
    else:
        # Obtain stock symbol from user
        symbol = request.form.get("symbol")

        # If user doesn't own stock, render error
        if symbol == '':
            return apology("Must own stock before selling", 403)

        # Obtain number of shares from user
        shares = int(request.form.get("shares"))

        # Prevent user from submitting form with no number, negative number, or zero
        if not shares:
             return apology("Please enter number of shares", 403)
        if shares < 0:
             return apology("Please enter a positive number", 403)
        if shares == 0:
             return apology("Transaction will not proceed", 403)

        # Obtain data for stock selected
        shares_held_list = Portfolio.query.filter(Portfolio.user_id == user, Portfolio.symbol == symbol).first()
        #("SELECT current_shares FROM portfolio WHERE user_id = :id AND symbol = :symbol", id = user, symbol = symbol)
        print("shares_held_list:", shares_held_list)

        # Obtain number of shares for stock selected
        shares_held = shares_held_list.current_shares
        print("shares_held:", shares_held)

        # Prevent user from selling more than they have
        if shares > shares_held:
            return apology("Unable to sell more than you have", 403)

        # Obtain available cash
        available = (Users.query.filter_by(id = user).first()).cash
        #("SELECT cash FROM users WHERE id = :id", id = user)

        # Obtain current price of stock
        price = lookup(symbol).get('price')

        # Calculate new number of shares
        updated_shares = shares_held - shares

        # Remove stocks from user's portfolio by number of shares indicated
        portfolio = Portfolio.query.filter(Portfolio.user_id == user, Portfolio.symbol == symbol).first()
        print("portfolio", portfolio)
        portfolio.current_shares = updated_shares
        print("Update db with new total:", portfolio.current_shares)
        db.session.commit()
        #("UPDATE portfolio SET current_shares = :updated_shares WHERE user_id = :id", updated_shares = updated_shares, id = user)

        # Calculate new amount of available cash
        total = available + (price * shares)

        # Update cash field in Users Table
        update_cash = Users.query.filter_by(id = user).first()
        update_cash.cash = total
        db.session.commit()
        #("UPDATE users SET cash = :total WHERE id = :id", total = total, id = user)

        # Obtain year, month, day, hour, minute, second
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")

        # Log transaction history
        log_sale = Sold(user, time, symbol, shares, price)
        db.session.add(log_sale)
        db.session.commit()
        #("INSERT INTO sold (seller_id, time, symbol, shares_sold, price_sold) VALUES (:seller_id, :time, :symbol, :shares_sold, :price_sold)", time = datetime.datetime.now(), symbol = symbol, shares_sold = shares, price_sold = price, seller_id = user)

        # Render success page with infomation about transaction
        return render_template("sold.html", shares = shares, symbol = symbol.upper())


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# Run Server
if __name__ == '__main__':
    app.run(debug = True)
# Run the following in the command line: python application.py