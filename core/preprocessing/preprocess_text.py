import json
import re
import pandas as pd
import numpy as np


df = pd.read_csv("data/uddannelser_full.csv")

df["combined_text"] = (
    df["titel"].fillna("") + "." +
    df["kategori"].fillna("") + "." +
    df["Introduktion"].fillna("") + "." +
    df["undervisning"].fillna("") + "." +
    df["fremtidsmuligheder"].fillna("")
).str.strip()


def remove_common_phrases(text):
    unwanted_phrases = [
        "du afslutter", "eksamen", "kan du læse videre", "karaktergennemsnit",
        "suppleringskurser", "kvote 1", "kvote 2", "Læs mere om", "gymnasial eksamen",
        "Læs om", "Uddannelsessteder", "studieophold", "uddannelsesstedet"
    ]
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        if not any(phrase.lower() in line.lower() for phrase in unwanted_phrases):
            cleaned.append(line)
    return " ".join(cleaned)

def emphasize_learning_phrases(text):
    # Beskyt forkortelser ved midlertidigt at erstatte dem
    protected_text = text.replace("bl.a.", "BLAA").replace("f.eks.", "FEKSEKS")

    # Udvidet mønster: fang sætninger med "Du lærer", "Du får", "Du kommer til" og behold hele sætningen op til rigtigt punktum
    important_sentences = re.findall(
        r"(Du\s+(?:lærer|kommer til|får|arbejder med|specialiserer dig i)\s+[^.!?]*[.!?])",
        protected_text,
        flags=re.IGNORECASE
    )

    # Genskab forkortelser i output
    important_sentences = [s.replace("BLAA", "bl.a.").replace("FEKSEKS", "f.eks.") for s in important_sentences]

    if important_sentences:
        text += "\n\nVigtige pointer:\n" + " ".join(important_sentences)
    return text

def clean_formatting(text):
    text = re.sub(r"https?://\S+", "", text)  # Fjern links
    text = re.sub(r"\s+", " ", text)  # Fjern ekstra whitespace
    return text.strip()

df["combined_text"] = df["combined_text"].apply(remove_common_phrases)
df["combined_text"] = df["combined_text"].apply(emphasize_learning_phrases)
df["combined_text"] = df["combined_text"].apply(clean_formatting)


df_match = df[["titel", "kategori", "url", "combined_text"]].copy()
df_match.to_csv("data/match_ready.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    print("Preprocessing completed.")
    print("Match-ready data saved to match_ready.csv.")
    print("Sample text from row 70:")
    print(df_match.iloc[70]["combined_text"])

