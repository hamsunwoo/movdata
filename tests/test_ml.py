#from movdata.ml import save_movies
from movdata.ml_copy import save_movies

def test_save_movies():
    r = save_movies(sleep_time=0.1)
    assert r
