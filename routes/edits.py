from flask import request, jsonify
from models.storage import load_transaction, save_transaction

def update_transaction():
    data = request.get_json()
    id = data["id"]  # original timestamp
    amount = float(data["amount"])
    new_timestamp = data["timestamp"]
    note = data.get("note", "")

    transactions = load_transaction()
    updated = False

    for t in transactions:
        if str(t.timestamp) == str(id):
            t.amount = amount
            t.timestamp = new_timestamp  # Be careful: see note above!
            t.note = note
            updated = True
            break

    if updated:
        save_transaction(transactions)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "not found"})



def delete_transaction():
    data = request.get_json()
    id = data["id"]

    transactions = load_transaction()
    new_transactions = [t for t in transactions if str(t.timestamp) != str(id)]
    if len(new_transactions) == len(transactions):
        return jsonify({"status": "not found"}), 404

    save_transaction(new_transactions)
    return jsonify({"status": "deleted"})

