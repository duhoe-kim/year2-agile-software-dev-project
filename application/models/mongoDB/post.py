from application import client

from datetime import date
##database "test"
db = client.test
##collection "user" in database "test"
users = db.users
mealplans = db.mealPlans
preferences = db.preferences

##user particulars
def insert_user(username, password):
    user_doc = {
        "username": username,
        "password": password,
        "gender": "",
        "age": 0,

        "currentWeight": 0,
        "currentHeight": 0,
        "BMI" : 0,

        "goal": "",
        "activityLevel": "",

        "targetWeight": 0,
        "targetDate": "",
        "startDate": "",

        "dailyCalories": 0,

        "isCurrentComplete": False,
        "isPrimaryGoalComplete": False,
        "isTargetGoalComplete": False,

        "isComplete": False           
    }

    meal_plan_doc = {
        "username": username,
        "isEmpty": True,

        "meals": [],
        "nutrients": []
    }

    users.insert_one(user_doc)
    mealplans.insert_one(meal_plan_doc)

def update_username(username, new_username):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "username": new_username
    }}

    users.update_one(filter, newvalues)
    mealplans.update_one(filter, newvalues)
        
def update_password(username, new_password):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "password": new_password
    }}
    users.update_one(filter, newvalues)

def update_current_BMI(username, current_weight, current_height, BMI):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "currentWeight": current_weight, 
            "currentHeight": current_height,
            "BMI" : BMI,

            "isCurrentComplete": True
    }}
    users.update_one(filter, newvalues)

def update_primary_goal(username, goal):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "goal": goal,

            "isPrimaryGoalComplete": True
    }}

    users.update_one(filter, newvalues)

def update_user_info(username, gender, age, activity_level):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "gender": gender,
            "age" : age,
            "activityLevel" : activity_level
    }}

    users.update_one(filter, newvalues)

def update_activity_level(username, activity_level):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "activityLevel" : activity_level
    }}

    users.update_one(filter, newvalues)

def update_target(username, target_weight, target_date):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "targetWeight": target_weight, 
            "targetDate": date.isoformat(target_date),
            "startDate": date.isoformat(date.today()),

            "isTargetGoalComplete": True,
            "isComplete": True
    }}

    users.update_one(filter, newvalues)

def update_new_target(username, target_weight, target_date):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "targetWeight": target_weight, 
            "targetDate": date.isoformat(target_date),
    }}

    users.update_one(filter, newvalues)

def reset_target(username):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "targetWeight": 0, 
            "targetDate": "",
    }}

    users.update_one(filter, newvalues)

def update_user_goal(username, daily_calories):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "dailyCalories" : daily_calories,

            "isTargetGoalComplete": True,
            "isComplete": True
    }}

    users.update_one(filter, newvalues)

def update_user_mealplan(username, meals, nutrients):
    filter = {"username": username}
    newvalues = {
        "$set": {
            "isEmpty": False,
            "meals": meals,
            "nutrients": nutrients
    }}

    mealplans.update_one(filter, newvalues)
