import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Baseline activities for reset
BASELINE_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team soccer training, matches and tactics",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": []
    },
    "Swimming Club": {
        "description": "Lap swimming and skill drills in the school pool",
        "schedule": "Mondays and Wednesdays, 3:45 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Acting workshops, stage performance and theater production",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Art Studio": {
        "description": "Painting, drawing, and mixed media creation",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Debate Team": {
        "description": "Competitive public speaking and argument preparation",
        "schedule": "Mondays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 14,
        "participants": []
    },
    "Science Fair Club": {
        "description": "Research projects and science fair preparation",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": []
    }
}

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    global activities
    activities.clear()
    activities.update(BASELINE_ACTIVITIES)

def test_get_activities(client):
    # Arrange: activities are reset to baseline
    
    # Act: GET /activities
    response = client.get("/activities")
    
    # Assert: 200 status and baseline keys
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == set(BASELINE_ACTIVITIES.keys())

def test_signup_success(client):
    # Arrange: reset activities
    
    # Act: POST signup for a new participant
    response = client.post("/activities/Chess%20Club/signup?email=new@student.edu")
    
    # Assert: 200 and participant added
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "new@student.edu" in activities["Chess Club"]["participants"]

def test_signup_duplicate(client):
    # Arrange: signup once
    client.post("/activities/Chess%20Club/signup?email=duplicate@student.edu")
    
    # Act: signup again
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@student.edu")
    
    # Assert: 400
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()

def test_delete_participant(client):
    # Arrange: signup a participant
    client.post("/activities/Chess%20Club/signup?email=to_delete@student.edu")
    
    # Act: DELETE the participant
    response = client.delete("/activities/Chess%20Club/participants?email=to_delete@student.edu")
    
    # Assert: 200 and participant removed
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    assert "to_delete@student.edu" not in activities["Chess Club"]["participants"]

def test_delete_missing_participant(client):
    # Arrange: reset activities
    
    # Act: DELETE non-existent participant
    response = client.delete("/activities/Chess%20Club/participants?email=missing@student.edu")
    
    # Assert: 404
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()

def test_unknown_activity_signup(client):
    # Arrange: reset activities
    
    # Act: POST signup for unknown activity
    response = client.post("/activities/Unknown%20Activity/signup?email=test@student.edu")
    
    # Assert: 404
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()