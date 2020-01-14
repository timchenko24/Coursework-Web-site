import pytest
from app import app


def test_index_page():
    with app.test_client() as client:
        r = client.get("/index")
        assert r.status_code == 200

def test_null_page():
    with app.test_client() as client:
        r = client.get("/aaa")
        assert r.status_code == 404