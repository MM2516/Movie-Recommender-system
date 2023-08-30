import pandas as pd
import streamlit as sl
import pickle
import requests


def getPoster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=008c1f26d33ec4fbe1b4b7d6492b58c9&&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        movies_posters.append(getPoster(movie_id))
    return recommended_movies, movies_posters


sl.title('Movie Recommender System')
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

selected_movie = sl.selectbox(
    'Select a movie:',
    movies['title'].values
)

similarity = pickle.load(open('similarity.pkl', 'rb'))

if sl.button('Recommend Movies'):
    recommended_list, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = sl.columns(5)

    with col1:
        sl.text(recommended_list[0])
        sl.image(posters[0])

    with col2:
        sl.text(recommended_list[1])
        sl.image(posters[1])

    with col3:
        sl.text(recommended_list[2])
        sl.image(posters[2])

    with col4:
        sl.text(recommended_list[3])
        sl.image(posters[3])

    with col5:
        sl.text(recommended_list[4])
        sl.image(posters[4])
