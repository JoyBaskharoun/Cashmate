from datetime import datetime, timedelta
from models.storage import load_transaction

def filter_transactions_by_date(transactions, filter_type):
    now = datetime.now()
    periods = {
        "day": timedelta(days=1),
        "week": timedelta(weeks=1),
        "month": timedelta(days=30),
        "year": timedelta(days=365)
    }
    if filter_type == "all-time":
        return transactions
    cutoff = now - periods.get(filter_type, timedelta(weeks=1))
    return [t for t in transactions if datetime.fromisoformat(t.timestamp) >= cutoff]

def render_grouped_transactions(username, t_type_filter, filter_type):
    transactions = load_transaction()
    filtered_transactions = [
        t for t in transactions 
        if t.username == username and t.t_type.lower() == t_type_filter.lower()
    ]
    filtered = filter_transactions_by_date(filtered_transactions, filter_type)

    category_dict = {}
    for t in filtered:
        category_dict.setdefault(t.category, []).append(t)

    html_rows = ""
    for idx, (category, txns) in enumerate(category_dict.items()):
        total = sum(t.amount for t in txns)
        html_rows += f"""
        <tr class="collapsible" id="{t_type_filter}-row-{idx}">
            <td class="bold-td">{category}</td>
            <td class="bold-td">${total:.2f}</td>
        </tr>
        <tr class="content" id="{t_type_filter}-content-row-{idx}">
            <td colspan="3">
                <table class="inner-table">
                    <tbody>
        """
        for t in txns:
            html_rows += f"""
            <tr data-id="{t.timestamp}">
                <td class="amount-cell">${t.amount:.2f}</td>
                <td class="date-cell">{t.formatted_date()}</td>
                <td class="note-cell">{t.note if t.note else "—"}</td>                    
                <td class="icons-container">
                    <img src="/static/images/icons/edit.svg" alt="Edit" class="action-icon edit-btn" title="Edit">
                    <img src="/static/images/icons/bin.svg" alt="Delete" class="action-icon delete-btn" title="Delete">
                </td>
            </tr>
            """

        html_rows += """
                    </tbody>
                </table>
            </td>
        </tr>
        """

    return html_rows
