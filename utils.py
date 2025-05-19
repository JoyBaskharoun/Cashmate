# Read HTML file
def get_html(page, message=""):
    with open(f"templates/{page}.html", "r") as file: #f to create formatted strings 
        content = file.read()
       
    content = content.replace("{{message}}", message)
    
    return content


# Append in txt file
def add_info(username):
    file = open("data/temp.txt", "a")
    file.write(username + "\n")
    file.close()
