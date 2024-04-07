# Script dependencies
import pandas as pd
import numpy as np

import operator


# Importing data
movies_df = pd.read_csv('resources/data/movies.csv')
ratings_df = pd.read_csv('resources/data/ratings.csv')
media_df =  pd.read_csv('resources/data/links_with_media.csv')


ratings = ratings_df.merge(movies_df, on='movieId', how='left')
updated_ratings = ratings.drop_duplicates(subset=['movieId'])
updated_ratings

newMovie_df = updated_ratings.merge(media_df, on='movieId', )
newMovie_df = newMovie_df.drop('Unnamed: 0', axis=1)


def get_ratings_and_info():
    # Select required columns
    random_50 = []
    ratings_info = newMovie_df[['rating', 'title', 'link', 'images']].head(50)
    for index, row in ratings_info.iterrows():
        movie = {
            'title': row['title'],
            'link': row['link'],
            'images': row['images'],
            'rating': row['rating']
        }
        random_50.append(movie)
    return random_50