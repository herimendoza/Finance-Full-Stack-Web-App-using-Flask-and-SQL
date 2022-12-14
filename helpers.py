import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def errorPage(title, info, file):
    return render_template('error.html', titlee=title, infoo=info, filee=file)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""
    apiSymbol = f"{urllib.parse.quote_plus(symbol)}"
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")

        url1 = "https://twelve-data1.p.rapidapi.com/price"
        
        querystring1 = {"symbol":apiSymbol,"format":"json","outputsize":"30"}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
        }
        response1 = requests.request("GET", url1, headers=headers, params=querystring1)

        response1.raise_for_status()

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response1.json()
        
        return {
            "price": float(quote["price"]),
            "symbol": apiSymbol,
        }
    except (KeyError, TypeError, ValueError):
        return None

def historyData(symbol):
    """Look up quote for symbol."""
    apiSymbol = f"{urllib.parse.quote_plus(symbol)}"
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")

        url2 = "https://twelve-data1.p.rapidapi.com/time_series"
        
        querystring2 = {"symbol":apiSymbol,"interval":"1day","outputsize":"30","format":"json"}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
        }

        response2 = requests.request("GET", url2, headers=headers, params=querystring2)

        response2.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:

        dataPoints = response2.json()
        stockDate = []
        stockPrice = []

        for data in dataPoints['values']:
            stockDate.append(data['datetime'].split("-", 1)[-1])
            stockPrice.append(float(data['close'])) 
        
        stockDate.reverse()
        stockPrice.reverse()
        
        return {
            "symbol": apiSymbol,
            "date": stockDate,
            "oldPrice": stockPrice
        }
    except (KeyError, TypeError, ValueError):
        return None

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
