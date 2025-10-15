# Hybrid Movie Recommender (Prototype)

This repository contains a modular, runnable prototype of a hybrid movie recommender
combining **User-based Collaborative Filtering (CF)** and **Content-Based Filtering (CB)**,
with a Hybrid combiner and a popularity-based cold-start fallback.

## Structure
- `hybrid_recommender/`
  - `data.py` — creates movie database and synthetic user ratings
  - `cf.py` — CollaborativeFiltering class (user-based cosine similarity)
  - `cb.py` — ContentBasedFiltering class (binary genre vectors + cosine)
  - `hybrid.py` — HybridRecommender combining CF and CB
  - `utils.py` — helper functions for display and analysis
  - `main.py` — example run / CLI entrypoint
- `requirements.txt` — required Python packages
- `.gitignore` — recommended ignores
- `LICENSE` — MIT License

## Quickstart (local)
1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the example:
   ```bash
   python -m hybrid_recommender.main
   ```
4. Outputs (`movie_database.csv`, `user_ratings.csv`, `sample_recommendations.csv`) will be
   created in the current working directory after the script runs.

## Notes
- This is a prototype meant for education, demos, or as a starting point for productionization.
- See `README.md` sections for suggested improvements (SVD, implicit feedback, ANN).