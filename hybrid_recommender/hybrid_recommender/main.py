"""Entry point for the hybrid recommender demo."""
from .data import create_movie_database, create_user_ratings
from .hybrid import HybridRecommender
from .utils import print_section_header, display_recommendations
import pandas as pd

def analyze_dataset(movies_df, ratings_df):
    print_section_header('DATASET STATISTICS')
    print(f"\nMovies Database:")
    print(f"  Total movies: {len(movies_df)}")
    print(f"  Years covered: {movies_df['year'].min()} - {movies_df['year'].max()}")
    print(f"  Average rating: {movies_df['avg_rating'].mean():.2f}/5.0")
    print(f"  Total ratings collected: {movies_df['num_ratings'].sum():,}")
    # simple genre distribution
    all_genres = []
    for g in movies_df['genre']:
        all_genres.extend(g.split('|'))
    from collections import Counter
    genre_counts = Counter(all_genres)
    print('\nGenre Distribution:')
    for genre, count in genre_counts.most_common(10):
        print(f"  {genre:15s}: {count:3d} movies")

def main():
    print('\n' + '=' * 75)
    print('  HYBRID MOVIE RECOMMENDER SYSTEM')
    print('  Prototype Version 1.0')
    print('=' * 75)
    print('\n[1/5] Loading movie database...')
    movies_df = create_movie_database()
    print(f"      ✓ Loaded {len(movies_df)} movies")
    print('[2/5] Loading user ratings...')
    ratings_df = create_user_ratings()
    print(f"      ✓ Loaded {len(ratings_df)} ratings from {ratings_df['user_id'].nunique()} users")
    print('[3/5] Building recommendation engines...')
    recommender = HybridRecommender(movies_df, ratings_df)
    print('      ✓ Collaborative Filtering engine ready')
    print('      ✓ Content-Based Filtering engine ready')
    print('      ✓ Hybrid engine ready')
    print('[4/5] Analyzing dataset...')
    analyze_dataset(movies_df, ratings_df)
    print('[5/5] Generating recommendations...')

    print_section_header('EXAMPLE: ACTION/SCI-FI FAN (User #5)')
    display_recommendations(recommender, user_id=5, method='hybrid')

    # Save artifacts
    movies_df.to_csv('movie_database.csv', index=False)
    ratings_df.to_csv('user_ratings.csv', index=False)
    # sample recommendations for first 10 users
    recs_out = []
    for uid in range(1, 11):
        recs = recommender.recommend_hybrid(uid, n=5)
        for rank, (mid, score) in enumerate(recs, 1):
            details = recommender.get_movie_details(mid)
            recs_out.append({
                'user_id': uid, 'rank': rank, 'movie_id': mid,
                'movie_title': details['title'], 'genre': details['genre'],
                'recommendation_score': round(score, 4)
            })
    pd.DataFrame(recs_out).to_csv('sample_recommendations.csv', index=False)
    print('\nArtifacts saved: movie_database.csv, user_ratings.csv, sample_recommendations.csv')
    print('\nRecommender demo finished.')

if __name__ == '__main__':
    main()