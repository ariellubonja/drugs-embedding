import os


def get_all_drugs_html(folder_path):
    html_text = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            with open(folder_path + filename, 'r') as file:
                html_text[filename] = file.read()
    
    return html_text