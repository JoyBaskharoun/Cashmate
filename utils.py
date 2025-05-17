# Read HTML file
def get_html(page, message=""):
    with open(f"templates/{page}.html", "r") as file: #f to create formatted strings similar to `` instead of +
        content = file.read()
       
    content = content.replace("{{message}}", message)
    
    return content


# Append in txt file
def add_info(username):
    with open("data/temp.txt", "a") as file:
        file.write(username + "\n")