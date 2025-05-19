from flask import session
from models.summary import get_summary, recent_transactions
from utils import get_html
from routes.authentications import read_users

def dashboard_route():
    email = session.get("email")

    users = read_users()
    user = None
    for u in users:
        if u["email"] == email:
            user = u
            break

    if user:
        username = user["username"]
    else:
        username = ""

    html = get_html("dashboard")
    transactions = recent_transactions(email)
    summary = get_summary(email)

    if len(transactions) == 0:
        # Show message when no transactions exist
        transactions_html = """
        <tr>
            <td colspan="5" style="text-align:center; font-style: italic;">
                You haven't added any transactions yet.
            </td>
        </tr>
        """
    else:
        transactions_html = ""
        for t in transactions:
            transactions_html += "<tr>"
            transactions_html += "<td>" + t.t_type.capitalize() + "</td>"
            transactions_html += "<td>$" + str(t.amount) + "</td>"
            transactions_html += "<td>" + t.category + "</td>"
            transactions_html += "<td>" + t.formatted_date() + "</td>"
            if t.note:
                transactions_html += "<td class='note'>" + t.note + "</td>"
            else:
                transactions_html += "<td class='note'>-</td>"
            transactions_html += "</tr>"

    html = html.replace("{{transactions}}", transactions_html)
    html = html.replace("{{total_income}}", str(round(summary['income'], 2)))
    html = html.replace("{{total_expense}}", str(round(summary['expense'], 2)))
    html = html.replace("{{balance}}", str(round(summary['balance'], 2)))
    html = html.replace("{{username}}", username)

    return html
