"""

    Collaborative-based filtering for item recommendation.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: You are required to extend this baseline algorithm to enable more
    efficient and accurate computation of recommendations.

    !! You must not change the name and signature (arguments) of the
    prediction function, `collab_model` !!

    You must however change its contents (i.e. add your own collaborative
    filtering algorithm), as well as altering/adding any other functions
    as part of your improvement.

    ---------------------------------------------------------------------

    Description: Provided within this file is a baseline collaborative
    filtering algorithm for rating predictions on Movie data.

"""

# Script dependencies
import pandas as pd
import numpy as np
import scipy as sp
import operator

import pickle
import copy
from surprise import Reader, Dataset
from surprise import SVD, NormalPredictor, BaselineOnly, KNNBasic, NMF
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from utils.data_loader import load_movie_titles

# Importing data
movies_df = pd.read_csv('resources/data/movies.csv')
ratings_df = pd.read_csv('resources/data/ratings.csv')
media_df =  pd.read_csv('resources/data/links_with_media.csv')


# merged_df = ratings_df.merge(movies_df, on='movieid', how='left')
media_df.drop('Unnamed: 0', axis=1)
ratings_df.drop(['timestamp'], axis=1,inplace=True)
newMovie_df = movies_df.merge(media_df[['images','link']], on=media_df['movieId'])
# merged_df

# We make use of an SVD model trained on a subset of the MovieLens 10k dataset.
# model=pickle.load(open('resources/models/svd_model.pkl', 'rb'))
with open('resources/models/am2_unsupervised_recommender.pkl', 'rb') as file:
    model = pickle.load(file)


def prediction_item(item_id):
    """Map a given favourite movie to users within the
       MovieLens dataset with the same preference.

    Parameters
    ----------
    item_id : int
        A MovieLens Movie ID.

    Returns
    -------
    list
        User IDs of users with similar high ratings for the given movie.

    """
    # Data preprosessing
    reader = Reader(rating_scale=(0.5, 5))
    load_df = Dataset.load_from_df(ratings_df,reader)
    a_train = load_df.build_full_trainset()

    predictions = []
    for ui in a_train.all_users():
        predictions.append(model.predict(iid=item_id,uid=ui, verbose = False))
    return predictions

def pred_movies(movie_list):
    """Maps the given favourite movies selected within the app to corresponding
    users within the MovieLens dataset.

    Parameters
    ----------
    movie_list : list
        Three favourite movies selected by the app user.

    Returns
    -------
    list
        User-ID's of users with similar high ratings for each movie.

    """
    # Store the id of users
    id_store=[]
    # For each movie selected by a user of the app,
    # predict a corresponding user within the dataset with the highest rating
    for i in movie_list:
        predictions = prediction_item(item_id = i)
        predictions.sort(key=lambda x: x.est, reverse=True)
        # Take the top 10 user id's from each movie with highest rankings
        for pred in predictions[:10]:
            id_store.append(pred.uid)
    # Return a list of user id's
    return id_store

# !! DO NOT CHANGE THIS FUNCTION SIGNATURE !!
# You are, however, encouraged to change its content.  

def collab_model(movie_list,top_n=10):
    """Short summary.
    arameters
    ----------
    movie_list : type
        Description of parameter `movie_list`.
    top_n : type
        Description of parameter `top_n`.
    Returns
    -------
    type
        Description of returned object.
    """
    #getting list of ids of 10 users that rated movies highly
    user_ids = pred_movies(movie_list)

    #obtaining the ratings of the users

    df_init_users = ratings_df[ratings_df['userId'].isin(user_ids)]

    # for i in user_ids:
    #     df_init_users = df_init_users.append(ratings_df[ratings_df['userId']==i])

    df_init_users=df_init_users.drop_duplicates().reset_index(drop=True)
    
    #obtaining movieIds from movie titles
    movie_ids = []
    for movie in movie_list:
        movie_ids.append(int(movies_df['movieId'][movies_df['title']==movie]))
    
    #adding new user
    new_row1 = {'userId':1234567, 'movieId':movie_ids[0], 'rating':5}
    new_row2 = {'userId':1234567, 'movieId':movie_ids[1], 'rating':5}
    new_row3 = {'userId':1234567, 'movieId':movie_ids[2], 'rating': 5}
    df_init_users = df_init_users.append([new_row1,new_row2,new_row3],ignore_index=True)

    #pivot ratings
    pivot_user = pd.pivot_table(df_init_users,values='rating',columns='userId',index='movieId')
    pivot_user.fillna(0, inplace=True)
    
    pivot_user = pivot_user.apply(lambda x: (x-np.min(x))/(np.max(x)-np.min(x)), axis=1)

    pivot_user_arr =  np.array(pivot_user)
    
    #finding movies similarities based on users
    cosine_sim=cosine_similarity(pivot_user_arr,pivot_user_arr)
    
    #mat
    m_index_list = list(pivot_user.index)
    df = movies_df[movies_df['movieId'].isin(m_index_list)].reset_index(drop=True)

    #Obtaining indices
    indices = pd.Series(df['title'])
    idx_1 = indices[indices == movie_list[0]].index[0]
    idx_2 = indices[indices == movie_list[1]].index[0]
    idx_3 = indices[indices == movie_list[2]].index[0]

    rank_1 = cosine_sim[idx_1]
    rank_2 = cosine_sim[idx_2]
    rank_3 = cosine_sim[idx_3]

    score_series_1 = pd.Series(rank_1).sort_values(ascending = False)
    score_series_2 = pd.Series(rank_2).sort_values(ascending = False)
    score_series_3 = pd.Series(rank_3).sort_values(ascending = False)

    # Appending the names of movies
    listings = score_series_1.append(score_series_1).append(score_series_3).sort_values(ascending = False)
    recommended_movies = []
    # Choose top 50
    top_50_indexes = list(listings.iloc[1:50].index)
    # Removing chosen movies
    top_indexes = np.setdiff1d(top_50_indexes,[idx_1,idx_2,idx_3])
    for i in top_indexes[:10]:

        movieItem = {
            'title': list(movies_df['title'])[i],
            'image_url': get_movie_image_url(list(movies_df['title'])[i]),
            # 'ratings' : get_movie_rating(list(movies_df['title'])[i])
              #  Get image URL
            # # 'external_link': get_external_link(newMovie_df.iloc[idx]['title'])  # Get external link
        }
        recommended_movies.append(movieItem)
        print(movieItem)

        
        # print(get_movie_image_url(newMovie_df.iloc[i]['movieId']))
        
   

    return recommended_movies

def get_movie_image_url(movie_title):
    """Get the image URL of a movie based on its title.
    
    Parameters
    ----------
    movie_title : str
        Title of the movie.
    
    Returns
    -------
    str
        Image URL of the movie.
    """
    # Find the image URL for the given movie title
    row = newMovie_df[newMovie_df['title'] == movie_title]
    if not row.empty:
        image_url = row['images'].values[0]
    else:
        # If image URL is not available, return a default image URL or handle the case accordingly
        image_url = 'default_image_url.jpg'

    return image_url

def get_movie_rating(movie_title):
    """
    Get the rating of a movie from a DataFrame.

    Parameters:
        movie_title (str): The title of the movie.
        ratings_df (pandas.DataFrame): DataFrame containing movie ratings (columns: 'userid', 'movieid', 'timestamp', 'ratings').
        movies_df (pandas.DataFrame): DataFrame containing movie details (columns: 'movieid', 'title', 'genre').

    Returns:
        float or None: The rating of the movie if found, otherwise None.
    """
    # Merge ratings_df and movies_df on 'movieid' column
    

    # Check if the movie title exists in the merged DataFrame
    movie_id = movies_df[movies_df['title'] == movie_title]['movieid']
    if not movie_id.empty:
        ratings_for_movie = ratings_df[ratings_df['movieid'] == movie_id.iloc[0]]['ratings']
        if not ratings_for_movie.empty:
            return ratings_for_movie.mean()
    print(f"Movie '{movie_title}' not found in the DataFrame.")
    return None