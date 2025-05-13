from flask import session
from models.summary import get_summary, recent_transactions
from utils import get_html

def dashboard_route():
    username = session.get("username")
    html = get_html("dashboard")    
    transactions = recent_transactions(username)
    summary = get_summary(username)

    transactions_html = ""
    for t in transactions:
        transactions_html += f"""
        <tr>
            <td>{t.t_type}</td>
            <td>${t.amount}</td>
            <td>{t.category}</td>
            <td>{t.formatted_date()}</td>
            <td>{t.note if t.note else "—"}</td>
        </tr>
        """

    html = html.replace("{{transactions}}", transactions_html)
    html = html.replace("{{total_income}}", str(round(summary['income'], 2)))
    html = html.replace("{{total_expense}}", str(round(summary['expense'], 2)))
    html = html.replace("{{balance}}", str(round(summary['balance'], 2)))
    
    return html
