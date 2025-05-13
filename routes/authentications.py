from flask import request, redirect, session
import json
from utils import get_html


USER_FILE = "data/users.json"

def hash_password(password):
    return password + "xyz"

def read_users():
    try:
        with open(USER_FILE, "r", encoding='utf-8') as file:
            return json.load(file)
    except:
        return []

def save_users(users):
    with open(USER_FILE, "w", encoding='utf-8') as file:
        json.dump(users, file)

def signup_route():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password") 
        
        if password != confirm_password:
            return "Passwords do not match!"

        users = read_users()
        if any(u["username"] == username for u in users):
            return "Username taken!"

        users.append({"username": username, "password": hash_password(password)})
        save_users(users)
        return '<meta http-equiv="refresh" content="0; url=/login" />'

    return get_html("signup")

def login_route():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Need username and password!"

        users = read_users()
        for user in users:
            if user["username"] == username and user["password"] == hash_password(password):
                session["username"] = username
                return '<meta http-equiv="refresh" content="0; url=/dashboard" />'

        return "Wrong username or password!"

    return get_html("login")

def logout_route():
    session.clear()
    return redirect("/login")