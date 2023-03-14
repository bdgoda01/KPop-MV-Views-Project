import pandas as pd
from bs4 import BeautifulSoup
import requests

url = "https://kworb.net/youtube/topvideos_korean.html"
df = pd.read_html(url)[0]

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')

links = []
for tr in table.findAll("tr"):
    trs = tr.findAll("td")
    for each in trs:
        try:
            link = each.find("a")["href"]
            links.append(link)
        except:
            pass

df["Link"] = links
print(df.head())