# Read HTML file
def get_html(page):
    with open(f"templates/{page}.html", "r", encoding='utf-8') as file:
        return file.read()