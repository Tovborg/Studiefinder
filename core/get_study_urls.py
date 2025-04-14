import requests
import json
# import beautifulsoup4
from bs4 import BeautifulSoup
import re
import os
import csv
# Base URL
bachelor_url = "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser/"

# Field of study URLs
links_to_studies = {
    "Erhvervssprog": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser/humanistiskebacheloruddannelser-0",
    "Øvrige humaniora": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser/humanistiskebacheloruddannelser-1",
    "Sprog": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser/humanistiskebacheloruddannelser/sprog",
    "Kunstneriske uddannelser": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser/kunstneriskeuddannelser",
    "Biologi, geografi, geologi mv.": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser-0",
    "Matematik, fysik, kemi og datalogi": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser-1",
    "Øvrige naturvidenskab": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser-2",
    "Erhvervsøkonomi": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser-4",
    "Forvaltning mv.": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser-5",
    "Øvrige samfundsvidenskab": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser-6",
    "Sundhedsvidenskabelige bacheloruddannelser": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser-7",
    "Ingeniørfag": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser-9",
    "Øvrige teknisk videnskab": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser-10",
    "Teologisk bacheloruddannelse": "https://www.ug.dk/uddannelser/bachelorogkandidatuddannelser/bacheloruddannelser/teologiskbacheloruddannelse"
}

BASE_URL = "https://www.ug.dk"

with open("uddannelser.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["kategori", "titel", "url"])  # Write header

    def parse_study_page(study, url):
        print(f"Gathering links for {study}")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        div = soup.find("div", class_="panel-pane pane-views-panes pane-content-structure-children-panel-pane-1")
        if not div:
            print(f"Div not found for {study} at {url}")
            return
        links = div.find_all("a")
        hrefs = [link.get("href") for link in links if link.get("href")]

        for href in hrefs:
            full_url = BASE_URL + href
            title = href.split("/")[-1].replace("-", " ").capitalize()
            writer.writerow([study, title, full_url])   # Write each row
    
    for study, url in links_to_studies.items():
        parse_study_page(study, url)
    

