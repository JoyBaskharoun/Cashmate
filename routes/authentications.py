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
    message = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm-password", "")

        if not email or not username or not password or not confirm_password:
            message = "Please fill in all fields."
        elif len(username) < 3:
            message = "Username must be at least 3 characters."
        elif len(password) < 6:
            message = "Password must be at least 6 characters."
        elif password != confirm_password:
            message = "Passwords do not match!"
        else:
            users = read_users()
            # Check if email already taken
            if any(u["email"] == email for u in users):
                message = "Email is already registered."
            else:
                users.append({
                    "email": email,
                    "username": username,
                    "password": hash_password(password)
                })
                save_users(users)
                return '<meta http-equiv="refresh" content="0; url=/login" />'

        return get_html("signup", message=message)

    return get_html("signup")




def login_route():
    message = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            message = "Please enter both email and password."
        else:
            users = read_users()
            user_match = next(
                (u for u in users if u["email"] == email and u["password"] == hash_password(password)),
                None,
            )
            if user_match:
                session["email"] = user_match["email"]
                return redirect("/dashboard")
            else:
                message = "Wrong email or password."

        return get_html("login", message=message)

    return get_html("login")



def logout_route():
    session.clear()
    return redirect("/")