import os
import pandas as pd
import asyncio
import httpx
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../../.env"))

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

if not DEEPSEEK_API_KEY:
    raise ValueError("API key for DeepSeek is not set in the environment variables.")

# Load cleaned data
df = pd.read_csv(os.path.join(BASE_DIR, "../data/augmented_data_cleaned.csv"))
rows = df.to_dict(orient="records")

# Prompt template
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

# Async call to API
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
            timeout=90.0
        )
        if response.status_code != 200:
            print(f"❌ Fejl {response.status_code} for '{row['titel']}': {response.text}")
            return index, "[Fejl: Ingen svar]"

        content = response.json()["choices"][0]["message"]["content"]
        return index, content

    except Exception as e:
        print(f"❌ Fejl for '{row['titel']}': {e}")
        return index, "[Fejl: Exception]"

# Async runner in batches
BATCH_SIZE = 5
BATCH_DELAY = 3

async def augment_all_rows(rows):
    results = [None] * len(rows)
    async with httpx.AsyncClient() as client:
        for i in tqdm(range(0, len(rows), BATCH_SIZE), desc="🚀 Augmentering i batches"):
            batch = rows[i:i + BATCH_SIZE]
            tasks = [get_augmented_text(client, row, i + idx) for idx, row in enumerate(batch)]
            batch_results = await asyncio.gather(*tasks)

            for index, result in batch_results:
                results[index] = result

            await asyncio.sleep(BATCH_DELAY)
    return results

# Main
def main():
    print("🚀 Starter DeepSeek-data-augmentering...")
    augmented_texts = asyncio.run(augment_all_rows(rows))
    df["final_augmented_text"] = augmented_texts
    out_path = os.path.join(BASE_DIR, "../data/deep_augmented_data.csv")
    df.to_csv(out_path, index=False)
    print("✅ Gemte deep_augmented_data.csv")

main()

