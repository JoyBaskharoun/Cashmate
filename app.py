from flask import Flask, session, redirect, url_for, Response, jsonify
from routes.authentications import signup_route, login_route, logout_route
from routes.dashboard import dashboard_route
from routes.transactions import add_route, income_route, expenses_route
from routes.edits import update_transaction, delete_transaction
from utils import get_html

app = Flask(__name__)
app.secret_key = "strong-secret-key"

# decorator function keeping some urls protected for none reg users
def login_required(f):  #f is for ex a flask route handler
    def decorated_function():
        if "email" not in session:
            return redirect(url_for("login"))
        return f() 
    decorated_function.__name__ = f.__name__ # perserve original func name (else flask sees every deco fun as "deco_func") causing conflicts. flask uses __name__ to reg routes
    return decorated_function


@app.route('/navbar')
def navbar():
    return get_html('navbar.html')

@app.route("/")
def home():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return get_html("index")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return signup_route()

@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return login_route()

@app.route("/logout")
@login_required
def logout():
    return logout_route()


@app.route("/dashboard")
@login_required
def dashboard():
    return dashboard_route() #page content

@app.route("/add", methods=["GET", "POST"]) #must specificaly say that it accepts both get and post
@login_required
def add():
    return add_route()

@app.route("/update-transaction", methods=["GET", "POST"])
@login_required
def route_update_transactions():
    return update_transaction()

@app.route("/delete-transaction", methods=["GET", "POST"])
@login_required
def route_delete_transactions():
    return delete_transaction()

@app.route("/income")
@login_required
def income():
    return income_route()

@app.route("/expenses")
@login_required
def expenses():
    return expenses_route()

# needed for charts
@app.route('/data/transactions.json')
@login_required
def serve_transactions_file():
    with open("data/transactions.json", "r") as file:
        content = file.read()
        return Response(content)


@app.route("/api/user-email")
@login_required
def get_user_email():
    return jsonify({"email": session.get("email")})


if __name__ == "__main__":
    app.run(debug=True)