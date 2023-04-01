import pandas as pd
from bs4 import BeautifulSoup
import requests

def findURLS(table):
    links = []
    for tr in table.findAll("tr"):
        trs = tr.findAll("td")
        for each in trs:
            try:
                link = each.find("a")["href"]
                fullLink = "https://kworb.net/youtube/" + link
                links.append(fullLink)
            except:
                pass
    
    return links

def scrapeURLS(url):
    links_df = pd.read_html(url)[0]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    linksTable = soup.find('table')
    links = findURLS(linksTable)
    links_df["Link"] = links
    return links_df