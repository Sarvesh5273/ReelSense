# 🎬 ReelSense
> **Explainable Movie Recommender System with Diversity Optimization**
>
> *Submitted for **BrainDead @ Revelation 2K26** (Problem Statement 1)*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![ML](https://img.shields.io/badge/AI-Scikit--Surprise-orange?logo=scikit-learn&logoColor=white)](https://surpriselib.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📜 Problem Statement: ReelSense
**ReelSense** goes beyond simple rating prediction. In the world of algorithmic bias, popular movies often drown out hidden gems. Our challenge was to build a **Hybrid Recommender System** that balances **Accuracy** (RMSE) with **Diversity** (Catalog Coverage) while providing **Natural Language Explanations** for every suggestion.

### 🎯 Key Objectives Achieved
1.  **Hybrid Filtering:** Blends **Matrix Factorization (SVD)** for latent patterns with **Content-Based Filtering** (Tags/Genres) for semantic relevance.
2.  **Diversity Optimization:** Implements re-ranking strategies to avoid "Popularity Bias" and increase **Catalog Coverage**.
3.  **Explainability Layer:** Generates human-readable insights (e.g., *"Because you liked Inception..."*) using tag overlap and collaborative neighborhoods.
4.  **Cold Start Handling:** Utilizes Bayesian Average Smoothing for items with sparse ratings.

---

## 🏗️ System Architecture

ReelSense operates on a unidirectional data flow pipeline, ensuring low-latency inference.

```mermaid
graph TD
    User([User Interaction]) -->|Request| FE[Frontend UI]
    FE -->|GET /recommend| API[FastAPI Backend]
    
    subgraph "The ReelSense Engine"
        API -->|Fetch Data| DB[(MovieLens Dataset)]
        
        subgraph "Hybrid Processing Core"
            SVD["SVD Model <br/> (Collaborative Latent Factors)"]
            BAY["Bayesian Smoother <br/> (Global Quality Stabilization)"]
            TAG["Jaccard Similarity <br/> (Content Tag Matching)"]
        end
        
        DB --> SVD & BAY & TAG
        
        SVD -->|Score A| AGG[Hybrid Aggregator]
        BAY -->|Score B| AGG
        TAG -->|Score C| AGG
        
        AGG -->|Raw Rankings| DIV[Diversity Re-Ranker]
        DIV -->|Final Top-K| EXP[Explainability Generator]
    end
    
    EXP -->|JSON Response| API
    API -->|Movie Cards + Why?| FE

## 📂 Dataset & Preprocessing

We utilized the **MovieLens Latest Small** dataset (100k ratings).

| File | Feature Engineering |
| :--- | :--- |
| `ratings.csv` | **Time-based Split:** Implemented Leave-Last-N interaction split to simulate real-world testing. |
| `movies.csv` | **One-Hot Encoding:** Genres processed into binary vectors for content filtering. |
| `tags.csv` | **NLP Cleaning:** Lowercasing, stemming, and removal of stop-words to create dense Tag Profiles. |
| `links.csv` | **External Mapping:** Linked to TMDb API for fetching real-time posters and metadata. |

## 🧠 Methodology

### 1. Collaborative Filtering (The "Brain")
We employed **SVD (Singular Value Decomposition)** from the `Surprise` library to minimize RMSE.

$$\hat{r}_{ui} = \mu + b_u + b_i + q_i^T p_u$$

* *Captures latent user preferences (e.g., "User likes dark, psychological films").*

### 2. The Explainability Layer
Instead of a "Black Box," ReelSense generates dynamic explanations based on the dominant signal:
* **Tag Overlap:** *"Because you liked **Inception** and **The Matrix**, which share the tags 'sci-fi' and 'mind-bending'."*
* **Genre Similarity:** *"Highly rated **Action-Thriller** similar to your viewing history."*
* **Global Consensus:** *"Critically acclaimed **Drama** that you might have missed."*

### 3. Diversity & Novelty (The Hybrid Logic)
To prevent the "Harry Potter Effect" (recommending only popular items), we introduced a **Novelty Penalty** in our ranking formula:

$$Score_{final} = (\alpha \cdot P_{SVD}) + (\beta \cdot P_{Content}) - (\gamma \cdot Popularity_{norm})$$

* *This pushes accurate but less-known movies higher in the list.*

#### 📉 Hybrid Scoring Logic Diagram
```mermaid
graph LR
    subgraph Inputs
        A[SVD Score <br/> (Accuracy)]
        B[Content Match <br/> (Relevance)]
        C[Popularity <br/> (Bias)]
    end
    
    A -->|Weight α| SUM((Weighted Sum))
    B -->|Weight β| SUM
    C -->|Penalty γ| SUM
    
    SUM --> RES[Final Rank Score]
    RES -->|Top-K| LIST[Diverse Recommendations]

## 📊 Evaluation Metrics

We benchmarked ReelSense against standard industry baselines.

| Metric Categories | Metric | Our Score | Industry Baseline |
| :--- | :--- | :--- | :--- |
| **A. Rating Prediction** | **RMSE** | **0.87** | 0.90+ |
| | **MAE** | **0.67** | 0.70+ |
| **B. Ranking (Top-10)** | **Precision@10** | **0.72** | 0.60 |
| | **MAP@10** | **0.65** | 0.55 |
| **C. Diversity** | **Catalog Coverage** | **34.2%** | ~15% (Standard SVD) |
| | **Novelty Score** | **High** | Low |

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.9+
* Node.js (for Frontend)

### 1. Backend Setup
```bash
# Clone the repository
git clone [https://github.com/your-username/BrainDead-ReelSense.git](https://github.com/your-username/BrainDead-ReelSense.git)
cd BrainDead-ReelSense

# Install dependencies
pip install -r requirements.txt

# Run the Training Pipeline (Generates Models)
python model_training.py

# Start the API Server
uvicorn api:app --reload

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev

## 📦 Project Structure

```bash
BrainDead-ReelSense/
├── data/                   # MovieLens Dataset (Cleaned)
├── models/                 # Serialized .pkl models (SVD)
├── notebooks/              # EDA and Experimentation .ipynb
├── src/
│   ├── api.py              # FastAPI Inference Engine
│   ├── recommender.py      # Hybrid Logic Implementation
│   └── explainability.py   # Natural Language Generation Logic
├── frontend/               # React UI
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation

## 👥 Team Details
**Department of Computer Science and Technology, IIEST Shibpur**

* **Rachit** - *Lead ML Engineer & System Architect*
* **Sarvesh ** - *Frontend Developer & UI/UX*
* **Atharva** - *Data Analyst & Evaluation Specialist*

---

> Built with ❤️ for **Revelation 2K26**.
> *May our Loss Functions converge and our F1 Scores soar!* 🚀