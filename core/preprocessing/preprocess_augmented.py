import json
import re
import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(SCRIPT_DIR, "../data/augmented_data.csv"))

# Lowercase alt for at sikre ens formatering
df["augmented_combined_text"] = df["augmented_combined_text"].str.lower()

# Fjern overskrifter og metadata
titles = [
    "titel:", "kategori:", "introduktion:", "undervisning:", 
    "karriere og fremtid:", "vigtige pointer:", 
    "### augmenteret beskrivelse:", "titel"
]
pattern = r"|".join([re.escape(title) for title in titles])
df["augmented_combined_text"] = df["augmented_combined_text"].str.replace(pattern, "", regex=True)

# Formatting of categories
kategori_mapping = {
    "Øvrige humaniora": "Humaniora",
    "Øvrige teknisk videnskab": "Teknisk videnskab",
    "Øvrige samfundsvidenskab": "Samfundsvidenskab",
    "Øvrige naturvidenskab": "Naturvidenskab",
    "Sundhedsvidenskabelige bacheloruddannelser": "Sundhedsvidenskab"
}



df["kategori"] = df["kategori"].replace(kategori_mapping)

# 2. Udskift kategoritekst inde i selve `augmented_combined_text`
for original, simplified in kategori_mapping.items():
    df["augmented_combined_text"] = df["augmented_combined_text"].str.replace(
        original.lower(), simplified.lower(), regex=False
    )

# Embedding-venlig formatering
def make_embedding_friendly(text):
    text = re.sub(r"###\s*\d\.\s*[^:\n]+:\s*", "", text)  # Fjern markdown overskrifter
    text = text.replace("*", "")  # Fjern punktform-markører
    text = re.sub(r"\s*\n\s*", " ", text)  # Fjern ny linje
    text = re.sub(r"\s+", " ", text)  # Fjern dobbelt whitespace
    return text.strip()

df["augmented_combined_text"] = df["augmented_combined_text"].apply(make_embedding_friendly)

# Fjern specialtegn undtagen typiske tegn
df["augmented_combined_text"] = df["augmented_combined_text"].str.replace(r"[^\w\s.,!?;:]", "", regex=True)

# Fjern uønsket redundans
redundant_text = [
    "bemærk der findes ikke en samlet oversigt over mulige kandidatuddannelser","bacheloruddannelsen","bacheloruddannelser",
    "bacheloruddannelse","bemærk", "sprog al undervisning foregår på engelsk", 
    "bachelor i", "der findes ikke en samlet oversigt over mulige kandidatuddannelser",
    "danmark", "uddannelsen", "uddanelser.", "uddannelse", "bachelor", "læs mere i ugartiklen:",
]
for text in redundant_text:
    df["augmented_combined_text"] = df["augmented_combined_text"].str.replace(text, "", regex=False)

# Fjern dobbelte punktummer og tilføj mellemrum efter punktummer, hvis nødvendigt
df["augmented_combined_text"] = df["augmented_combined_text"].str.replace(r"\.{2,}", ".", regex=True)
df["augmented_combined_text"] = df["augmented_combined_text"].str.replace(r"\.(?![\s.])", ". ", regex=True)

# Fjern gentagne ord
def remove_duplicate_words(text):
    return re.sub(r'\b(\w+)( \1\b)+', r'\1', text)

df["augmented_combined_text"] = df["augmented_combined_text"].apply(remove_duplicate_words)

# Til sidst: fjern alle overskydende mellemrum og trim tekst
df["augmented_combined_text"] = df["augmented_combined_text"].str.replace(r"\s+", " ", regex=True)
df["augmented_combined_text"] = df["augmented_combined_text"].str.strip()

print(df["augmented_combined_text"][180])
print(df["kategori"].unique())

from transformers import AutoTokenizer
# Indlæs tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-mpnet-base-v2")

tokenized_raw = tokenizer(df["augmented_combined_text"].tolist(), truncation=False)
token_lengths_raw = [len(tokens) for tokens in tokenized_raw["input_ids"]]

# Statistik
over_512 = sum(l > 512 for l in token_lengths_raw)
print(f"Antal tekster > 512 tokens: {over_512} / {len(token_lengths_raw)}")
print(f"Max token length: {max(token_lengths_raw)}")
print(f"Gennemsnitlig token længde (uden truncation): {sum(token_lengths_raw) / len(token_lengths_raw)}")

# Gem som ny ren CSV til embedding
output_path = os.path.join(SCRIPT_DIR, "../data/augmented_data_cleaned.csv")
df.to_csv(output_path, index=False)
print("✅ Renset data gemt som augmented_data_cleaned.csv")
