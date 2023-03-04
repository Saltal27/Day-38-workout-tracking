import requests
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

# ---------------------------- CONSTANT VARIABLES ------------------------------- #
load_dotenv(find_dotenv())
NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
HEADERS = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "Content-Type": "application/json",
    "Authorization": os.environ.get("TOKEN"),
}

# ---------------------------- GETTING THE EXERCISES INFO ------------------------------- #
user_exercises = input("Tell me what exercises you did today:\n")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_request_body = {
 "query": user_exercises,
 "gender": "male",
 "weight_kg": 85,
 "height_cm": 187,
 "age": 21,
}

response = requests.post(url=exercise_endpoint, json=exercise_request_body, headers=HEADERS)
# print(response.text)

exercises_list = response.json()["exercises"]

# ---------------------------- SAVING THE DATA INTO GOOGLE SHEETS ------------------------------- #
today = datetime.now()

sheety_api_endpoint = "https://api.sheety.co/6f99efa404162352318a74763b1e629c/myWorkouts/workouts"
for exercise in exercises_list:
    sheety_body_request = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%H:%M:%S"),
            "exercise": exercise["name"].capitalize(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheety_response = requests.post(url=sheety_api_endpoint, json=sheety_body_request, headers=HEADERS)

    # print(sheety_body_request)
    # print(sheety_response.text)

# I ran for 8 miles, cycled for 20 minutes and swam for 1 hour
