"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities.update({
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
})

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

# Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")


    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
