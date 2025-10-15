import numpy as np
from collections import defaultdict

class CollaborativeFiltering:
    """User-based collaborative filtering using cosine similarity."""

    def __init__(self, ratings_df):
        self.ratings_df = ratings_df.copy()
        self.user_movie_matrix = None
        self.build_matrix()

    def build_matrix(self):
        self.user_movie_matrix = self.ratings_df.pivot_table(
            index='user_id', columns='movie_id', values='rating'
        ).fillna(0)

    def calculate_user_similarity(self, user1, user2):
        user1_ratings = self.user_movie_matrix.loc[user1].values
        user2_ratings = self.user_movie_matrix.loc[user2].values
        mask = (user1_ratings > 0) & (user2_ratings > 0)
        if mask.sum() == 0:
            return 0.0
        dot = np.dot(user1_ratings[mask], user2_ratings[mask])
        n1 = np.linalg.norm(user1_ratings[mask])
        n2 = np.linalg.norm(user2_ratings[mask])
        if n1 == 0 or n2 == 0:
            return 0.0
        return float(dot / (n1 * n2))

    def find_similar_users(self, target_user, n=5):
        similarities = []
        for user in self.user_movie_matrix.index:
            if user == target_user:
                continue
            sim = self.calculate_user_similarity(target_user, user)
            similarities.append((user, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:n]

    def recommend_movies(self, target_user, n=10):
        similar_users = self.find_similar_users(target_user)
        user_rated = set(self.ratings_df[self.ratings_df['user_id'] == target_user]['movie_id'])
        movie_scores = defaultdict(float)
        movie_weights = defaultdict(float)
        for similar_user, similarity in similar_users:
            if similarity <= 0:
                continue
            sdf = self.ratings_df[self.ratings_df['user_id'] == similar_user]
            for _, row in sdf.iterrows():
                movie_id = row['movie_id']
                if movie_id in user_rated:
                    continue
                movie_scores[movie_id] += row['rating'] * similarity
                movie_weights[movie_id] += similarity
        recommendations = []
        for movie_id, score in movie_scores.items():
            if movie_weights[movie_id] > 0:
                avg_score = score / movie_weights[movie_id]
                recommendations.append((int(movie_id), float(avg_score)))
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n]