import pandas as pd
import os
import asyncio
import httpx
from tqdm import tqdm
import re
import numpy as np
from dotenv import load_dotenv


# Load environment variables
# Load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../../.env"))

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

if not DEEPSEEK_API_KEY:
    raise ValueError("API key for DeepSeek is not set in the environment variables.")

# Load cleaned data
df = pd.read_csv(os.path.join(BASE_DIR, "../data/deep_augmented_data_final.csv"))
df_full = df.copy()  # Corrections will be inserted into this copy

# Filter for relevant categories
target_categories = ["Kunstneriske uddannelser", "Teknisk videnskab", "Ingeniørfag"]
domain_rows = df[df["kategori"].isin(target_categories)].reset_index()

# Prompt builder with domain emphasis
def build_prompt(text, category):
    if category == "Kunstneriske uddannelser":
        domain_focus = "Omskriv teksten, så den fremhæver, at dette er en *kunstnerisk* uddannelse. Læg vægt på kreativitet, æstetik, visuel tænkning og arbejdet med kunst og design. Brug ord og vendinger, der appellerer til elever med stærke kreative eller visuelle interesser. Du må gerne ændre formuleringer, men *behold alt det oprindelige indhold* – herunder elevudtalelser, jobtitler, Google-søgninger og fag. Tilføj ikke ny tekst eller nye afsnit."
    elif category in ["Ingeniørfag", "Teknisk videnskab"]:
        domain_focus = "Omskriv teksten, så den tydeligt fremhæver, at dette er en *teknisk* uddannelse. Læg vægt på anvendt teknologi, problemløsning, systemudvikling og ingeniørfaglige arbejdsmetoder. Brug et teknisk og præcist sprog, men bevar klarheden. Du må gerne ændre formuleringer, men *behold alt det oprindelige indhold* – herunder elevudtalelser, jobtitler, Google-søgninger og fag. Tilføj ikke ny tekst eller nye afsnit."
    else:
        raise ValueError("Unsupported category for domain boost")

    return f"""
Du er en sprogekspert og hjælper med at omskrive følgende tekst, så den er mere målrettet.

Tekst:
{text}

Opgave:
{domain_focus}

Svar kun med den omskrevne tekst – ingen forklaringer, ingen overskrifter.
"""

# API call
async def get_augmented_text(client, row, index):
    try:
        prompt = build_prompt(row["final_augmented_text"], row["kategori"])
        response = await client.post(
            DEEPSEEK_API_URL,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Du er en hjælpsom assistent"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 512,
            },
            timeout=60.0
        )
        if response.status_code != 200:
            print(f"❌ Fejl {response.status_code} for '{row['titel']}': {response.text}")
            return index, "[Fejl: Exception]"
        content = response.json()["choices"][0]["message"]["content"]
        return index, content
    except Exception as e:
        print(f"❌ Undtagelse for '{row['titel']}': {e}")
        return index, "[Fejl: Exception]"

# Async runner
async def boost_domain_rows(rows):
    results = [None] * len(rows)
    async with httpx.AsyncClient() as client:
        tasks = [get_augmented_text(client, row, i) for i, row in rows.iterrows()]
        for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="🎯 Kører domain-boosting"):
            index, content = await coro
            results[index] = content
    return results

# Run boost
boosted_texts = asyncio.run(boost_domain_rows(domain_rows))

# Update original dataframe
for i, row in domain_rows.iterrows():
    original_index = row["index"]
    df_full.at[original_index, "final_augmented_text"] = boosted_texts[i]

# Save updated dataset
output_path = os.path.join(BASE_DIR, "deep_augmented_data_final_boosted.csv")
df_full.to_csv(output_path, index=False)