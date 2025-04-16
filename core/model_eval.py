import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load Data
df = pd.read_csv("data/augmented_data.csv")
embeddings = np.load("embeddings/uddannelse_embeddings_mpnet.npy")

# Load Model
model = SentenceTransformer("all-mpnet-base-v2")

# Test Cases: prompt - forventede relevante uddannelser
test_cases = [
    {
        "prompt": "Jeg elsker teknologi og vil gerne lære at programmere. Jeg interesserer mig for computere og hvordan software fungerer.",
        "expected": ["Datalogi", "Softwareteknologi", "Datavidenskab og machine learning"]
    },
    {
        "prompt": "Jeg interesserer mig for kroppen og sundhed og kunne godt tænke mig at arbejde med mennesker og medicin.",
        "expected": ["Medicin", "Folkesundhedsvidenskab", "Medicinalbiologi"]
    },
    {
        "prompt": "Jeg er vild med sprog og vil gerne arbejde internationalt. Det kunne være fedt at lære om kultur og kommunikation.",
        "expected": ["International virksomhedskommunikation fremmedsprog", "Engelsk", "Sprog og internationale studier engelsk"]
    },
    {
        "prompt": "Jeg vil gerne arbejde med bæredygtighed og finde løsninger på klimaproblemer. Miljø og natur interesserer mig.",
        "expected": ["Miljøvidenskab", "Bæredygtig energiteknik", "Teknisk videnskab"]
    },
    {
        "prompt": "Jeg tænker meget over samfundet og politik og vil gerne forstå hvordan mennesker og stater fungerer.",
        "expected": ["Samfundsfag", "Statskundskab", "Sociologi"]
    },
]

results = []

for case in test_cases:
    user_embedding = model.encode([case["prompt"]])
    similarities = cosine_similarity(user_embedding, embeddings)[0]
    top_indices = similarities.argsort()[::-1][:5]
    top_titles = df.iloc[top_indices]["titel"].tolist()

    # Evaluer hvilke af de forventede der matcher
    matched = [
        title for title in top_titles
        if any(expected.lower() in title.lower() for expected in case["expected"])
    ]
    recall = len(matched) / len(case["expected"])

    results.append({
        "Prompt": case["prompt"],
        "Top 5 Matches": top_titles,
        "Expected": case["expected"],
        "Matched": matched,
        "Recall@5": round(recall, 2)
    })

# Output som tabel
results_df = pd.DataFrame(results)
results_df.to_csv("model_results/model_eval_results_2.csv", index=False, encoding="utf-8")
print(results_df)