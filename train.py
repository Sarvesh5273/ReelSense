import pandas as pd
import pickle
from surprise import Dataset, Reader, SVD

# 1. Load your data
print("Loading datasets...")
ratings = pd.read_csv("ratings.csv")

# 2. Configure the Reader (Rating scale is 0.5 to 5.0)
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[["userId", "movieId", "rating"]], reader)

# 3. Train the SVD Model (The "Brain")
print("Training SVD Model (Calculating Vectors)...")
# We use all available data to build the best possible model
trainset = data.build_full_trainset()

# n_factors=100 means we create a vector of size 100 for every user and movie
model = SVD(n_factors=100, random_state=42) 
model.fit(trainset)

# 4. Save the Model
print("Saving model to 'svd_model.pkl'...")
with open("svd_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Success! You can now restart your API.")