from application import client

from datetime import date
##database "test"
db = client.test
##collection "user" in database "test"
users = db.users
mealPlans = db.mealPlans
preferences = db.preferences

def find_username(username):
    if users.find_one({"username": username}):
        return True
    else:
        return False

def find_user(username, password):
    if users.find_one({"$and": [{"username": username}, {"password": password}]}):
        return True
    else:
        return False

def get_password(username):
    password_json = users.find_one({"username": username}, {"password": 1})
    pasword = password_json["password"]

    return pasword

def get_primary_goal(username):
    primary_goal_json = users.find_one({"username": username}, {"goal": 1})
    primary_goal = primary_goal_json["goal"]

    return primary_goal

def get_current(username):
    current_json = users.find_one({"username": username}, 
                                  {"currentWeight": 1, "currentHeight": 1})
    
    current_weight = current_json["currentWeight"]
    current_height = current_json["currentHeight"]

    return current_weight, current_height

def get_current_BMI(username):
    current_BMI_json = users.find_one({"username": username}, {"BMI": 1})
    current_BMI = current_BMI_json["BMI"]

    return current_BMI

def get_user_particulars(username):
    user_particulars_json = users.find_one({"username": username},
                                           {"gender": 1, "age": 1, "activityLevel": 1})
    gender = user_particulars_json["gender"]
    age = user_particulars_json["age"]
    activity_level = user_particulars_json["activityLevel"]

    return gender, age, activity_level

def get_activity_level(username):
    activity_level_json = users.find_one({"username": username}, {"activityLevel": 1})
    activity_level = activity_level_json["activityLevel"]

    return activity_level

def get_target(username):
    target_json = users.find_one({"username": username}, 
                                 {"targetWeight": 1, "targetDate": 1})
    target_weight = target_json["targetWeight"]
    target_date = target_json["targetDate"]

    return target_weight, target_date

def get_daily_calories(username):
    daily_calories_json = users.find_one({"username": username}, {"dailyCalories": 1})

    daily_calories = daily_calories_json["dailyCalories"]

    return daily_calories

def get_register_status(username):
    is_complete_json = users.find_one({"username": username}, {"isComplete": 1})

    is_complete = is_complete_json["isComplete"]

    return is_complete

def get_register_step_status(username):
    register_step_status_json = users.find_one({"username": username}, 
                                          {"isCurrentComplete": 1, 
                                           "isPrimaryGoalComplete": 1, 
                                           "isTargetGoalComplete": 1})
    
    is_current_complete = register_step_status_json["isCurrentComplete"]
    is_primary_goal_complete = register_step_status_json["isPrimaryGoalComplete"]
    is_target_goal_complete = register_step_status_json["isTargetGoalComplete"]

    return is_current_complete, is_primary_goal_complete, is_target_goal_complete

def isEmpty_user_mealplan(username):
    isEmpty_json = mealPlans.find_one({"username": username}, {"isEmpty": 1})
    isEmpty = isEmpty_json["isEmpty"]

    return isEmpty

def get_user_mealplan(username):
    mealplan_info_json = mealPlans.find_one({"username": username}, 
                                             {"meals": 1, "nutrients": 1})
    meals = mealplan_info_json["meals"]
    nutrients = mealplan_info_json["nutrients"]

    return meals, nutrients
