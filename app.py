from flask import Flask, request
import json

app = Flask(__name__)
USER_FILE = "data/users.json"

# Password "hash" (adds "xyz")
def hash_password(password):
    return password + "xyz"

# Read HTML file
def get_html(page):
    with open(f"templates/{page}.html", "r", encoding='utf-8') as file:
        return file.read()

# Read users from file
def read_users():
    try:
        with open(USER_FILE, "r", encoding='utf-8') as file:
            return json.load(file)
    except:
        return []

# Save users to file
def save_users(users):
    with open(USER_FILE, "w", encoding='utf-8') as file:
        json.dump(users, file)

@app.route("/")
def home():
    return get_html("index")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return "Need username and password!", 400
            
        users = read_users()
        for user in users:
            if user["username"] == username:
                return "Username taken!", 400
                
        users.append({"username": username, "password": hash_password(password)})
        save_users(users)
        return '<meta http-equiv="refresh" content="0; url=/login" />'
    
    return get_html("signup")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return "Need username and password!", 400
            
        users = read_users()
        for user in users:
            if user["username"] == username and user["password"] == hash_password(password):
                return '<meta http-equiv="refresh" content="0; url=/dashboard" />', 200, {"Set-Cookie": f"username={username}"}
                
        return "Wrong username or password!", 401
    
    return get_html("login")

@app.route("/dashboard")
def dashboard():
    username = request.cookies.get("username")
    if not username:
        return '<meta http-equiv="refresh" content="0; url=/login" />'
        
    html = get_html("dashboard")
    html = html.replace("{{username}}", username)
    return html

@app.route("/logout")
def logout():
    return '<meta http-equiv="refresh" content="0; url=/login" />', 200, {"Set-Cookie": "username=; Expires=Thu, 01 Jan 1970 00:00:00 GMT"}

if __name__ == "__main__":
    try:
        with open(USER_FILE, "x") as file:
            json.dump([], file)
    except:
        pass
        
    app.run(debug=True)