# Read HTML file
def get_html(page, message=""):
    with open(f"templates/{page}.html", "r", encoding='utf-8') as file:
        content = file.read()               
    return content.replace("{{message}}", message)  
