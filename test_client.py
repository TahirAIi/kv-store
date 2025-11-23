import pytest
from fastapi.testclient import TestClient
from main import app

app_client = TestClient(app)

def test_get_put_scenario():
    with open("put.txt", "r") as f:
        for line in f:
            run_test(line)



def run_test(line: str):
    parts = line.strip().split()

    if len(parts) != 3:
        pytest.fail("Incorrect number of arguments")

    method, key, value = parts

    if method == "PUT":
        response = app_client.put(f"/{key}", data=value)
        assert response.status_code == 200

    if method == "GET":
        response = app_client.get(f"/{key}")
        if value == "NOT_FOUND":
            assert response.status_code == 404
        else:
            assert response.status_code == 200 , \
                f"GET {key}: expected 200 but got {response.status_code}"
            assert response.json() == value , \
                f"GET {key}: expected value '{value}' but got '{response.json()}'"

