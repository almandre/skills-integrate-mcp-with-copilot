
...existing code...

# Função para calcular score de mérito
def calcular_score_merito(student):
    grades = student.get("academic_grades", [])
    activity_scores = list(student.get("activity_scores", {}).values())
    avg_grades = sum(grades) / len(grades) if grades else 0
    avg_activities = sum(activity_scores) / len(activity_scores) if activity_scores else 0
    score = (avg_grades + avg_activities) / 2
    return score

# Endpoint para exibir ranking de alunos por mérito
@app.get("/students/merit-ranking")
def get_merit_ranking():
    ranking = []
    for email, student in students.items():
        score = calcular_score_merito(student)
        ranking.append({
            "email": email,
            "name": student["name"],
            "grade_level": student["grade_level"],
            "score_merito": score
        })
    ranking.sort(key=lambda x: x["score_merito"], reverse=True)
    return ranking
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
activities = {
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
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}

# In-memory student database with academic grades and activity scores
students = {
    "michael@mergington.edu": {
        "name": "Michael",
        "grade_level": 11,
        "academic_grades": [8.5, 9.0, 8.0],  # Example grades
        "activity_scores": {"Chess Club": 9.0}
    },
    "daniel@mergington.edu": {
        "name": "Daniel",
        "grade_level": 11,
        "academic_grades": [7.5, 8.0, 7.0],
        "activity_scores": {"Chess Club": 8.0}
    },
    "emma@mergington.edu": {
        "name": "Emma",
        "grade_level": 10,
        "academic_grades": [9.0, 9.5, 9.0],
        "activity_scores": {"Programming Class": 9.5}
    },
    "sophia@mergington.edu": {
        "name": "Sophia",
        "grade_level": 10,
        "academic_grades": [8.0, 8.5, 8.0],
        "activity_scores": {"Programming Class": 8.5}
    },
    # ...add other students as needed
}


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
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:

        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}

# Função para calcular score de mérito
def calcular_score_merito(student):
    grades = student.get("academic_grades", [])
    activity_scores = list(student.get("activity_scores", {}).values())
    avg_grades = sum(grades) / len(grades) if grades else 0
    avg_activities = sum(activity_scores) / len(activity_scores) if activity_scores else 0
    score = (avg_grades + avg_activities) / 2
    return score

# Endpoint para exibir ranking de alunos por mérito
@app.get("/students/merit-ranking")
def get_merit_ranking():
    ranking = []
    for email, student in students.items():
        score = calcular_score_merito(student)
        ranking.append({
            "email": email,
            "name": student["name"],
            "grade_level": student["grade_level"],
            "score_merito": score
        })
    ranking.sort(key=lambda x: x["score_merito"], reverse=True)
    return ranking
