# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import traceback
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from backend.database import init_db

# Load data and model

df = pd.read_csv("core/data/uddannelser_full.csv")
embeddings = np.load("core/embeddings/uddannelse_embeddings_mpnet.npy")
model = SentenceTransformer("all-mpnet-base-v2")

# FastAPI app
app = FastAPI(debug=True)
init_db()

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
        # Strip whitespace from user input
        user_input = request.user_input.strip()
        user_embedding = model.encode([user_input])
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
    
# Authentican with Google
from pydantic import BaseModel
import requests
# Import the database session
from backend.models import SessionLocal, User
from sqlalchemy.orm import Session


# Model for the request data
class Token(BaseModel):
    access_token: str

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/auth/google")
def google_login(data: Token, db: Session = Depends(get_db)):
    userinfo_endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {data.access_token}"}
    response = requests.get(userinfo_endpoint, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    data = response.json()
    email = data.get("email")
    sub = data.get("sub")

    if not email:
        raise HTTPException(status_code=400, detail="missing email in user info")
    
    print("User info:", data)

    # Check if user exists in the database
    user = db.query(User).filter(User.google_sub == sub).first()
    if not user:
        # Create a new user if one doesn't exist
        user = User(
            email=email,
            name=data.get("name"),
            google_sub=sub,
            picture=data.get("picture"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print("New user created:", user)
    else: 
        print("User already exists:", user)
    
    # Return user info
    return {
                "message": "Login Successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "picture": user.picture,
                }
            }
