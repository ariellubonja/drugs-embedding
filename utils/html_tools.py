import os
from bs4 import BeautifulSoup
import requests


def get_all_drugs_html(folder_path):
    html_text = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            with open(folder_path + filename, 'r') as file:
                html_text[filename] = file.read()
    
    return html_text


def get_drug_urls_in_list_page(page_url):
    """
        Extract all drug names from the likes of https://www.drugs.com/alpha/ab.html
        TODO there is a problem with some pages that have too few drugs e.g. https://www.drugs.com/alpha/ae.html
        Ignoring them for now
    """
    page = requests.get(page_url)

    parsed_page = BeautifulSoup(page.text)

    # Wanna look for this
    # ul class="ddc-list-column-2"><li><a href="/cons/a-b-otic.html">A/B Otic</a></li>
    # <li><a href="/mtm/abacavir.html">Abacavir</a></li>

    # https://www.geeksforgeeks.org/beautifulsoup-find-all-li-in-ul/
    drugs_ul = parsed_page.find("body").find("ul", {"class": "ddc-list-column-2"})

    try:
        ahrefs = drugs_ul.findAll("a")
        links = [c['href'] for c in ahrefs]

        return [base_url + l for l in links]
    except AttributeError:
        print("Skipped because layout is different: ", page_url)
        return []


def get_drug_class_name(html_text):
    """
    From html_text of a Drugs.com drug page, extract the drug class name and URL

    Parameters
    ----------
    html_text : str
        HTML text of a Drugs.com drug page
    """
    
    soup = BeautifulSoup(html_text, 'html.parser')

    # # Find the <b> tag containing 'Drug class:'
    # drug_class_tag = soup.find('b', string='Drug class:')

    # # Find the <a> tag that follows the <b> tag
    # a_tag = drug_class_tag.find_next_sibling('a')

    # # Extract the href link and text
    # href_link = a_tag['href']
    # text = a_tag.get_text()


    # return (text, href_link)

    # Find the <b> tag containing 'Drug class:'
    try:
        drug_class_tag = soup.find('b', string='Drug class:')
        if drug_class_tag is None:
            raise AttributeError('Drug class tag not found')
        
        # Find the <a> tag that follows the <b> tag
        a_tag = drug_class_tag.find_next_sibling('a')

        # Extract the href link and text
        href_link = a_tag['href']
        text = a_tag.get_text()

        # Print the extracted href link and text
        print(href_link)
        print(text)
    except AttributeError as e:
        print('Warning: Drug Class not found in ', soup.title.string)#, e)




