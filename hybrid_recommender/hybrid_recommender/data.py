import pandas as pd
import numpy as np

def create_movie_database():
    """Generate comprehensive movie database (100 movies)"""
    movies_data = {
        'movie_id': list(range(1, 101)),
        'title': [
            # Action Movies (1-15)
            'The Dark Guardian', 'Speed Chase', 'Cyber Strike', 'Final Mission', 'Iron Warrior',
            'Night Assault', 'Fury Road Reborn', 'Apex Predator', 'Silent Strike', 'Code Red',
            'Terminal Velocity', 'Shadow Ops', 'Black Phantom', 'Rogue Agent', 'Combat Zone',
            # Drama Movies (16-30)
            'Broken Dreams', 'The Last Letter', 'Autumn Rain', 'Silent Tears', 'Midnight Confessions',
            'Faded Memories', 'The Pianist Story', 'Lost in Time', 'Echoes of Yesterday', 'The Farewell',
            'Winter Heart', 'Unspoken Words', 'The Artist', 'Paper Towns', 'The Notebook Revisited',
            # Comedy Movies (31-45)
            'Wedding Crashers 2', 'Funny Business', 'The Hangover Returns', 'Office Chaos', 'Date Night Gone Wrong',
            'Crazy Vacation', 'Best Man Disaster', 'The Proposal Remix', 'Game Night', 'Hot Pursuit',
            'Daddy Daycare Plus', 'The Interview 2', 'Step Brothers United', 'Neighbors War', 'Girls Trip 2',
            # Horror Movies (46-55)
            'Midnight Terror', 'The Haunting Hour', 'Silent Screams', 'Dark Basement', 'The Conjuring Legacy',
            'Insidious Return', 'The Nun Chronicles', 'Sinister 3', 'Paranormal Night', 'The Ritual 2',
            # Sci-Fi Movies (56-70)
            'Quantum Leap', 'Interstellar Journey', 'The Matrix Reborn', 'Blade Runner 2099', 'Arrival 2',
            'Ex Machina Returns', 'Edge of Tomorrow 2', 'Inception Paradox', 'Gravity Pull', 'The Martian Chronicles',
            'Dune Prophecy', 'Avatar Legends', 'Star Wars Legacy', 'Contact 2', 'District 10',
            # Romance Movies (71-80)
            'Love in Paris', 'The Vow Returns', 'Me Before You 2', 'A Walk to Remember Again', 'Dear John 2',
            'The Lucky One Returns', 'Safe Haven 2', 'The Best of Me', 'The Longest Ride 2', 'The Choice Returns',
            # Thriller Movies (81-90)
            'Gone Girl Returns', 'The Girl on the Train 2', 'Shutter Island Secrets', 'Prisoners Return', 'Zodiac Files',
            'Seven Sins', 'Memories of Murder', 'The Wailing 2', 'Oldboy Revenge', 'Parasite Legacy',
            # Animation Movies (91-100)
            'Toy Story 5', 'Finding Dory 2', 'Coco Returns', 'Inside Out 2', 'Up Again',
            'Moana Journey', 'Frozen 3', 'Zootopia 2', 'Big Hero 7', 'Wreck-It Ralph 3'
        ],
        'genre': [
            # Action (1-15)
            'Action', 'Action', 'Action|Sci-Fi', 'Action|Thriller', 'Action',
            'Action', 'Action', 'Action|Horror', 'Action|Thriller', 'Action',
            'Action', 'Action|Thriller', 'Action', 'Action|Thriller', 'Action',
            # Drama (16-30)
            'Drama', 'Drama|Romance', 'Drama', 'Drama', 'Drama',
            'Drama', 'Drama', 'Drama|Sci-Fi', 'Drama', 'Drama',
            'Drama', 'Drama', 'Drama', 'Drama|Romance', 'Drama|Romance',
            # Comedy (31-45)
            'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy|Romance',
            'Comedy', 'Comedy', 'Comedy|Romance', 'Comedy', 'Comedy',
            'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy',
            # Horror (46-55)
            'Horror', 'Horror', 'Horror', 'Horror', 'Horror',
            'Horror', 'Horror', 'Horror', 'Horror', 'Horror|Thriller',
            # Sci-Fi (56-70)
            'Sci-Fi', 'Sci-Fi|Drama', 'Sci-Fi|Action', 'Sci-Fi', 'Sci-Fi|Drama',
            'Sci-Fi|Thriller', 'Sci-Fi|Action', 'Sci-Fi|Thriller', 'Sci-Fi|Thriller', 'Sci-Fi|Drama',
            'Sci-Fi', 'Sci-Fi|Action', 'Sci-Fi|Action', 'Sci-Fi|Drama', 'Sci-Fi|Thriller',
            # Romance (71-80)
            'Romance', 'Romance|Drama', 'Romance|Drama', 'Romance|Drama', 'Romance|Drama',
            'Romance', 'Romance|Thriller', 'Romance|Drama', 'Romance|Drama', 'Romance|Drama',
            # Thriller (81-90)
            'Thriller|Drama', 'Thriller|Drama', 'Thriller', 'Thriller|Drama', 'Thriller',
            'Thriller', 'Thriller', 'Thriller|Horror', 'Thriller|Action', 'Thriller|Drama',
            # Animation (91-100)
            'Animation|Comedy', 'Animation|Comedy', 'Animation|Drama', 'Animation|Comedy', 'Animation|Drama',
            'Animation|Comedy', 'Animation|Comedy', 'Animation|Comedy', 'Animation|Action', 'Animation|Comedy'
        ],
        'year': [2023 + (i % 3) for i in range(100)],
        'director': ['Various'] * 100,
        'avg_rating': [round(3.5 + (i % 15) * 0.1, 2) for i in range(100)],
        'num_ratings': [9000 + (i * 100) for i in range(100)]
    }
    return pd.DataFrame(movies_data)

def create_user_ratings(seed=42, num_users=50):
    """Generate synthetic user rating data for collaborative filtering"""
    np.random.seed(seed)
    user_ratings = []
    user_profiles = {
        'action_lover': list(range(1, 16)) + list(range(56, 71)),
        'drama_fan': list(range(16, 31)) + list(range(71, 81)),
        'comedy_enthusiast': list(range(31, 46)) + list(range(91, 101)),
        'horror_buff': list(range(46, 56)) + list(range(81, 91)),
        'family_viewer': list(range(91, 101)) + list(range(31, 41))
    }

    for user_id in range(1, num_users+1):
        if user_id <= 10:
            profile = 'action_lover'
        elif user_id <= 20:
            profile = 'drama_fan'
        elif user_id <= 30:
            profile = 'comedy_enthusiast'
        elif user_id <= 40:
            profile = 'horror_buff'
        else:
            profile = 'family_viewer'

        preferred_movies = user_profiles[profile]
        num_ratings = np.random.randint(15, 26)
        num_preferred = int(num_ratings * 0.7)
        num_random = num_ratings - num_preferred

        rated_movies = (
            list(np.random.choice(preferred_movies, num_preferred, replace=False)) +
            list(np.random.choice([m for m in range(1, 101) if m not in preferred_movies], 
                                num_random, replace=False))
        )

        for movie_id in rated_movies:
            if movie_id in preferred_movies:
                rating = float(np.random.choice([3.5, 4.0, 4.5, 5.0], p=[0.1,0.2,0.3,0.4]))
            else:
                rating = float(np.random.choice([2.0,2.5,3.0,3.5,4.0], p=[0.1,0.2,0.3,0.25,0.15]))
            user_ratings.append({'user_id': user_id, 'movie_id': movie_id, 'rating': rating})

    return pd.DataFrame(user_ratings)