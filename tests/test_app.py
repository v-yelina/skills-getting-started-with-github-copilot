from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def reset_activities():
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
    })


def test_get_activities():
    reset_activities()
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success():
    reset_activities()
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_fails():
    reset_activities()
    client.post("/activities/Chess Club/signup", params={"email": "dupe@mergington.edu"})
    response = client.post("/activities/Gym Class/signup", params={"email": "dupe@mergington.edu"})
    assert response.status_code == 400


def test_unregister_success():
    reset_activities()
    activities["Chess Club"]["participants"].append("remove@mergington.edu")
    response = client.delete("/activities/Chess Club/participants", params={"email": "remove@mergington.edu"})
    assert response.status_code == 200
    assert "remove@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_missing_fails():
    reset_activities()
    response = client.delete("/activities/Chess Club/participants", params={"email": "missing@mergington.edu"})
    assert response.status_code == 404
