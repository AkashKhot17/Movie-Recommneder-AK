import pandas as pd
import requests
import streamlit as st

import pickle
# import ssl
# import certifi


# for SSL handshake for poster
# ssl._create_default_https_context = ssl.create_default_context(
#     cafile=certifi.where()
# )

movies = pickle.load(open("movies_pkl.pkl", "rb"))

similarity = pickle.load(open('similarity_pkl.pkl','rb'))

# movies_dict=pickle.load(open("movies_dict.pkl", "rb"))
# movies=pd.DataFrame(movies_dict)

st.title("Movie Recomender System")

print(movies.head())
selected_movie= st.selectbox(
    "How would you like to be contacted?",
    movies["title"].values
)


# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#
#     recommend_list=[]
#     for i in distances[1:6]:
#         recommend_list.append(movies.iloc[i[0]].title)
#
#
#     return recommend_list


# Main Function
# def fetch_poster(movie_id):
#
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=71176ecc564f6ba4565822da850dd49b"
#
#     # response = requests.get(url, verify=certifi.where())
#     response = requests.get(url, timeout=5)
#     # Debug check
#     if response.status_code != 200:
#         print("Error:", response.status_code)
#         print("Response:", response.text)
#         return None
#
#     try:
#         data = response.json()
#
#     except:
#         print("Invalid JSON:", response.text)
#         return None
#
#     poster_path = data.get('poster_path')
#
#     if poster_path is None:
#         print("Poster not found for movie_id:", movie_id)
#         return None
#
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path


@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=71176ecc564f6ba4565822da850dd49b"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=No+Image"

        data = response.json()
        poster_path = data.get("poster_path")

        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Image"

        return "https://image.tmdb.org/t/p/w500/" + poster_path

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []




    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


if st.button("Recommend"):
        recommended_list,poster=recommend(selected_movie)


        col1, col2, col3 , col4 , col5= st.columns(5)

        with col1:
            st.markdown(
                f"<h4 style='text-align:center; font-size:16px;'>{recommended_list[0]}</h4>",
                unsafe_allow_html=True
            )
            st.image(poster[0])

        with col2:
            st.markdown(
                f"<h4 style='text-align:center; font-size:16px;'>{recommended_list[1]}</h4>",
                unsafe_allow_html=True
            )
            st.image(poster[1])

        with col3:
            st.markdown(
                f"<h4 style='text-align:center; font-size:16px;'>{recommended_list[2]}</h4>",
                unsafe_allow_html=True
            )
            st.image(poster[2])
        with col4:

            st.markdown(
                f"<h4 style='text-align:center; font-size:16px;'>{recommended_list[3]}</h4>",
                unsafe_allow_html=True
            )
            st.image(poster[3])

        with col5:
            st.markdown(
                f"<h4 style='text-align:center; font-size:16px;'>{recommended_list[4]}</h4>",
                unsafe_allow_html=True
            )

            st.image(poster[4])


#   full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
# https://api.themoviedb.org/3/movie/65?api_key=71176ecc564f6ba4565822da850dd49b

# https://www.themoviedb.org/settings/api
# python -m venv .venv
# .venv\Scripts\activate
# python -m pip install --upgrade pip
# pip install streamlit requests certifi