import os
import subprocess
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# # Slet gamle filer hvis de findes
# if os.path.exists("data/match_ready.csv"):
#     print("🗑️ Sletter tidligere match_ready.csv...")
#     os.remove("data/match_ready.csv")

if os.path.exists("embeddings/uddannelse_embeddings_mpnet.npy"):
    print("🗑️ Sletter tidligere embeddings...")
    os.remove("embeddings/uddannelse_embeddings_mpnet.npy")

# # Kør preprocessing-script
# print("⚙️ Kører preprocess_text.py...")
# subprocess.run(["python3", "preprocess_text.py"], check=True)

# Indlæs data
print("📄 Indlæser nyt augmented_data.csv...")
df = pd.read_csv("data/deep_augmented_data_final_boosted.csv")

# Indlæs model
print("🤖 Indlæser transformer model...")
model = SentenceTransformer("all-mpnet-base-v2")

# Generér embeddings
print("🧠 Genererer embeddings...")
# embeddings = model.encode(df["combined_text"].tolist(), show_progress_bar=True)
embeddings = model.encode(df["final_augmented_text"].tolist(), show_progress_bar=True)

# Gem embeddings
print("💾 Gemmer embeddings...")
np.save("embeddings/uddannelse_embeddings_mpnet.npy", embeddings)
print("✅ Embeddings gemt som uddannelse_embeddings_mpnet.npy")
