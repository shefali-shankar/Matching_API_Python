from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test for exact match
def test_exact_match():
    test_input = {"trade": "Painting", "unit_of_measure": "M2"}
    response = client.post("/match", json=test_input)
    assert response.status_code == 200
    assert response.json() == {
        "best_match": {
            "trade": "Painting",
            "unit_of_measure": "M2",
            "rate": 23.0
        },
        "similarity_score": 1.0
    }

# Test for partial match
def test_partial_match():
    test_input = {"trade": "paint", "unit_of_measure": "HouR"}
    response = client.post("/match", json=test_input)
    assert response.status_code == 200
    assert response.json()["similarity_score"] < 1.0

# Test for no match
def test_no_match():
    test_input = {"trade": "Mason", "unit_of_measure": "Days"}
    response = client.post("/match", json=test_input)
    assert response.status_code == 404
    assert response.json() == {"detail": "No matching trade item found"}

# Test for Invalid Data format
def test_invalid_data_format():
    test_input = {"tr": ""}
    response = client.post("/match", json=test_input)
    assert response.status_code == 422
    assert response.json()["body"] == f"Invalid Data format. {test_input}"

# Test for Empty Strings
def test_empty_string():
    test_input = {"trade": "","unit_of_measure": "  "}
    response = client.post("/match", json=test_input)
    assert response.status_code == 404
    assert response.json() == {"detail":"One or more Input Strings are empty."}
