from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle
import numpy as np
from numpy.linalg import norm

app = FastAPI()

# -------------------------------
# CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Load Data & Model
# -------------------------------
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")
tags = pd.read_csv("tags.csv")

# Pre-process genres
movies["genre_list"] = movies["genres"].apply(
    lambda x: [] if x == "(no genres listed)" else x.split("|")
)

with open("svd_model.pkl", "rb") as f:
    svd_model = pickle.load(f)

# -------------------------------
# HELPER: Cosine Similarity
# -------------------------------
def compute_cosine_match(user_id, movie_id):
    """
    Calculates the geometric angle between the User Vector and Movie Vector.
    Returns a percentage (0-100%).
    """
    try:
        # 1. Convert Raw IDs to Internal Model IDs
        inner_uid = svd_model.trainset.to_inner_uid(user_id)
        inner_iid = svd_model.trainset.to_inner_iid(movie_id)
        
        # 2. Extract the Latent Vectors (The "Brain" Data)
        user_vector = svd_model.pu[inner_uid]
        movie_vector = svd_model.qi[inner_iid]
        
        # 3. Compute Cosine Similarity
        # formula: (A . B) / (||A|| * ||B||)
        dot_product = np.dot(user_vector, movie_vector)
        magnitude = norm(user_vector) * norm(movie_vector)
        
        if magnitude == 0: return 50.0 # Neutral fallback
        
        cosine_sim = dot_product / magnitude
        
        # 4. Map -1.0 to 1.0 scale -> 0% to 100%
        # -1 (Opposite) -> 0%
        #  0 (Unrelated) -> 50%
        # +1 (Perfect)  -> 100%
        match_percentage = (cosine_sim + 1) / 2 * 100
        
        return round(match_percentage, 1)

    except ValueError:
        # ID not in training set (Cold start)
        return 50.0

# -------------------------------
# Recommendation Logic
# -------------------------------
def recommend(user_id: int, top_k: int):
    # 1. User History
    user_ratings = ratings[ratings["userId"] == user_id]
    watched_ids = set(user_ratings["movieId"])
    
    # 2. Filter Candidates
    candidate_movies = movies[~movies["movieId"].isin(watched_ids)]
    
    predictions = []

    # 3. Process Candidates (No Randomness, Pure Math)
    # We look at the top candidates the model predicts heavily
    for row in candidate_movies.itertuples(index=False):
        try:
            # A. PREDICTED RATING (The Quality Score)
            # This uses Bias + Dot Product
            pred = svd_model.predict(user_id, row.movieId)
            est = pred.est

            # Filter: Only consider "Good" movies
            if est < 3.0: continue

            # B. MATCH PERCENTAGE (The Taste Score)
            # This uses PURE Vector Similarity (Cosine)
            match_score = compute_cosine_match(user_id, row.movieId)

            # C. EXPLAINABILITY (Hackathon Req)
            # Simple genre explanation
            genre = row.genre_list[0] if row.genre_list else "Movies"
            
            # Logic: High Rating but Low Match? -> "Critically Acclaimed"
            # Logic: High Rating AND High Match? -> "Perfect for you"
            if match_score > 80:
                explanation = f"Exact match for your taste in {genre}."
            elif match_score > 50:
                explanation = f"Highly rated {genre} film you might like."
            else:
                explanation = f"Critically acclaimed {genre} film."

            predictions.append({
                "movieId": row.movieId,
                "title": row.title,
                "predicted_rating": round(est, 2),    # e.g., 4.12
                "match_percentage": match_score,      # e.g., 53.4% (Real Vector Math)
                "explanation": explanation
            })
        except:
            continue

    # 4. Sort Strategy
    # We sort by Rating (Quality) first, but you can see the Match % variance
    predictions.sort(key=lambda x: x["predicted_rating"], reverse=True)
    
    return predictions[:top_k]

# -------------------------------
# API Endpoints
# -------------------------------
@app.get("/")
def root():
    return {"message": "ReelSense Vector-Math API Running"}

@app.get("/recommendations")
def get_recommendations(user_id: int, top_k: int = 10):
    return recommend(user_id, top_k)