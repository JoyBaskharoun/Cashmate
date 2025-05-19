from datetime import datetime, timedelta
from models.storage import load_transaction

def filter_transactions_by_date(transactions, filter_type):
    now = datetime.now()
    if filter_type == "all-time":
        return transactions
    if filter_type == "day":
        cutoff = now - timedelta(days=1)
    elif filter_type == "week":
        cutoff = now - timedelta(weeks=1)
    elif filter_type == "month":
        cutoff = now - timedelta(days=30)
    elif filter_type == "year":
        cutoff = now - timedelta(days=365)
    else:
        cutoff = now - timedelta(weeks=1)
    result = []
    for t in transactions:
        t_date = datetime.fromisoformat(t.timestamp)
        if t_date >= cutoff:
            result.append(t)
    return result

def render_grouped_transactions(email, t_type_filter, filter_type):
    transactions = load_transaction()
    filtered = []
    for t in transactions:
        if t.email == email and t.t_type.lower() == t_type_filter.lower():
            filtered.append(t)
    filtered = filter_transactions_by_date(filtered, filter_type)

    if len(filtered) == 0:
        return f"""
        <tr>
            <td colspan="4" style="text-align:center; font-style: italic;">
                You haven't added transactions yet.
            </td>
        </tr>
        """

    # sort by date descending
    for i in range(len(filtered)):
        for j in range(len(filtered) - i - 1):
            d1 = datetime.fromisoformat(filtered[j].timestamp)
            d2 = datetime.fromisoformat(filtered[j+1].timestamp)
            if d1 < d2:
                filtered[j], filtered[j+1] = filtered[j+1], filtered[j]

    categories = {}
    for t in filtered:
        if t.category not in categories:
            categories[t.category] = []
        categories[t.category].append(t)

    html = ""
    idx = 0
    for category, trans in categories.items():
        total = 0
        for t in trans:
            total += t.amount
        html += f"""
        <tr id="{t_type_filter}-row-{idx}">
            <td class="bold-td">{category}</td>
            <td class="bold-td">${total:.2f}</td>
        </tr>
        <tr class="content" id="{t_type_filter}-content-row-{idx}">
            <td colspan="3">
                <table class="inner-table">
                    <tbody>
        """
        for t in trans:
            note = t.note if t.note else "-"
            html += f"""
            <tr class="tr" data-id="{t.id}">
                <td class="amount-cell">${t.amount:.2f}</td>
                <td class="date-cell">{t.formatted_date()}</td>
                <td class="note-cell">{note}</td>
                <td class="icons-container">
                    <img src="/static/images/icons/edit.svg" alt="Edit" class="action-icon edit-btn" title="Edit">
                    <img src="/static/images/icons/bin.svg" alt="Delete" class="action-icon delete-btn" title="Delete">
                </td>
            </tr>
            """
        html += """
                    </tbody>
                </table>
            </td>
        </tr>
        """
        idx += 1

    return html
