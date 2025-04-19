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
load_dotenv(".env")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

if not DEEPSEEK_API_KEY:
    raise ValueError("API key for DeepSeek is not set in the environment variables.")

# Load cleaned data
# Load full augmented dataset
df_all = pd.read_csv("core/data/augmented_data.csv")

# Split into success and failed rows
failed_df = df_all[df_all["augmented_text"].str.contains("[Fejl: Exception]", na=False, regex=False)].copy().reset_index(drop=True)
ok_df = df_all[~df_all["augmented_text"].str.contains(r"\[Fejl: Exception\]", na=False, regex=True)].copy()


print(f"🔍 Fundet {len(failed_df)} rækker med fejl – genkører nu kun disse...")


# Prompt
def build_prompt(row):
    return f"""
Du er en studievejleder med speciale i at forklare uddannelser til gymnasieelever, som skal vælge en bacheloruddannelse.
Du får nu oplysninger om en dansk bacheloruddannelse fra UddannelsesGuiden (UG.dk). Ud fra disse oplysninger skal du skrive en kort, flydende og elevvenlig tekst på maks 520 tokens, som egner sig til semantisk matching mod en gymnasieelevs fritekstbeskrivelse af fag, interesser og arbejdsformer.
✳️ Format: Du skal skrive én sammenhængende tekst uden overskrifter eller punktopstillinger. Du må ikke bruge markdown. Du må gerne skrive i et levende og relaterbart sprog, men aldrig for langt.
🔍 Formål: Teksten skal hjælpe en gymnasieelev med at forstå, hvad man laver på uddannelsen, hvordan man arbejder, hvilke fag/interesser der matcher, og hvad man typisk kan blive.
✅ Du skal inkludere:
- Hvilke fag/interesser passer til denne uddannelse (f.eks. matematik, samfundsfag, formidling…)
- Hvordan man arbejder (f.eks. gruppearbejde, laboratorie, dataanalyse, feltarbejde…)
- Hvilke metoder og emner man møder (f.eks. statistik, argumentation, kulturforståelse, eksperimenter…)
- Hvad man typisk kan blive, og hvor man arbejder bagefter (f.eks. UX-designer, lærer, biolog)
- Hvordan man typisk er som person, hvis man vælger den
- Brug gerne vendinger som “Du vil trives her hvis…” eller “Denne uddannelse er oplagt for dig der elsker…”
❌ Du må ikke:
- Skrive mere end 520 tokens
- Bruge punktopstillinger, overskrifter eller listeform
- Bruge teknisk sprog fra UG.dk direkte
- Referere til kolonnenavne
- Bruge markdown
Her er oplysningerne om uddannelsen:
Titel: {row["titel"]}
Kategori: {row["kategori"]}
Introduktion: {row["Introduktion"]}
Undervisning: {row["undervisning"]}
Fremtidsmuligheder: {row["fremtidsmuligheder"]}
"""

# 🔌 Async API-kald
# Async call
async def get_augmented_text(client, row, index, semaphore, max_retries=3):
    async with semaphore:
        for attempt in range(max_retries):
            try:
                prompt = build_prompt(row)
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
                        "max_tokens": 550,
                    },
                    timeout=60.0
                )

                await asyncio.sleep(1.5)  # 🔁 Lidt længere pause for stabilitet

                if response.status_code != 200:
                    print(f"❌ Fejl {response.status_code} for '{row['titel']}': {response.text}")
                    continue  # Prøv igen

                content = response.json()["choices"][0]["message"]["content"]
                return index, content
            except Exception as e:
                print(f"❌ Undtagelse (forsøg {attempt+1}) for '{row['titel']}': {e}'")
                await asyncio.sleep(2.5)  # Vent lidt mere før retry
        return index, "[Fejl: Exception]"  # Alle forsøg fejlede


# Async loop
async def augment_data(failed_rows):
    results = [None] * len(failed_rows)
    semaphore = asyncio.Semaphore(2)

    async with httpx.AsyncClient() as client:
        tasks = [get_augmented_text(client, row, i, semaphore) for i, row in failed_rows.iterrows()]
        for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Genkører fejl"):
            index, content = await coro
            results[index] = content
    return results

# Main
def main():
    fixed_texts = asyncio.run(augment_data(failed_df))
    failed_df.loc[:, "augmented_text"] = fixed_texts


    final_df = pd.concat([ok_df, failed_df], ignore_index=True)
    final_df.to_csv("core/data/augmented_data.csv", index=False)
    print("✅ Fejlrettet data gemt.")

if __name__ == "__main__":
    main()