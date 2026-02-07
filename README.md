# 🎬 ReelSense
> **"Not just a recommendation. A revelation."**

[![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=black)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/ML-Scikit--Surprise-3776AB?logo=python&logoColor=white)](https://surpriselib.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Overview
**ReelSense** is a next-generation **Hybrid Recommendation Engine** built for **Revelation 2K26 (Problem Statement 1)**.

Unlike traditional "Black Box" recommenders that simply output a list of movies, ReelSense prioritizes **Explainability**. It uses a novel **3-Tier Hybrid Architecture** combining **Matrix Factorization (SVD)**, **Bayesian Statistical Smoothing**, and **Content-Based Filtering** to deliver hyper-personalized results with natural language explanations.

---

## 🌟 Key Features

* **🧠 Hybrid Intelligence:** Fuses Latent User Vectors (SVD) with Global Group Patterns (Bayesian Average) for statistically robust predictions.
* **🔍 "Prism" Explainability Layer:** Every recommendation comes with a dynamic "Why?" insight (e.g., *"Recommended because you like 'Twist Ending' movies"*).
* **⚡ Real-Time Vector Math:** Computes Cosine Similarity on 100-dimensional latent vectors in <200ms.
* **🎨 Cinematic UI:** A responsive, dark-mode interface built with **React + Tailwind CSS**, featuring dynamic poster fetching via **TMDB API**.
* **🛡️ Cold-Start Protection:** Uses Bayesian Smoothing to ensure niche movies are treated fairly against blockbusters.

---

## 🏗️ System Architecture

ReelSense operates on a unidirectional data flow pipeline, ensuring low-latency inference.

```mermaid
graph TD
    User([User]) -->|Request| FE[React Frontend]
    FE -->|GET /recommend| API[FastAPI Backend]
    
    subgraph "The ReelSense Engine"
        API -->|Fetch History| DB[(Dataset)]
        
        subgraph "Parallel Processing"
            SVD[SVD Model\n(Personal Taste)]
            BAY[Bayesian Smoother\n(Global Quality)]
            TAG[Jaccard Index\n(Content Match)]
        end
        
        DB --> SVD & BAY & TAG
        
        SVD -->|Score A| AGG[Hybrid Aggregator]
        BAY -->|Score B| AGG
        TAG -->|Score C| AGG
        
        AGG -->|Final Rank| PRISM[Prism Explanation Logic]
    end
    
    PRISM -->|JSON Response| API
    API -->|Movie Cards| FE

🧮 The "Secret Sauce" (Math)We don't guess. We calculate. ReelSense uses a weighted linear equation to balance Personalization vs. Quality.1. The Hybrid Score Formula$$ Score_{final} = (0.7 \cdot P_{SVD}) + (0.3 \cdot P_{Global}) + Bonus_{Tag} $$$P_{SVD}$: The dot product of the User Vector and Item Vector ($p_u \cdot q_i$).$P_{Global}$: A Bayesian Weighted Average to stabilize ratings for sparse items.$Bonus_{Tag}$: A Jaccard Similarity boost derived from semantic tag overlap.2. Match Percentage (Cosine Similarity)$$ Similarity = \frac{A \cdot B}{||A|| \cdot ||B||} $$We calculate the geometric angle between your "Taste Vector" and the "Movie Vector" to generate a percentage match (e.g., 96.4% Match).💻 Tech StackComponentTechnologyRoleFrontendReact.js, Tailwind CSS, Framer MotionInteractive UI & AnimationsBackendFastAPI, UvicornHigh-performance Inference APIML EngineScikit-Surprise, NumPy, PandasMatrix Factorization & Vector MathDataMovieLens Small DatasetTraining Data (100k ratings)VisualsTMDB APIReal-time Posters & Metadata🛠️ Installation & SetupFollow these steps to run ReelSense locally.PrerequisitesNode.js (v16+)Python (v3.9+)TMDB API Key (Free)1. Backend SetupBash# Clone the repository
git clone [https://github.com/yourusername/reelsense.git](https://github.com/yourusername/reelsense.git)
cd reelsense

# Install Python dependencies
pip install fastapi uvicorn pandas numpy scikit-surprise

# Train the "Brain" (Generates svd_model.pkl)
python model_training.py

# Start the Server
uvicorn api:app --reload
Server runs at: http://127.0.0.1:80002. Frontend SetupBash# Open a new terminal and navigate to frontend
cd frontend

# Install Node modules
npm install

# Configure API Key
# Create a .env file and add: VITE_TMDB_API_KEY=your_key_here

# Start the UI
npm run dev
Client runs at: http://localhost:5173📸 ScreenshotsHome PageAI Insights(Note: Replace placeholder links with actual screenshots of your running app)🔮 Future ScopeNeural Collaborative Filtering (NCF): Replacing SVD with Deep Learning for non-linear pattern recognition.LLM Integration: Connecting the "Prism" layer to GPT-4 for paragraph-length movie analysis.Social Graph: Adding "Watch Parties" based on vector similarity between two different users.👥 ContributorsSarvesh - Lead Developer & ML Engineer[Teammate Name] - Frontend Architect[Teammate Name] - Data Scientist⚖️ LicenseThis project is licensed under the MIT License - see the LICENSE file for details.Built with ❤️ for Revelation 2K26.