# recommendations.py

import pandas as pd
import pickle
import os

class RecommendationData:
    def __init__(self):
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.df_movies = None
        self.movie_indices = None

    def load_data(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(base_dir, 'tfidf_matrix.pkl'), 'rb') as f:
                self.tfidf_matrix = pickle.load(f)
            with open(os.path.join(base_dir, 'cosine_sim_matrix.pkl'), 'rb') as f:
                self.cosine_sim = pickle.load(f)
            self.df_movies = pd.read_csv(os.path.join(base_dir, 'movies_features.csv'))
            self.movie_indices = pd.Series(
                self.df_movies.index, index=self.df_movies['movie_id']
            ).drop_duplicates()
            print("Recommendation data loaded successfully.")
        except Exception as e:
            print(f"Error loading recommendation data: {e}")
            self.tfidf_matrix = None
            self.cosine_sim = None
            self.df_movies = None
            self.movie_indices = None

# Instantiate the recommendation data object
recommendation_data = RecommendationData()
