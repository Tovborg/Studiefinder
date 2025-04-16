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
df = pd.read_csv(os.path.join(BASE_DIR, "../data/deep_augmented_data.csv"))
df_full = df.copy()  # Corrections will be inserted into this copy
rows = df.to_dict(orient="records")

# Find rows with errors
error_mask = df["final_augmented_text"].str.contains(r"\[Fejl: Exception\]")
error_rows = df[error_mask].reset_index()
print(f"Antal rækker med fejl: {len(error_rows)}")

# Prompt
def build_prompt(text):
    return f"""
Du er en ekspert i AI og studievejledning. Her er en tekst, der beskriver en dansk bacheloruddannelse – den indeholder både introduktion, karriere, eksempler på elevinteresser, Google-søgninger og jobtitler:

{text}

Din opgave er at:

1. Udvælge og omskrive de mest relevante dele af teksten, så de bedst beskriver uddannelsens formål, typiske elevinteresser og karriereveje.

2. Skriv 3 korte og præcise sætninger, som en elev kunne sige, hvis de drømmer om denne uddannelse. Brug varieret og naturligt sprog – f.eks. "Jeg elsker at...", "Det lyder spændende at...", "Jeg interesserer mig for..."

3. Tilføj 2–3 unikke og realistiske jobtitler, man kan få med uddannelsen – ikke bare generelle som “konsulent” eller “formidler”, men så specifikt som muligt.

4. Tilføj 2 Google-søgninger, en nysgerrig elev kunne lave for at lære mere om feltet. Brug realistiske søgefraser og elev-ordvalg.

5. Nævn 2–3 konkrete fag eller projekter man typisk møder på uddannelsen, og beskriv kort hvilke brancher eller arbejdsområder uddannelsen typisk leder til.

Begræns output til **minimum 400 tokens og gerne tæt på 512**. Undgå at gentage ord fra inputteksten direkte – omskriv og fremhæv det vigtigste. Returner udelukkende selve tekstoutputtet uden overskrifter eller labels.
"""

# 🔌 Async API-kald
async def get_augmented_text(client, row, index):
    try:
        prompt = build_prompt(row["augmented_combined_text"])
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

# 🚀 Kør dem i batches
async def rerun_failed_rows(rows):
    results = [None] * len(rows)
    async with httpx.AsyncClient() as client:
        tasks = [get_augmented_text(client, row, i) for i, row in rows.iterrows()]
        for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="🔄 Retter fejl"):
            index, content = await coro
            results[index] = content
    return results

# 🧠 Main
def main():
    print("🔁 Retter tidligere fejl...")
    fixed_texts = asyncio.run(rerun_failed_rows(error_rows))

    # Indsæt dem tilbage i originalen
    for i, row in error_rows.iterrows():
        original_index = row["index"]
        df_full.at[original_index, "final_augmented_text"] = fixed_texts[i]

    # Gem hele datasættet igen
    df_full.to_csv(os.path.join(BASE_DIR, "../data/deep_augmented_data_final.csv"), index=False)
    print("✅ Gemte opdateret fil: deep_augmented_data_final.csv")

if __name__ == "__main__":
    main()