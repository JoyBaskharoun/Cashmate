from flask import Flask, request
from routes.authentications import signup_route, login_route, logout_route
from routes.dashboard import dashboard_route
from routes.transactions import add_route, income_route, expenses_route

app = Flask(__name__)
app.secret_key = "strong-secret-key"

@app.route("/")
def home():
    from utils import get_html
    return get_html("index")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    return signup_route()

@app.route("/login", methods=["GET", "POST"])
def login():
    return login_route()

@app.route("/logout")
def logout():
    return logout_route()

@app.route("/dashboard")
def dashboard():
    return dashboard_route()

@app.route("/add", methods=["GET", "POST"])
def add():
    return add_route()

@app.route("/income")
def income():
    return income_route()

@app.route("/expenses")
def expenses():
    return expenses_route()

if __name__ == "__main__":
    app.run(debug=True)
