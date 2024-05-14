from application.models.mongoDB.get import *

from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import (
    StringField, PasswordField, BooleanField,
    DecimalField, IntegerField, DateField, RadioField, SelectField,
    SubmitField)
from wtforms.validators import (
    ValidationError, DataRequired, Optional,
    Length, EqualTo, NumberRange, Regexp
)

data_required_msg = "Required"

primary_goal_choices = {"lose weight": "lose",
                        "maintain weight": "maintain",
                        "gain weight": "gain"}
activity_level_choices = {"Sedentary" : 1.2, 
                          "Light Exercise" : 1.3, 
                          "Moderate Exercise" : 1.5, 
                          "Heavy Exercise" : 1.7, 
                          "Very Heavy Exercise" : 1.9}

class RegisterForm(FlaskForm):
    def validate_username(form, username_to_check):
        if find_username(username_to_check.data):
            raise ValidationError("Username already exists, please try another username")
    
    username = StringField(
        label = "Username:",
        validators = [
            DataRequired(data_required_msg),
            Length(min = 2, max = 30, message = "Username must be between %(min)d and %(max)d characters"),
            Regexp(r"^[a-zA-Z0-9]+$", message = "Username should not include special letter or space")
        ])
    password = PasswordField(
        label = "Password:",
        validators = [
            DataRequired(data_required_msg),
            Length(min = 8, message = "Password must be %(min)d or more characters")
        ])
    re_password = PasswordField(
        label = "Confirm Password:",
        validators = [
            DataRequired(data_required_msg),
            EqualTo("password", message = "Passwords do not match")
        ])
    agree_policy_label = Markup("<a href='/about/privacy-policy'>Privacy Policy</a>")
    agree_policy = BooleanField(
        label = "I have read and agreed with the " + agree_policy_label,
        validators = [
            DataRequired(data_required_msg)
        ])
    
    submit = SubmitField(label = "Register")

class CurrentBMIForm(FlaskForm): 
    current_weight = DecimalField(
        label = "Curret Weight:",
        places = 2,
        validators = [
            DataRequired(f"{data_required_msg}, Weight must be numeric"),
            NumberRange(min = 20, max=150, message = "Weight must be in the range of %(min)d and %(max)d")
        ])
    current_height = DecimalField(
        label = "Curret Height:",
        places = 2,
        validators = [
            DataRequired(f"{data_required_msg}, Height must be numeric"),
            NumberRange(min = 100, max = 250, message = "Height must be in the range of %(min)d and %(max)d")
        ])
    
    submit_next = SubmitField(label = "Next")

class PrimaryGoalForm(FlaskForm):
    primary_goal = RadioField(
        label = "Select your goal",
        choices = list(primary_goal_choices.keys()),
        validators = [
            DataRequired(data_required_msg)
        ])
    
    submit_back = SubmitField(label = "Back")
    submit_next = SubmitField(label = "Next")

class DailyCaloriesForm(FlaskForm):
    gender = RadioField(
        label = "Gender:",
        choices = ["male", "female"],
        validators = [
            DataRequired(data_required_msg)
        ])
    age = IntegerField(
        label ="Age",
        validators = [
            DataRequired(data_required_msg),
            NumberRange(min = 10, max = 80, message = "Age must be in the range of %(min)d and %(max)d")
        ])
    activity_level = SelectField(
        label = "Activity level:",
        choices = list(activity_level_choices.keys()),
        validators = [
            DataRequired(data_required_msg)   
        ])

    submit_back = SubmitField(label = "Back")
    submit_next = SubmitField()

class TargetGoalForm(FlaskForm):     
    def validate_target_date(form, date_to_check):
        current_date = date.today()
        target_date = date_to_check.data
        if (target_date - current_date).days <= 0:
            raise ValidationError("Target date can only be future date")
            
    target_weight = DecimalField(
        label = "Target Weight:",
        places = 2,
        validators = [
            DataRequired(f"{data_required_msg}, Weight must be numeric"),
            NumberRange(min = 20, max = 150, message = "Weight must be in the range of %(min)d and %(max)d")
        ])
    target_date = DateField(
        label = "Target Date:",
        validators = [
            DataRequired(data_required_msg)
        ])

    submit_back = SubmitField(label = "Back")
    submit_complete = SubmitField(label = "Complete")
