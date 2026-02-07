from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle

app = FastAPI()

# -------------------------------
# CORS (for React)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Load data + model
# -------------------------------
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")

movies["genre_list"] = movies["genres"].apply(
    lambda x: [] if x == "(no genres listed)" else x.split("|")
)

with open("svd_model.pkl", "rb") as f:
    svd_model = pickle.load(f)

# -------------------------------
# Recommendation logic
# -------------------------------
def recommend(user_id: int, top_k: int):
    watched = set(
        ratings[ratings["userId"] == user_id]["movieId"]
    )

    rows = []
    for _, movie in movies.iterrows():
        if movie["movieId"] in watched:
            continue

        pred = svd_model.predict(user_id, movie["movieId"])

        rows.append({
            "movieId": int(movie["movieId"]),
            "title": movie["title"],
            "predicted_rating": round(pred.est, 2),
            "match_percentage": min(round(pred.est / 5 * 100, 1), 95),
            "explanation": "Recommended based on similar users and genres."
        })

    rows = sorted(rows, key=lambda x: x["predicted_rating"], reverse=True)
    return rows[:top_k]

# -------------------------------
# API endpoints
# -------------------------------
@app.get("/")
def root():
    return {
        "message": "ReelSense backend running",
        "endpoints": ["/recommendations"]
    }

@app.get("/recommendations")
def get_recommendations(user_id: int, top_k: int = 10):
    return recommend(user_id, top_k)
