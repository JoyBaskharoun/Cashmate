from flask import Flask, session, redirect, url_for, request
from functools import wraps
from routes.authentications import signup_route, login_route, logout_route
from routes.dashboard import dashboard_route
from routes.transactions import add_route, income_route, expenses_route
from routes.edits import update_transaction, delete_transaction
from models.storage import load_transaction
from models.filters import filter_transactions_by_date, render_grouped_transactions



app = Flask(__name__)
app.secret_key = "strong-secret-key"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    if "email" in session:
        return redirect(url_for("dashboard"))
    from utils import get_html
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
    return dashboard_route()

@app.route("/add", methods=["GET", "POST"])
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

@app.route("/api/income")
@login_required
def api_income():
    filter_type = request.args.get("filter", "all-time")
    email = session.get("email")
    transactions = load_transaction()
    filtered_transactions = [
        t for t in transactions if t.email == email and t.t_type.lower() == "income"
    ]
    filtered = filter_transactions_by_date(filtered_transactions, filter_type)

    # Use your existing function to generate HTML rows for filtered transactions
    html_rows = render_grouped_transactions(email, "income", filter_type)
    return html_rows


if __name__ == "__main__":
    app.run(debug=True)