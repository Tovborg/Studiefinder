# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
import traceback
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load data and model

df = pd.read_csv("../core/uddannelser_full.csv")
embeddings = np.load("../core/uddannelse_embeddings.npy")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# FastAPI app
app = FastAPI(debug=True)

# Tillad frontend at tilgå API'et
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class MatchRequest(BaseModel):
    user_input: str
    top_n: int = 5

@app.post("/match")
def match_study(request: MatchRequest):
    """
    Match the user's input with the study programs based on cosine similarity.
    """
    print("Received request:", request.dict())
    try:
        user_embedding = model.encode([request.user_input])
        similarity = cosine_similarity(user_embedding, embeddings)[0]
        top_indices = similarity.argsort()[::-1][:request.top_n]

        matches = []
        for idx in top_indices:
            matches.append({
                "titel": df.iloc[idx]["titel"],
                "beskrivelse": df.iloc[idx]["Introduktion"],
                "url": df.iloc[idx]["url"],
                "match_score": round(float(similarity[idx]), 4)
            })
        
        return {"matches": matches}
    
    except Exception as e:
        # Log the error for debugging
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))