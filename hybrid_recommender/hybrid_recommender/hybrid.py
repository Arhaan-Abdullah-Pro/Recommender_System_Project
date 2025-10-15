from collections import defaultdict
from .cf import CollaborativeFiltering
from .cb import ContentBasedFiltering

class HybridRecommender:
    def __init__(self, movies_df, ratings_df):
        self.movies_df = movies_df
        self.ratings_df = ratings_df
        self.cf_engine = CollaborativeFiltering(ratings_df)
        self.cb_engine = ContentBasedFiltering(movies_df)

    def get_user_ratings(self, user_id):
        user_data = self.ratings_df[self.ratings_df['user_id'] == user_id]
        return [(int(row['movie_id']), float(row['rating'])) for _, row in user_data.iterrows()]

    def recommend_hybrid(self, user_id, n=10, cf_weight=0.6, cb_weight=0.4):
        user_rated = self.get_user_ratings(user_id)
        if not user_rated:
            return self.recommend_popular(n)
        cf_recs = self.cf_engine.recommend_movies(user_id, n=20)
        cb_recs = self.cb_engine.recommend_for_user(user_rated, self.ratings_df, n=20)
        combined = defaultdict(float)
        if cf_recs:
            max_cf = max([s for _,s in cf_recs]) or 1.0
            for mid, score in cf_recs:
                combined[int(mid)] += (score / max_cf) * cf_weight
        if cb_recs:
            max_cb = max([s for _,s in cb_recs]) or 1.0
            for mid, score in cb_recs:
                combined[int(mid)] += (score / max_cb) * cb_weight
        recs = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        return recs[:n]

    def recommend_popular(self, n=10):
        pop = self.movies_df.nlargest(n, 'num_ratings')[['movie_id','avg_rating']]
        return [(int(r['movie_id']), float(r['avg_rating'])) for _,r in pop.iterrows()]

    def get_movie_details(self, movie_id):
        movie = self.movies_df[self.movies_df['movie_id'] == movie_id].iloc[0]
        return {
            'title': movie['title'],
            'genre': movie['genre'],
            'year': int(movie['year']),
            'director': movie['director'],
            'avg_rating': float(movie['avg_rating']),
            'num_ratings': int(movie['num_ratings'])
        }