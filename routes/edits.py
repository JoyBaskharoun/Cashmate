from flask import request, jsonify
from models.storage import load_transaction, save_transaction

def update_transaction():
    data = request.get_json() 
    id = data.get("id")     

    transactions = load_transaction() 
    updated = False

    for t in transactions:
        if str(t.id) == str(id):  # find the right transaction
            if "amount" in data:
                try:
                    t.amount = float(data["amount"])
                except:
                    return jsonify({"status": "error", "message": "Bad amount"})

            if "timestamp" in data and data["timestamp"]:
                t.timestamp = data["timestamp"]  # change timestamp if there

            if "note" in data:
                t.note = data["note"]  # change note if there

            updated = True
            break

    if updated:
        save_transaction(transactions) 
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Not found"})


def delete_transaction():
    data = request.get_json()  
    id = data.get("id")       

    transactions = load_transaction() 
    new_transactions = []
    for t in transactions:
        if str(t.id) != str(id):  # keep all but the one to delete
            new_transactions.append(t)

    # important it solves an issue with response
    if len(new_transactions) == len(transactions):
        return jsonify({"status": "not found"})

    save_transaction(new_transactions) 
    return jsonify({"status": "deleted"})