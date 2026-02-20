
# this is not the Main file
# But do not use similarity_pkl so kept

import pandas as pd
import requests
import streamlit as st
import pickle
import ssl
import certifi
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors



# Load movies dataframe
movies = pickle.load(open("movies_pkl.pkl", "rb"))

st.title("Movie Recommender System")

# ----------------------------
# 🔥 Create Vector + Train Model
# ----------------------------

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(vectors)

# ----------------------------
# Poster Fetch Function
# ----------------------------

@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=71176ecc564f6ba4565822da850dd49b"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=No+Image"

        data = response.json()
        poster_path = data.get("poster_path")

        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Image"

        return "https://image.tmdb.org/t/p/w500/" + poster_path

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"


# ----------------------------
# Recommendation Function
# ----------------------------

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances, indices = model.kneighbors(
        [vectors[index]],
        n_neighbors=6
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in indices[0][1:]:
        movie_id = movies.iloc[i].movie_id
        recommended_movie_names.append(movies.iloc[i].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# ----------------------------
# UI
# ----------------------------

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    recommended_list, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.markdown(
                f"<h4 style='text-align:center; font-size:16px;'>{recommended_list[i]}</h4>",
                unsafe_allow_html=True
            )
            st.image(posters[i])