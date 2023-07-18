import os
from bs4 import BeautifulSoup
import requests
import pandas as pd

base_url = "https://www.drugs.com"

def get_all_drugs_html(folder_path):
    html_text = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            with open(folder_path + filename, 'r') as file:
                html_text[filename] = file.read()
    
    return html_text


def get_unique_drugs(drugs_edgelist_csv_path="outputs/drugs_html_edgelist.csv"):
    """
    Get the set of unique drugs from the crawled websites
    Returns only drugs that are contain a "Related Drugs" section. These are the only ones included in the graph
    """

    drugs_df = pd.read_csv(drugs_edgelist_csv_path)

    # Undo replacement of "/" with "$"
    drugs_df.iloc[:,0] = drugs_df.iloc[:,0].str.replace("/", "$")
    drugs_df.iloc[:,1] = drugs_df.iloc[:,1].str.replace("/", "$")

    # Get only drug name (remove url)
    drugs_df = drugs_df.applymap(replace_url_w_drug_name)

    drugs_df = drugs_df['0'].tolist() + drugs_df['1'].tolist()

    return set(drugs_df)


def replace_url_w_drug_name(url: str):
    """
    Replaces the drug name in the url with the drug name
    E.g. https://www.drugs.com/mtm/prevident.html > prevident
    """
    return url[url.rfind("$")+1:-5]


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


def get_drug_class_name(html_text, print_warnings=True):
    """
    From html_text of a Drugs.com drug page, extract the drug class name and URL

    Parameters
    ----------
    html_text : str
        HTML text of a Drugs.com drug page
    """
    
    soup = BeautifulSoup(html_text, 'html.parser')

    # Not all drugs have a drug class in the data
    try:
        drug_class_tag = soup.find('b', string='Drug class:')
        if drug_class_tag is None:
            raise AttributeError('Drug class tag not found')
        
        # Find the <a> tag that follows the <b> tag
        sibling = drug_class_tag.find_next_sibling('a')

        # The drug class may not always be a link
        if sibling.name == 'a':  # If the next sibling is an <a> tag
            href_link = sibling['href']
            drug_class = sibling.get_text()
        else:
            drug_class = sibling.strip()
            href_link = None

        return (drug_class, href_link)
    
    except AttributeError as e:
        if print_warnings:
            print('Warning: Drug Class not found in ', soup.title.string)#, e)

