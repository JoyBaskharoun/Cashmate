from flask import Flask, request, redirect
import json
from models import add_transaction, get_summary, recent_transactions,load_transaction, filter_transactions_by_date, render_grouped_transactions

app = Flask(__name__)
USER_FILE = "data/users.json"

# Password "hash" (adds "xyz")
def hash_password(password):
    return password + "xyz"

# Read HTML file
def get_html(page):
    with open(f"templates/{page}.html", "r", encoding='utf-8') as file:
        return file.read()

# Read users from file
def read_users():
    try:
        with open(USER_FILE, "r", encoding='utf-8') as file:
            return json.load(file)
    except:
        return []

# Save users to file
def save_users(users):
    with open(USER_FILE, "w", encoding='utf-8') as file:
        json.dump(users, file)

@app.route("/")
def home():
    return get_html("index")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return "Need username and password!", 400
            
        users = read_users()
        for user in users:
            if user["username"] == username:
                return "Username taken!", 400
                
        users.append({"username": username, "password": hash_password(password)})
        save_users(users)
        return '<meta http-equiv="refresh" content="0; url=/login" />'
    
    return get_html("signup")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return "Need username and password!", 400
            
        users = read_users()
        for user in users:
            if user["username"] == username and user["password"] == hash_password(password):
                return '<meta http-equiv="refresh" content="0; url=/dashboard" />', 200, {"Set-Cookie": f"username={username}"}
                
        return "Wrong username or password!", 401
    
    return get_html("login")

@app.route("/dashboard")
def dashboard():
    username = request.cookies.get("username")
    if not username:
        return '<meta http-equiv="refresh" content="0; url=/login" />'
        
    html = get_html("dashboard")    
    
    transactions = recent_transactions()
    summary = get_summary()
    
    # Build transactions HTML
    transactions_html = ""
    for t in transactions:
        transactions_html += f"""
        <tr>
            <td>{t.t_type}</td>
            <td>{t.amount}</td>
            <td>{t.category}</td>
            <td>{t.formatted_date()}</td>
            <td>{t.note}</td>
        </tr>
        """
    
    # Replace placeholders
    html = html.replace("{{username}}", username)
    html = html.replace("{{transactions}}", transactions_html)
    html = html.replace("{{total_income}}", str(round(summary['income'], 2)))
    html = html.replace("{{total_expense}}", str(round(summary['expense'], 2)))
    html = html.replace("{{balance}}", str(round(summary['balance'], 2)))
    
    return html


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        html = get_html("add")
        return html

    # POST method
    amount = request.form.get("amount")
    t_type = request.form.get("type")
    category = request.form.get("category")
    note = request.form.get("note", "")  

    if not amount or not t_type or not category:
        return "Missing required fields", 400

    # Convert amount to float
    try:
        amount = float(amount)
    except ValueError:
        return "Invalid amount", 400

    add_transaction(amount, t_type, category, note)

    # Redirect back to dashboard after adding
    return redirect("/dashboard")



@app.route("/expenses")
def expenses():
    filter_type = request.args.get("filter", "week")
    transactions = load_transaction()
    expenses_html = render_grouped_transactions(transactions, "expense", filter_type)
    html = get_html("expenses")
    html = html.replace("{{expenses}}", expenses_html)
    return html



@app.route("/incomes")
def incomes():
    filter_type = request.args.get("filter", "week")
    transactions = load_transaction()
    incomes_html = render_grouped_transactions(transactions, "income", filter_type)
    html = get_html("incomes")
    html = html.replace("{{incomes}}", incomes_html)
    return html


@app.route("/logout")
def logout():
    return '<meta http-equiv="refresh" content="0; url=/login" />', 200, {"Set-Cookie": "username=; Expires=Thu, 01 Jan 1970 00:00:00 GMT"}

if __name__ == "__main__":
    try:
        with open(USER_FILE, "x") as file:
            json.dump([], file)
    except:
        pass
        
    app.run(debug=True)