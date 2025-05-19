from flask import request, redirect, session
from datetime import datetime
from utils import get_html
from models.storage import add_transaction
from models.filters import render_grouped_transactions

def add_route():
    if request.method == "GET":
        return get_html("add") 

    t_type = request.form.get("type")
    category = request.form.get("category")
    amount = request.form.get("amount")
    timestamp = request.form.get("timestamp")
    note = request.form.get("note", "")

    if t_type not in ["income", "expense"]:
        return "Error: Select income or expense." 

    if not category:
        return "Error: Category required." 

    if not amount:
        return "Error: Amount required." 

    try:
        amount = float(amount)
        if amount <= 0:
            return "Error: Amount must be positive."  # no zero or less
    except:
        return "Error: Invalid amount." 

    if not timestamp:
        timestamp = datetime.now().isoformat(timespec='minutes')  # use now if empty
    else:
        try:
            datetime.fromisoformat(timestamp)  # check date format
        except:
            return "Error: Bad date/time."  # bad date

    email = session.get("email")

    add_transaction(email, amount, t_type, category, note, timestamp) 

    return redirect("/dashboard")  


def income_route():
    email = session.get("email")

    filter_type = request.args.get("filter", "all-time")  # get filter or default
    income_html = render_grouped_transactions(email, "income", filter_type)
    html = get_html("income").replace("{{income}}", income_html)
    return html

def expenses_route():
    email = session.get("email")

    filter_type = request.args.get("filter", "all-time")  # get filter or default
    expenses_html = render_grouped_transactions(email, "expense", filter_type)
    html = get_html("expenses").replace("{{expenses}}", expenses_html)
    return html
