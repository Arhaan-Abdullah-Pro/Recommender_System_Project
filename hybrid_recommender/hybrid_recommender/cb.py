import numpy as np
from collections import defaultdict

class ContentBasedFiltering:
    """Content-based filtering using binary genre vectors and cosine similarity."""

    def __init__(self, movies_df):
        self.movies_df = movies_df.copy()
        self.genre_profiles = {}
        self.build_genre_profiles()

    def build_genre_profiles(self):
        all_genres = set()
        for g in self.movies_df['genre']:
            all_genres.update(g.split('|'))
        self.all_genres = sorted(list(all_genres))
        for _, row in self.movies_df.iterrows():
            movie_id = int(row['movie_id'])
            genres = row['genre'].split('|')
            vec = [1 if gg in genres else 0 for gg in self.all_genres]
            self.genre_profiles[movie_id] = np.array(vec, dtype=float)

    def calculate_movie_similarity(self, m1, m2):
        v1 = self.genre_profiles.get(int(m1))
        v2 = self.genre_profiles.get(int(m2))
        if v1 is None or v2 is None:
            return 0.0
        dot = float(np.dot(v1, v2))
        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)
        if n1 == 0 or n2 == 0:
            return 0.0
        return dot / (n1 * n2)

    def recommend_similar_movies(self, movie_id, n=10):
        sims = []
        for mid in self.genre_profiles:
            if mid == int(movie_id):
                continue
            sims.append((mid, self.calculate_movie_similarity(movie_id, mid)))
        sims.sort(key=lambda x: x[1], reverse=True)
        return sims[:n]

    def recommend_for_user(self, user_rated_movies, ratings_df, n=10):
        # user_rated_movies: list of (movie_id, rating)
        high_rated = [(m,r) for m,r in user_rated_movies if r >= 4.0]
        if not high_rated:
            high_rated = user_rated_movies
        movie_scores = defaultdict(float)
        movie_counts = defaultdict(int)
        user_movies = set([m for m,_ in user_rated_movies])
        for movie_id, user_rating in high_rated:
            similar = self.recommend_similar_movies(movie_id, n=20)
            for mid, sim in similar:
                if mid in user_movies:
                    continue
                movie_scores[mid] += sim * user_rating
                movie_counts[mid] += 1
        recs = []
        for mid, score in movie_scores.items():
            if movie_counts[mid] > 0:
                recs.append((mid, float(score / movie_counts[mid])))
        recs.sort(key=lambda x: x[1], reverse=True)
        return recs[:n]