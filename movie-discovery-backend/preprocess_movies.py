from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from bson.objectid import ObjectId
import pickle
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['movie_db']

# Check if movies collection has data
movie_count = db.movies.count_documents({})
print(f"Number of movies in the collection: {movie_count}")

if movie_count == 0:
    print("The movies collection is empty. Please populate it with data.")
    exit()

# Fetch all movies from the database
movies_cursor = db.movies.find()
movies_list = []

# Print sample movies
print("\nSample movies from the database:")
for i, movie in enumerate(db.movies.find()):
    if i < 5:
        print(movie)
    else:
        break

# Reset the cursor and rebuild movies_list
movies_cursor = db.movies.find()
for movie in movies_cursor:
    movie_id = str(movie['_id'])
    combined_features = ''

    # Process Genre
    genres = movie.get('Genre', [])
    if genres and isinstance(genres, list):
        combined_features += ' '.join(genres) + ' '

    # Process Director
    director = movie.get('Director', '')
    if director:
        combined_features += director + ' '

    # Process Cast
    cast = movie.get('Cast', [])
    if cast and isinstance(cast, list):
        combined_features += ' '.join(cast)

    combined_features = combined_features.strip()
    movies_list.append({
        'movie_id': movie_id,
        'combined_features': combined_features
    })

# Print the first few entries of movies_list
print("\nFirst few entries in movies_list:")
for item in movies_list[:5]:
    print(item)

# Create a DataFrame
df_movies = pd.DataFrame(movies_list)

# Print DataFrame columns and first few rows
print("\nDataFrame columns:", df_movies.columns)
print("First few rows of df_movies:")
print(df_movies.head())

# Check if 'combined_features' is empty or contains only whitespace
if df_movies['combined_features'].isnull().all() or (df_movies['combined_features'].str.strip() == '').all():
    print("\nError: 'combined_features' column is empty or only contains whitespace.")
    exit()
else:
    print("\nSample 'combined_features':")
    print(df_movies['combined_features'].head())

# Vectorize using TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
try:
    tfidf_matrix = tfidf.fit_transform(df_movies['combined_features'])
except ValueError as e:
    print(f"\nError during TF-IDF vectorization: {e}")
    exit()

# Save the TF-IDF matrix and mapping
with open('tfidf_matrix.pkl', 'wb') as f:
    pickle.dump(tfidf_matrix, f)

# Compute the cosine similarity matrix
from sklearn.metrics.pairwise import linear_kernel

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Save the cosine similarity matrix
with open('cosine_sim_matrix.pkl', 'wb') as f:
    pickle.dump(cosine_sim, f)

df_movies.to_csv('movies_features.csv', index=False)
