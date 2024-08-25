import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
from streamlit import header

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
df = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def getpost(id):
    responce = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c7c92887bf02b0dd6d077dc23c63df69'.format(id))
    data = responce.json()
    return "https://image.tmdb.org/t/p/w500/"+ str(data['poster_path'])

def recommend(movie):
    index = df[df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])[1:5]
    recom_movies = []
    recom_movies_id = []
    for i in distances:
        recom_movies.append(df.iloc[i[0]].title)
        recom_movies_id.append(getpost(df.iloc[i[0]].id))
    return recom_movies,recom_movies_id


st.title("Movie Recommender System")

option = st.selectbox(
    "What movie are you watching?",
    df['title'].values)

if st.button('Recommend'):
    recom_copy_movies,recom_copy_movies_poster = recommend(option)
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.text(recom_copy_movies[0])
        st.image(recom_copy_movies_poster[0])
    with col2:
        st.text(recom_copy_movies[1])
        st.image(recom_copy_movies_poster[1])
    with col3:
        st.text(recom_copy_movies[2])
        st.image(recom_copy_movies_poster[2])
    with col4:
        st.text(recom_copy_movies[3])
        st.image(recom_copy_movies_poster[3])