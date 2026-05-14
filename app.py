import pickle
import os
import streamlit as st
import requests
import joblib
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Cinemate | Movie Recommender", page_icon="🍿", layout="wide")

st.markdown(
    """
<style>
.main-title {
    font-size: 3rem;
    text-align: center;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
}

.movie-poster {
    width: 100%;
    border-radius: 10px;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.movie-poster:hover {
    transform: scale(1.08);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.movie-title {
    text-align: center;
    font-weight: 600;
    margin-top: 8px;
}
</style>
""",
    unsafe_allow_html=True,
)


TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
POSTER_PLACEHOLDER_URL = "https://via.placeholder.com/500x750?text=No+Poster"
LOTTIE_URL = "https://assets10.lottiefiles.com/packages/lf20_khzniaya.json"


@st.cache_data
def load_lottie_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None


@st.cache_data
def load_movies():
    with open("movies.pkl", "rb") as movie_file:
        return pickle.load(movie_file)


@st.cache_resource
def load_similarity():
    return joblib.load("similarity_compressed.joblib")

def fetch_poster(movie_id):
    if not TMDB_API_KEY:
        return POSTER_PLACEHOLDER_URL
    url = "https://api.themoviedb.org/3/movie/{}".format(movie_id)
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return POSTER_PLACEHOLDER_URL
    poster_path = data.get('poster_path')
    if not poster_path:
        return POSTER_PLACEHOLDER_URL
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

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

    return recommended_movie_names, recommended_movie_posters


movies = load_movies()
similarity = load_similarity()

header_col, animation_col = st.columns([3, 1])
with header_col:
    st.markdown('<h1 class="main-title">🎬 Cinemate Movie Recommender</h1>', unsafe_allow_html=True)
with animation_col:
    lottie_animation = load_lottie_url(LOTTIE_URL)
    if lottie_animation:
        st_lottie(lottie_animation, height=150, key="movie-lottie")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if not TMDB_API_KEY:
    st.warning("TMDB_API_KEY is not set. Placeholder posters will be shown.")

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.balloons()
    columns = st.columns(5)
    for i, column in enumerate(columns):
        with column:
            st.markdown(
                f"""
                <div>
                    <img class="movie-poster" src="{recommended_movie_posters[i]}" alt="{recommended_movie_names[i]}">
                    <div class="movie-title">{recommended_movie_names[i]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )




