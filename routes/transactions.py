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

    # Validate required fields
    if not t_type or t_type not in ["income", "expense"]:
        return "Error: Please select a valid transaction type (income or expense)."

    if not category or category.strip() == "":
        return "Error: Category is required."

    if not amount:
        return "Error: Amount is required."

    # Validate amount is a positive number
    try:
        amount = float(amount)
        if amount <= 0:
            return "Error: Amount must be greater than zero."
    except ValueError:
        return "Error: Invalid amount format."

    # Handle timestamp: if not provided or empty, set to current datetime
    if not timestamp or timestamp.strip() == "":
        timestamp = datetime.now().isoformat(timespec='minutes')
    else:
        # Optional: validate timestamp format (ISO 8601)
        try:
            # This will raise ValueError if format is wrong
            datetime.fromisoformat(timestamp)
        except ValueError:
            return "Error: Invalid date/time format."

    email = session.get("email")
    if not email:
        return redirect("/login")

    # Call your function to add the transaction
    add_transaction(email, amount, t_type, category, note, timestamp)

    return redirect("/dashboard")

def income_route():
    email = session.get("email")
    if not email:
        return redirect("/login")

    filter_type = request.args.get("filter", "week")
    income_html = render_grouped_transactions(email, "income", filter_type)
    html = get_html("income").replace("{{income}}", income_html)
    return html

def expenses_route():
    email = session.get("email")
    if not email:
        return redirect("/login")

    filter_type = request.args.get("filter", "week")
    expenses_html = render_grouped_transactions(email, "expense", filter_type)
    html = get_html("expenses").replace("{{expenses}}", expenses_html)
    return html
