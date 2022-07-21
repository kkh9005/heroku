import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()

tmdb.api_key = '5ee26b59321d55a2c9fe631d180a3095'
tmdb.language = 'ko-KR'

movies = pickle.load(open('movies.pickle','rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle','rb'))

#데이터 준비 완료! st을 이용해 화면 구성

st.set_page_config(layout = 'wide')
#화면을 넓게쓰기위해서 wide

#상단에 제목처럼
st.header('Woozi의 영화추천')

def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = enumerate(cosine_sim[idx])
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]

    images = []
    titles = []

    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id)
        #영화제목을 넣으면 상세정보를 얻어올수있다.tmdbapi

        images_path = details['poster_path']
        if images_path:
            image_path = 'https://image.tmdb.org/t/p/w500'+images_path

        else:
            image_path = 'no_image.jpg'
        images.append(image_path)
        titles.append(details['title'])

    return images, titles

movie_list = movies['title'].values
title = st.selectbox('평소 좋아하는 영화를 고르세요 >_<',movie_list)

#버튼만들기
if st.button('추천!'):
    #progress bar만들기
    with st.spinner('잠시 기다려 주세요 ㅠ_ㅠ'):
        images, titles = get_recommendations(title)


    #2줄로나눠 5개씩!화면에 표시

        idx = 0
        for i in range(0,2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1






