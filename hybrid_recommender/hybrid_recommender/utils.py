def print_section_header(title):
    print('\n' + '=' * 75)
    print(f'  {title}')
    print('=' * 75)

def display_recommendations(recommender, user_id, method='hybrid'):
    print(f"\nGenerating recommendations for User #{user_id}...")
    user_ratings = recommender.get_user_ratings(user_id)
    print(f"\nUser's Rating History ({len(user_ratings)} movies rated):")
    if user_ratings:
        user_ratings_sorted = sorted(user_ratings, key=lambda x: x[1], reverse=True)[:5]
        for movie_id, rating in user_ratings_sorted:
            details = recommender.get_movie_details(movie_id)
            print(f"  ★ {rating:.1f} - {details['title']} ({details['genre']}) [{details['year']}]")
    else:
        print("  (No rating history - Cold Start scenario)")

    if method == 'collaborative':
        recs = recommender.cf_engine.recommend_movies(user_id, n=10)
        method_name = "Collaborative Filtering"
    elif method == 'content':
        recs = recommender.cb_engine.recommend_for_user(user_ratings, recommender.ratings_df, n=10)
        method_name = "Content-Based Filtering"
    else:
        recs = recommender.recommend_hybrid(user_id, n=10)
        method_name = "Hybrid (CF 60% + CB 40%)"

    print(f"\n{method_name} Recommendations:")
    print("-" * 75)
    for i, (movie_id, score) in enumerate(recs, 1):
        details = recommender.get_movie_details(movie_id)
        print(f"{i:2d}. {details['title'][:40]:40s} | Score: {score:.3f}")
        print(f"     Genre: {details['genre']:30s} | Rating: {details['avg_rating']:.1f}/5.0 ({details['num_ratings']:,} ratings)")
        print(f"     Director: {details['director']:30s} | Year: {details['year']}")
        print()