import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Indlæs data og embeddings
df = pd.read_csv("match_ready.csv")
embeddings = np.load("uddannelse_embeddings.npy")

# Initialiser samme model som ved embedding
print("Indlæser transformer...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Brugerinput: Midlertidig i test-fase
user_input = input("Hvad er du interesseret i? Skriv lidt om dine taniker og ønsker til fremtiden:\n")

# Embed brugerens input
user_embeddings = model.encode([user_input])

# Beregn cosine similarity mellem brugerens input og uddannelserne
similarities = cosine_similarity(user_embeddings, embeddings)[0]

# Find de 5 mest relevante uddannelser
top_n = 5
top_indices = similarities.argsort()[::-1][:top_n]

# Vis resultaterne
print("\nDe mest relevante uddannelser for dig er:")
for idx in top_indices:
    match = df.iloc[idx]
    score = similarities[idx]
    print(f"{match['titel']} ({match['kategori']})")
    print(f"Match score: {score:.2%}")
    print(f"Link: {match['url']}\n")