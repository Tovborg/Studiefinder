# Here we augment the "combined" column in the DataFrame with more formulations, keyword, phrases and so on.
import pandas as pd
import numpy as np
import re
from openai import OpenAI
import os
from dotenv import load_dotenv
# Async libraries
from tqdm.asyncio import tqdm_asyncio
import asyncio
import httpx
from tqdm import tqdm
import json

# Load environment variables from .env file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

if not DEEPSEEK_API_KEY:
    raise ValueError("API key for DeepSeek is not set in the environment variables.")

# Load data
df = pd.read_csv("data/match_ready.csv")
rows = df.to_dict(orient="records")  # Convert DataFrame to list of dictionaries

# Prompt template
def build_prompt(text):
    return f"""Du er en ekspert i studievejledning og sprogforståelse. Givet følgende studieinformation:

{text}

Beskriv:
1. Tre måder en gymnasieelev kunne formulere sine interesser, som matcher denne uddannelse.
2. Tre Google-søgninger en elev kunne finde på at lave.
3. To jobtitler man kan få med denne uddannelse.

Svar kort og præcist, men med variationer.
"""

# Asynchronous function to call the API
async def get_augmented_text(client, row, index):
    try:
        prompt = build_prompt(row["combined_text"])
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
                "max_tokens": 800,
            },
            timeout=60.0
        )
        res_json = response.json()
        content = res_json["choices"][0]["message"]["content"]
        return index, row["combined_text"] + "\n\n### Augmenteret beskrivelse:\n" + content

    except Exception as e:
        print(f"Fejl for '{row['titel']}':", e)
        return index, row["combined_text"] + "\n\n### Augmenteret beskrivelse:\n[Fejl: ingen svar]"

    
# Main async runner
BATCH_SIZE = 10
BATCH_DELAY = 2

async def augment_all_rows(rows):
    results = [None] * len(rows)  # Placeholder for korrekt rækkefølge
    async with httpx.AsyncClient() as client:
        for i in tqdm(range(0, len(rows), BATCH_SIZE), desc="🚀 Augmentering i batches"):
            batch = rows[i:i + BATCH_SIZE]
            tasks = [get_augmented_text(client, row, i + idx) for idx, row in enumerate(batch)]

            batch_results = await asyncio.gather(*tasks)

            for index, result in batch_results:
                results[index] = result

            await asyncio.sleep(BATCH_DELAY)  # Vent før næste batch

    return results
# Wrapper to run the async function
def main():
    print("🚀 Starter data augmentering...")
    augmented_texts = asyncio.run(augment_all_rows(rows))

    df_augmented = pd.DataFrame({
        "titel": [row["titel"] for row in rows],
        "kategori": [row["kategori"] for row in rows],
        "url": [row["url"] for row in rows],
        "augmented_combined_text": augmented_texts
    })

    # Save augmented data
    df_augmented.to_csv("data/augmented_data.csv", index=False, encoding="utf-8")
    print("Gemte augmented_data.csv")

if __name__ == "__main__":
    main()
    print("✅ Data augmentering færdig.")