from application.logics.calculation import *
from application.models.mongoDB.get import *

import bcrypt

class CustomErrorMessage(Exception):
    pass

def validate_primary_goal(BMI, primary_goal):
    if primary_goal == "lose" and (BMI - 2) < 19:
        raise CustomErrorMessage("Your goal would lead to underweight")
    if primary_goal == "gain" and (BMI + 2) >= 24.9:
         raise CustomErrorMessage("Your goal would lead to obesity")

def validate_target_weight(current_weight, target_weight, primary_goal):
    if primary_goal == "lose" and current_weight < target_weight:
        raise CustomErrorMessage("You will gain weight instead!")
    elif primary_goal == "gain" and current_weight > target_weight:
        raise CustomErrorMessage("You will lose weight instead!")
    elif current_weight == target_weight:
        raise CustomErrorMessage("You will maintain weight instead!")

def validate_target_BMI(target_weight, current_height):
    target_BMI = calculate_BMI(target_weight, current_height)

    if target_BMI <= 19:
        raise CustomErrorMessage("Your target weight would lead to underweight")
    elif target_BMI >= 30:
        raise CustomErrorMessage("Your target weight would lead to obesity")

def validate_target(adc, daily_calories):
    acceptable_range = daily_calories/5

    if acceptable_range < adc:
        raise CustomErrorMessage("Current target would cause damge to your health")

def validate_new_password(username, new_password):
    old_password_hashed = get_password(username)
    new_password_hashed = bcrypt.hashpw(new_password.encode("utf-8"), old_password_hashed)

    if old_password_hashed == new_password_hashed:
        raise CustomErrorMessage("New password is same as the old password, Please use other password")
    
def validate_new_current_weight(old_current_weight, new_current_weight):
    if abs(old_current_weight - new_current_weight) > 5:
        raise CustomErrorMessage("Plesae enter valid weight for your new current weight")

def validate_new_current_weight(old_current_height, new_current_height):
    if abs(old_current_height - new_current_height) > 5:
        raise CustomErrorMessage("Plesae enter valid weight for your new current height")
    
