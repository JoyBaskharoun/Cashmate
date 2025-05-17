from flask import request, jsonify
from models.storage import load_transaction, save_transaction

def update_transaction():
    data = request.get_json()
    id = data.get("id")

    transactions = load_transaction()
    updated = False

    for t in transactions:
        if str(t.id) == str(id):
            # Update amount only if provided and valid
            if "amount" in data:
                try:
                    t.amount = float(data["amount"])
                except (ValueError, TypeError):
                    return jsonify({"status": "error", "message": "Invalid amount value"})

            # Update timestamp only if provided and non-empty
            if "timestamp" in data and data["timestamp"]:
                t.timestamp = data["timestamp"]

            # ~ note only if provided 
            if "note" in data:
                t.note = data["note"]

            updated = True
            break 

    if updated:
        save_transaction(transactions)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Transaction not found"}), 404



def delete_transaction():
    data = request.get_json()
    id = data.get("id")

    transactions = load_transaction()
    new_transactions = [t for t in transactions if str(t.id) != str(id)]

    if len(new_transactions) == len(transactions):
        return jsonify({"status": "not found"})

    save_transaction(new_transactions)
    return jsonify({"status": "deleted"})