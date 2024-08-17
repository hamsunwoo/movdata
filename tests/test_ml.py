from movdata.ml import save_movies
from movdata.movieinfo import save_movies_info
def test_save_movies():
    r = save_movies(sleep_time=0.1)
    assert r


def test_save_movies_info():
    r = save_movies_info()
    assert r
