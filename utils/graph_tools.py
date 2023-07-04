import pandas as pd


def replace_url_w_drug_name(url: str):
    """
    Replaces the drug name in the url with the drug name
    E.g. https://www.drugs.com/mtm/prevident.html > prevident
    """
    return url[url.rfind("$")+1:-5]


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
