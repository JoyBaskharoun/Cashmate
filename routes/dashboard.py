from flask import session
from models.summary import get_summary, recent_transactions
from utils import get_html
from routes.authentications import read_users

def dashboard_route():
    email = session.get("email")
    
    users = read_users()
    user = next((u for u in users if u["email"] == email), None)
    username = user["username"] if user else ""
    
    html = get_html("dashboard")    
    transactions = recent_transactions(email)
    summary = get_summary(email)
        

    transactions_html = ""
    for t in transactions:
        transactions_html += f"""
        <tr>
            <td>{t.t_type.capitalize()}</td>
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
    html = html.replace("{{username}}", username) 
    
    return html



