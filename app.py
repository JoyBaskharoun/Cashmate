from flask import Flask, session, redirect, Response, jsonify, render_template
from jinja2 import FileSystemLoader
import os
from routes.authentications import signup_route, login_route, logout_route
from routes.dashboard import dashboard_route
from routes.transactions import add_route, income_route, expenses_route
from routes.edits import update_transaction, delete_transaction


template_paths = [os.path.join(os.path.dirname(__file__), path) for path in ['.', 'templates']]
app = Flask(__name__)
app.jinja_loader = FileSystemLoader(template_paths)
app.secret_key = "strong-secret-key"

# decorator function keeping some urls protected for none reg users
def login_required(f):
    def decorated_function():
        if "email" not in session:
            return redirect("login")
        return f()
    decorated_function.__name__ = f.__name__ # perserve original func name
    return decorated_function


@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route("/")
def home():
    if "email" in session:
        return redirect("dashboard")
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "email" in session:
        return redirect("dashboard")
    return signup_route()

@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" in session:
        return redirect("dashboard")
    return login_route()

@app.route("/logout")
@login_required
def logout():
    return logout_route()


@app.route("/dashboard")
@login_required
def dashboard():
    return dashboard_route()

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
    file = open("data/transactions.json", "r")
    content = file.read()
    file.close()
    return Response(content)


@app.route("/api/user-email")
@login_required
def get_user_email():
    return jsonify({"email": session.get("email")})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.after_request
def add_cache_control_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    return response

if __name__ == "__main__":
    app.run(debug=True)