from flask import request, redirect, session
import json
from utils import get_html, add_info

u_file = "data/users.json"

def hash_password(password):
    return password + "xyz"  

def read_users():
    try:
        file = open(u_file, "r")
        users = json.load(file)
        file.close()
        return users
    except:
        return []

def save_users(users):
    file = open(u_file, "w")
    json.dump(users, file)
    file.close()

from flask import session

def signup_route():
    message = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm-password", "")

        if email == "" or username == "" or password == "" or confirm_password == "":
            message = "Fill all fields."
        elif len(username) < 3:
            message = "Username too short."
        elif not username.isalpha():
            message = "Username must contain letters only."
        elif len(password) < 6:
            message = "Password too short."
        elif password != confirm_password:
            message = "Passwords don't match."
        else:
            users = read_users()
            found = False
            for u in users:
                if u["email"] == email:
                    found = True
                    break
            if found:
                message = "Email taken."
            else:
                users.append({
                    "email": email,
                    "username": username,
                    "password": hash_password(password)
                })
                save_users(users)
                add_info(username)

                # Set server-side session
                session["email"] = email
                session["username"] = username

                # Return JS snippet to save email in localStorage and redirect
                return f"""
                <script>
                  localStorage.setItem('email', '{email}');
                  window.location.href = '/dashboard';
                </script>
                """

        return get_html("signup", message=message)

    return get_html("signup")


def login_route():
    message = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        users = read_users()
        user_match = None
        for u in users:
            if u["email"] == email and u["password"] == hash_password(password):
                user_match = u
                break

        if user_match:
            session["email"] = user_match["email"]
            return """
                <script>
                  localStorage.setItem('email', '{}');
                  window.location.href = '/dashboard';
                </script>
                """.format(user_match["email"])
        else:
            message = "Wrong email or password."

        return get_html("login", message=message)

    return get_html("login")

def logout_route():
    session.clear()
    return redirect("/")