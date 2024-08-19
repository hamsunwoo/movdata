import requests
import os
import json
import time
from tqdm import tqdm

API_KEY = os.getenv('MOVIE_API_KEY')

def save_json(data, file_path):
    #파일저장 경로 mkdir
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return True

def req(url):
    r = requests.get(url)
    j = r.json()
    return j

def save_movies(start_year=2014, end_year=2021, sleep_time=1):

    #연도별 저장
    for year in range(start_year, end_year + 1):
        home_path = os.path.expanduser("~")
        file_path = f"{home_path}/data/movies_pagelimit/year={year}/data.json"
    
        #위 경로가 있으면 API 호출을 멈추고 프로그램 종료
        if os.path.exists(file_path):
            print(f"파일이 이미 존재합니다. (연도: {year})")
            continue
        else:
            print(f"데이터를 저장합니다. (연도: {year})")
        

        all_data = []
        url_base = f"https://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={API_KEY}&openStartDt={year}&openEndDt={year}"
        r = req(url_base)
        d = r['movieListResult']['movieList']
        all_data.extend(d)

        #데이터 json파일로 저장
        save_json(all_data, file_path)
    
    return True