from flask import request, jsonify
from models.storage import load_transaction, save_transaction

def update_transaction():
    data = request.get_json()
    id = data.get("id") 
    amount = float(data["amount"])
    new_timestamp = data.get("timestamp", None)
    
    transactions = load_transaction()
    updated = False

    for t in transactions:
        if str(t.timestamp) == str(id):
            t.amount = amount
            
            if new_timestamp:
                t.timestamp = new_timestamp
            
            if "note" in data:
                t.note = data["note"]
            
            updated = True
            break

    if updated:
        save_transaction(transactions)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "not found"})




def delete_transaction():
    data = request.get_json()
    id = data.get("id")
    if not id:
        return jsonify({"status": "error", "message": "Missing transaction ID"}), 400

    transactions = load_transaction()
    new_transactions = [t for t in transactions if str(t.timestamp) != str(id)]

    if len(new_transactions) == len(transactions):
        return jsonify({"status": "not found"}), 404

    save_transaction(new_transactions)
    return jsonify({"status": "deleted"})
