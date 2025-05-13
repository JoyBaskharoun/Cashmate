from flask import request, redirect, session
from utils import get_html
from models.storage import add_transaction
from models.filters import render_grouped_transactions

def add_route():
    if request.method == "GET":
        return get_html("add")

    amount = request.form.get("amount")
    t_type = request.form.get("type")
    category = request.form.get("category")
    note = request.form.get("note", "")  

    if not amount or not t_type or not category:
        return "Missing required fields"

    try:
        amount = float(amount)
    except ValueError:
        return "Invalid amount"

    username = session.get("username")
    add_transaction(username, amount, t_type, category, note)

    return redirect("/dashboard")

def income_route():
    username = session.get("username")
    if not username:
        return redirect("/login")

    filter_type = request.args.get("filter", "week")
    income_html = render_grouped_transactions(username, "income", filter_type)
    html = get_html("income").replace("{{income}}", income_html)
    return html

def expenses_route():
    username = session.get("username")
    if not username:
        return redirect("/login")

    filter_type = request.args.get("filter", "week")
    expenses_html = render_grouped_transactions(username, "expense", filter_type)
    html = get_html("expenses").replace("{{expenses}}", expenses_html)
    return html
