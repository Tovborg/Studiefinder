import requests
import json
# import beautifulsoup4
from bs4 import BeautifulSoup
import re
import os
import pandas as pd

# Load uddannelser.csv into a DataFrame
df = pd.read_csv("uddannelser.csv", encoding="utf-8")

def extract_sections_by_title(soup):
    sections = {}

    # Hent introduktion (fra .pane-node-field-pixi)
    intro_pane = soup.find("div", class_="panel-pane pane-entity-field pane-node-field-pixi")
    intro_manchet = soup.find("div", class_="panel-pane pane-entity-field pane-node-field-manchet")
    
    manchet_text = intro_manchet.get_text(separator="\n", strip=True) if intro_manchet else ""
    pane_text = intro_pane.get_text(separator="\n", strip=True) if intro_pane else ""

    # Kombinér til én introduktion
    intro_text = (manchet_text + "\n\n" + pane_text).strip()

    # Gem i dict
    if intro_text:
        sections["Introduktion"] = intro_text
       


    afsnitliste = soup.find("div", class_="view-afsnitsliste")
    if not afsnitliste:
        return sections

    rows = afsnitliste.find_all("div", class_="views-row")

    for row in rows:
        header = row.find("h2", class_="ug3-foldable-header")
        content = row.find("div", class_="views-field-field-bodytext")
        if header and content:
            title = header.get_text(strip=True)
            text = content.get_text(separator="\n", strip=True)
            sections[title] = text

    return sections

# loop through the DataFrame
for index, row in df.iterrows():
    print(f"Processing row {index + 1}/{len(df)}")
    url = row['url']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    sections = extract_sections_by_title(soup)
    # print(sections)
    undervisning = sections.get("Undervisning", "Ingen undervisning fundet")
    adgangskrav = sections.get("Adgangskrav", "Ingen adgangskrav fundet")
    optagelse = sections.get("Optagelse", "Ingen optagelse information fundet")
    uddannelsessteder = sections.get("Uddannelsessteder", "Ingen uddannelsessteder fundet")
    # Find the section that contains "adgangskvotienter"
    oekonomi = sections.get("Økonomi", "Ingen økonomi fundet")
    fremtidsmuligheder = sections.get("Fremtidsmuligheder", "Ingen fremtidsmuligheder fundet")
    love_og_regler = sections.get("Love og regler", "Ingen love og regler fundet")
    adgangskvotienter = sections.get("Adgangskvotienter 2024", "Ingen adgangskvotienter fundet")
    
    # Add the new columns to the DataFrame
    df.at[index, 'Introduktion'] = sections.get("Introduktion", "Ingen introduktion fundet")
    df.at[index, 'undervisning'] = undervisning
    df.at[index, 'adgangskrav'] = adgangskrav
    df.at[index, 'optagelse'] = optagelse
    df.at[index, 'uddannelsessteder'] = uddannelsessteder
    df.at[index, 'økonomi'] = oekonomi
    df.at[index, 'fremtidsmuligheder'] = fremtidsmuligheder
    df.at[index, 'love_og_regler'] = love_og_regler
    df.at[index, 'adgangskvotienter'] = adgangskvotienter
    

    
# Save the updated DataFrame to a new CSV file'
df.to_csv("uddannelser_full.csv", index=False, encoding="utf-8")
print(f"Saved updated DataFrame to uddannelser_full.csv")