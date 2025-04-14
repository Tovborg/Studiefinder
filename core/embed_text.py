import requests
import json
# import beautifulsoup4
from bs4 import BeautifulSoup
import re
import os
import pandas as pd

df = pd.read_csv("uddannelser_full.csv")

df["combined_text"] = (
    df["Introduktion"].fillna("") + "\n\n" +
    df["undervisning"].fillna("") + "\n\n" +
    df["adgangskrav"].fillna("") + "\n\n" +
    df["fremtidsmuligheder"].fillna("")
).str.strip()

df_match = df[["titel", "kategori", "url", "combined_text"]].copy()
df_match.to_csv("match_ready.csv", index=False, encoding="utf-8")

import numpy as np
from sentence_transformers import SentenceTransformer

print("Indlæser transformer...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Embed kombineret tekst
print("Genererer embeddings...")
embeddings = model.encode(df_match["combined_text"].tolist(), show_progress_bar=True)

# Gem embeddings til fil
print("Gemmer embeddings...")
np.save("uddannelse_embeddings.npy", embeddings)
print("Embeddings gemt som uddannelse_embeddings.npy")