import requests
import os
import json
import time
from tqdm import tqdm

API_KEY = os.getenv('MOVIE_API_KEY')

#JSON 파일열고 MovieCd 추출하기
def extract_movie_list_json(movieCd):
    
    home_path = os.path.expanduser("~")
    start_year = 2015
    end_year = 2021

    #모든 연도의 movieCd를 저장할 리스트
    all_moviecd = []

    for year in range(start_year, end_year + 1):
        movie_list_path=f"{home_path}/data/movies/year={year}/data.json"


    #MovieList JSON 파일 열기
    if os.path.exists(movie_list_path):
        with open(movie_list_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
        #JSON파일에서 MovieCd 추출하기
        for key in data:
            if movieCd in key:
                all_moviecd.append({"year": year, "movieCd": key[movieCd]})
    else:
        print(f"{movie_list_path} 파일이 존재하지 않습니다.")
    
    return all_moviecd

#영화 상세정보 JSON파일로 저장
def save_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return True

#영화 상세정보 url
def req(url):
    r = requests.get(url)
    j = r.json()
    return j


#영화 상세정보 저장
def save_movies_info():
    movie_code_key = 'movieCd'
    extract_movie_code = extract_movie_list_json(movie_code_key)
    
    movie_info_by_year = {}

    for key in tqdm(extract_movie_code):
        year = key['year']
        code = key['movieCd']
        home_path = os.path.expanduser("~")
        file_path = f"{home_path}/data/movies/year={year}/movie_info.json"
    
        #영화 정보가 이미 연도의 movie_info.json에 저장되어 있는지 확인
        if year not in movie_info_by_year:
            movie_info_by_year[year] = []

            #기존 movie_info.json이 존재하면 로드
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    movie_info_by_year[year] = json.load(f)
       
       #중복 확인(이미 저장된 movieCd인지 확인)
        if any(movie.get('movieCd') == code for movie in movie_info_by_year[year]):
           print(f"영화 정보가 이미 존재합니다: {year}년 {code}")
           continue

        #API 호출
        url_base = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={API_KEY}&movieCd={code}"
        movie_info = req(url_base).get('movieInfoResult', {}).get('movieInfo', {})
        
        #연도별로 영화상세정보 리스트에 다 저장
        movie_info_by_year[year].append(movie_info)

        #데이터를 연도별로  json 파일로 저장
        for year, movie_info_list in movie_info_by_year.items():
            file_path = f"{home_path}/data/movies/year={year}/movie_info.json"
            save_json(movie_info_list, file_path)
            print(f"영화 정보를 저장했습니다: {year}년 {code}")
    
    return True
