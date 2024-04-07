"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px


# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model
from streamlit_option_menu import option_menu
from recommenders.discover_movie import get_ratings_and_info

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')
movies_df = pd.read_csv('resources/data/movies.csv')
ratings = pd.read_csv('resources/data/ratings.csv')

movies = ratings.merge(movies_df, on='movieId', how='left')
movies[['title']].dropna()

# Load the external stylesheet/css
with open('resources/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    # page_selection = st.sidebar.selectbox("Choose Option", page_options)
    with st.sidebar:
            st.info("**Ayo! Its Showtime 🍿**")
            page_selected = option_menu(
            menu_title = "Find Your Way",
            options = ["Home","Our Recommender Systems","Discover More Movies","Insights","About Us","Contact Us"],
            icons = ["house","gear", "film","binoculars","info-circle","telephone"],
            menu_icon = "compass",
            styles={
                    "icon": {"font-size": "10px"},
                   'nav-link':{'--hover-color': "#FF6700"},
                   'nav-link-selected': {'background-color':'#1C352D'},
                   'a':{'color': '#fff'},
                   

            },
            default_index = 0,
            #orientation = "horizontal",
        )
#             st.markdown(
#     """
#     <div style='background-color:#d0d0d0; padding:10px; border-radius:5px;'>
#         <h2 style='text-align:center;'>🎈 Interactive charts coming in v1.1.0!</h2>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
    if page_selected == "Home":
         
                st.write('# Movie Match')
                st.write('### The Ultimate Movie Recommder')
                st.image('resources/imgs/Image_header.png',use_column_width=True)

    if page_selected == "Our Recommender Systems":
            st.info("Choose A Recommender")
            

            tab1, tab2 = st.tabs(['Collaborative Filtering','Content Based Filtering'])

            #  # User-based preferences
            # st.write('### Enter Your Three Favorite Movies')
            # movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
            # movie_2 = st.selectbox('Second Option',title_list[25055:25255])
            # movie_3 = st.selectbox('Third Option',title_list[21100:21200])
            # fav_movies = [movie_1,movie_2,movie_3]


            with tab1:
                    # User-based preferences
                with st.container():
                     st.write("""
                    Logistic Regression uses the probability of a data point to belonging to a certain class to classify each datapoint to it's best estimated class

Logistic regression has been rated as the best performing model for linearly separable data especially if it's predicting binary data(Yes & NO or 1 & 0), and performs better when there's no class imbalance. 
""")
                st.write('### Enter Your Three Favorite Movies')
                movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
                movie_2 = st.selectbox('Second Option',title_list[25055:25255])
                movie_3 = st.selectbox('Third Option',title_list[21100:21200])
                fav_movies = [movie_1,movie_2,movie_3]
                
                if st.button("Recommend"):

                    try:
                        with st.spinner('Crunching the numbers...'):
                            top_recommendations = collab_model(movie_list=fav_movies,
                                                            top_n=10)
                        st.title("Some Movies You Might like:")
                        col1,col2,col3,col4,col5,col6,col7,col8,col9,col10 = st.columns(10)
                        cols=[col1,col2,col3,col4,col5,col6,col7,col8,col9,col10]
                       
                        with st.container():
                            

                            for i, entry in enumerate(top_recommendations):
                                with st.container():
                                    with cols[i]:
                                        st.image(entry['image_url'],width=150, caption=entry['title'] )
                                # st.markdown(f"""
                                #             <div class="card" width=140px>
                                #                 <img src="{entry['image_url']}" class="myImg"></img>
                                #                 <p>{entry['title']}</p>
                                #             </div>
                                #             """,unsafe_allow_html=True)
                                
                                # with cols[i]:
                                #     st.write(f"""<b style="color:red"> {entry['title']}</b>""",unsafe_allow_html=True)
                                #     st.image(entry['image_url'], width=200)
                    except:
                        st.error("Oops! Looks like this algorithm does't work.\
                                We'll need to fix it!")
                        
            with tab2:
                 
                 # User-based preferences
                st.write('### Enter Your Three Favorite Movies')
                movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200],key=1)
                movie_2 = st.selectbox('Second Option',title_list[25055:25255], key=3)
                movie_3 = st.selectbox('Third Option',title_list[21100:21200], key=4)
                fav_movies = [movie_1,movie_2,movie_3]
                 

                if st.button("Recommend",2):

                    try:
                        with st.spinner('Crunching the numbers...'):
                            top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                           
                        st.title("We think you'll like:")
                        col1,col2,col3,col4,col5,col6,col7,col8,col9,col10 = st.columns(10)
                        cols=[col1,col2,col3,col4,col5,col6,col7,col8,col9,col10]

                        print(top_recommendations)
                        with st.container():
                                for i, entry in enumerate(top_recommendations):
                                    with cols[i]:
                                        st.image(entry['image_url'],width=150, caption=entry['title'] )
                    except:
                        st.error("Oops! Looks like this algorithm does't work.\
                                We'll need to fix it!")


    # if page_selected == "404":
    #     # Header contents
                
    #             # Recommender System algorithm selection
    #             sys = st.radio("Select an algorithm",
    #                         ('Content Based Filtering',
    #                             'Collaborative Based Filtering'))

    #             # User-based preferences
    #             st.write('### Enter Your Three Favorite Movies')
    #             movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
    #             movie_2 = st.selectbox('Second Option',title_list[25055:25255])
    #             movie_3 = st.selectbox('Third Option',title_list[21100:21200])
    #             fav_movies = [movie_1,movie_2,movie_3]

    #             # Perform top-10 movie recommendation generation
    #             if sys == 'Content Based Filtering':
    #                 if st.button("Recommend"):
    #                     try:
    #                         with st.spinner('Crunching the numbers...'):
    #                             top_recommendations = content_model(movie_list=fav_movies,
    #                                                                 top_n=10)
    #                         st.title("We think you'll like:")
    #                         for i,j in enumerate(top_recommendations):
    #                             st.subheader(str(i+1)+'. '+j)
    #                     except:
    #                         st.error("Oops! Looks like this algorithm does't work.\
    #                                 We'll need to fix it!")


    #             if sys == 'Collaborative Based Filtering':
    #                 if st.button("Recommended"):
    #                     try:
    #                         with st.spinner('Crunching the numbers...'):
    #                             top_recommendations = collab_model(movie_list=fav_movies,
    #                                                             top_n=10)
    #                         st.title("We think you'll like:")
    #                         col1,col2,col3,col4,col5,col6,col7,col8,col9,col10 = st.columns(10)
    #                         cols=[col1,col2,col3,col4,col5,col6,col7,col8,col9,col10]
                            
    #                         with st.container():
                                

    #                             for i, entry in enumerate(top_recommendations):
    #                                 st.markdown(f"""
    #                                             <div class="card" width=140px>
    #                                                 <img src="{entry['image_url']}" class="myImg"></img>
    #                                                 <p>{entry['title']}</p>
    #                                             </div>
    #                                             """,unsafe_allow_html=True)
                                    
    #                                 with cols[i]:
    #                                     st.write(f"""<b style="color:red"> {entry['title']}</b>""",unsafe_allow_html=True)
    #                                     st.image(entry['image_url'], width=200)
    #                     except:
    #                         st.error("Oops! Looks like this algorithm does't work.\
    #                                 We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selected == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")
    
    if page_selected == "Discover More Movies":

        st.markdown("""
            <style>
                    # .css-ytjvkl{
                    #     color: rgb(255, 75, 75);
                    #     text-decoration: none;
                    #     border: 2px solid #bfc111;
                    #     background-color: darkolivegreen;
                    #     color: white;
                    #     padding: 4px;
                    #     border-radius: 5px;
                    # }
                
                    p{
                        color: red;
                        
                    
                    }
                    p a {
                        text-decoration: none;
                        border: 2px solid #bfc111;
                        background-color: darkolivegreen;
                        color: white;
                        padding: 4px;
                        border-radius: 5px;
                    }
                    .css-1offfwp a {
                        color: #fff;
                    }
            </style>
                    """, unsafe_allow_html=True)
        st.button("Hello", key=99)

        top_50 = get_ratings_and_info()

        st.title("See more title like:")
        col1,col2,col3,col4,col5,col6,col7,col8,col9,col10 = st.columns(10)
        cols=[col1,col2,col3,col4,col5,col6,col7,col8,col9,col10]

        print("Prnted here ", top_50)
        with st.container():
                for i, entry in enumerate(top_50[0:10]):
                    with cols[i]:
                        st.image(entry['images'],width=150, caption=entry['title'] )
                        st.caption(entry['rating'])
                        st.markdown(f"""<a href={entry['link']}>For More Info!</a>""", unsafe_allow_html=True)

       
            
                
       



    if page_selected == "Insights":

        movies['release_date'] = pd.to_datetime(movies['timestamp'], unit='s')
        # Extract the year from the datetime objects
        movies['release_year'] = movies['release_date'].dt.year
        movies['release_year'].to_string()
        # Filter the DataFrame to include only movies released within the past 10 years
        current_year = pd.Timestamp.now().year
        recent_movies_df = movies[movies['release_year'] >= current_year - 10]
        # Aggregate the data to count the occurrences of each genre in the past decade
        genre_counts = recent_movies_df['genres'].value_counts().reset_index()
        genre_counts.columns = ['Genres', 'Count']
        top_10_genres = genre_counts.head(10)

        # Change display options to prevent pandas from using a comma as a thousands separator
        pd.set_option('display.float_format', lambda x: '{:.0f}'.format(x))
        
    


        

        tab1, tab2, tab3 = st.tabs(['Top Rated', 'Worst Rated', 'Popular Genres'])
        

        
        rating_summary = movies.groupby('title').agg(total_rating_score=('rating', 'sum'),
                                             rating_count=('rating', 'count')).reset_index()
        highly_rated = rating_summary.nlargest(10, 'total_rating_score')

        ratings_count_df = movies[['title', 'rating']].groupby('title').count().reset_index()
        

        # ratings_count_df = movies['title']['rating'].groupby('rating').count().reset_index()

        ratings_count_df[['title', 'rating_count']] = ratings_count_df[['title', 'rating']]
        ratings_count_df.drop(ratings_count_df['rating'])
        # # Sort the DataFrame by rating count to get the top 10 and worst 10 movies
        top_10_movies = ratings_count_df.sort_values(by='rating_count', ascending=False).head(10)
        worst_10_movies = ratings_count_df.sort_values(by='rating_count', ascending=False).tail(10)

        # top_10_movies = movie_stats.sort_values(by='rating_count', ascending=False).head(10)
        # worst_10 = movie_stats.sort_values(by='rating_count', ascending=False).tail(10)

        

# Plot the top popular genres

        if st.checkbox('Show raw data'):
            st.write(movies)
        
        # if st.checkbox("See top genres"):
        #     st.title("Top Popular Genres")
        #     fig, ax = plt.subplots()
        #     genre_counts.plot(kind='bar', ax=ax)
        #     ax.set_xlabel('Genre')
        #     ax.set_ylabel('Number of Movies')
        #     st.pyplot(fig)
        

        with tab1:
            
            st.title("Top 10 Movies")

            if st.checkbox('See table'):
                    st.write(highly_rated)
            
            if st.checkbox('Bar graph'):
                top_chart = alt.Chart(top_10_movies[['title', 'rating_count']]).mark_bar().encode(
                    x='title',
                    y=alt.Y('rating_count', sort='-x'),
                    color=alt.Color('rating_count', scale=alt.Scale(scheme='viridis'))
                ).properties(width=600, height=400)
                st.altair_chart(top_chart, use_container_width=True)
            
           
                
                
        with tab2:
            
            with st.container():
                st.title("Worst 10 Movies")
                if st.checkbox('Show table'):
                    st.write(worst_10_movies[['title', 'rating_count']])
            
        with tab3:
            st.subheader("Genres Release for the Past Decade ")

            if st.checkbox('Show Table'):
                st.write(recent_movies_df[['title','genres', 'release_year']])

            if st.checkbox('Show Graph'):
                top_10_genres.head()
                st.bar_chart(top_10_genres.set_index('Genres'), height=500)

           
            
    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()
