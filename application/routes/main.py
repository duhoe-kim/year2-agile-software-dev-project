from application import app
from application.forms.main import *
from application.logics.validation import *

from application.models.mongoDB.get import *
from application.models.mongoDB.post import *
from application.models.api import *

from flask import (
    render_template, redirect, url_for, flash,
    session
)
from functools import wraps
import bcrypt

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("user"):
            return f(*args, **kwargs)
        else:
            flash("login required", category = "warning")
            return redirect(url_for("index"))
    
    return wrap

def registeration_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("user"):
            is_complete = get_register_status(session["user"])
        else:
            flash("Your are not logged in. Please login again", category = "warning")
            return redirect(url_for("index"))
        
        if is_complete == True:
            return f(*args, **kwargs)
        else:
            flash("Please complete your registeration steps before proceeding", category = "warning")
            
            username = session["user"]
            session["user"] = None
            is_current_complete, is_primary_goal_complete, is_target_goal_complete = get_register_step_status(username)
                
            if is_current_complete == False:
                return redirect(url_for("current_BMI", username = username))
            elif is_primary_goal_complete == False:
                return redirect(url_for("primary_goal", username = username))
            elif is_target_goal_complete == False:
                return redirect(url_for("daily_calories", username = username))
    
    return wrap

@app.route("/", methods = ["GET", "POST"])
def index():
    if session.get("user"):
        return redirect(url_for("home", username = session["user"]))
    else:
        return redirect(url_for("login"))

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username_to_verify = form.username.data
        password_to_verify = form.password.data
        
        try:
            if find_username(username_to_verify):
                username = form.username.data
            else: raise Exception
            
            user_password = get_password(username)
            hash_password_to_verify = bcrypt.hashpw(password_to_verify.encode("utf-8"), user_password)

            if find_user(username, hash_password_to_verify):
                session["user"] = username
                return redirect(url_for("index"))
            else: raise Exception
        except Exception:
            flash("Bad username or password. Please try again", category = "error")

    return render_template("main/login.html",
                           form = form)

@app.route("/logout/<username>", methods = ["GET"])
@login_required
def logout(username):
    session["user"] = None

    flash("Logout Successful", category = "success")

    return redirect(url_for("index"))
    
@app.route("/home/<username>", methods = ["GET", "POST"])
@registeration_required
@login_required
def home(username):
    daily_calories = get_daily_calories(username)
    form = MealplanForm()

    if form.validate_on_submit():
        calories = form.target_calories.data
        diet = diet_choices[form.diet.data]["field"]

        meal_plan = get_meal_plans(calories, diet)
        update_user_mealplan(username, meal_plan["meals"], meal_plan["nutrients"])
    
    isEmpty = isEmpty_user_mealplan(username)
    meals, nutrients = get_user_mealplan(username)
    
    return render_template("main/home.html",
                           username = username,
                           daily_calories = daily_calories,
                           isEmpty = isEmpty,
                           meals = meals,
                           nutrients = nutrients,
                           form = form)

@app.route("/setting/<username>", methods = ["GET", "POST"])
@app.route("/setting/<username>/<option>", methods = ["GET", "POST"])
@login_required
def setting(username, option = "change-username"):
    set_current_session(username)
    set_goal_session(username)
    set_target_session(username)

    # change username
    current_username = username

    username_form = UpdateUsernameForm()

    if username_form.submit_username.data and username_form.validate_on_submit():
        new_username = username_form.username.data
        update_username(current_username, new_username)
    
        session["user"] = new_username

        flash("Successfully updated your username", category = "success")
        return redirect(url_for("setting", username = session["user"], option = "change-username"))
   
    # change password
    new_password_input_error = None

    password_form = UpdatePasswordForm()

    if password_form.submit_password.data and password_form.validate_on_submit():
        new_password = password_form.password.data 
        
        try:
            validate_new_password(username, new_password)
        except Exception as e:
            new_password_input_error = e
        else:
            hash_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
            update_password(username, hash_new_password)
            flash("Successfully updated your password", category = "success")

    # update current
    current_error = False
    new_current_weight_input_error = None
    new_current_height_input_error = None

    current_form = UpdateCurrentForm()

    if current_form.submit_current.data and current_form.validate_on_submit():
        new_current_weight = float(current_form.current_weight.data)
        new_current_height = float(current_form.current_height.data)

        while(True):
            try:
                validate_new_current_weight(session["current_weight"], new_current_weight)
            except Exception as e:
                new_current_weight_input_error = e
                current_error = True

            try:
                validate_new_current_weight(session["current_height"], new_current_height)
            except Exception as e:
                new_current_height_input_error = e
                current_error = True
            
            if current_error == True:
                break
            else:
                BMI = calculate_BMI(new_current_weight, new_current_height)
                update_current_BMI(username, new_current_weight, new_current_height, BMI)

                session["current_weight"] = new_current_weight
                session["current_height"] = new_current_height
                flash("Successfully updated your current weight and height", category = "success")

                break
    
    goal_form = UpdateGoalForm(primary_goal = session["primary_goal_selected"], 
                                activity_level = session["activity_level_selected"])
    
    if goal_form.submit_goal.data and goal_form.validate_on_submit():
        session["primary_goal_selected"] = goal_form.primary_goal.data

        current_BMI = get_current_BMI(username)
        new_primary_goal = primary_goal_choices[goal_form.primary_goal.data]
        new_activity_level = activity_level_choices[goal_form.activity_level.data]

        while(True):
            try:
                validate_primary_goal(current_BMI, new_primary_goal)
            except Exception as e:
                flash(e, category = "warning")
                break
            else:
                update_primary_goal(username, new_primary_goal)
                update_activity_level(username, new_activity_level)
                if new_primary_goal == "maintain":
                    reset_target(username)

                flash("Successfully updated your goal", category = "success")                
                break

    target_form = UpdateTargetForm()

    if target_form.submit_target.data and target_form.validate_on_submit():
        while(True):
            new_target_weight = float(target_form.target_weight.data)
            new_target_date = target_form.target_date.data

            try:
                primary_goal = get_primary_goal(username)
                validate_target_weight(session["current_weight"], new_target_weight, primary_goal)
                validate_target_BMI(new_target_weight, session["current_height"])

                adc = calculate_ADC(session["current_weight"], new_target_weight, new_target_date)
                current_daily_calories = get_daily_calories(username)
                
                validate_target(adc, current_daily_calories)
            except Exception as e:
                flash(e, category = "warning")
                break
            else:
                target_daily_calories = calculate_target_calories(adc, current_daily_calories, primary_goal)    
            
                update_new_target(username, new_target_weight, new_target_date)
                update_user_goal(username, target_daily_calories)
                
                flash("Successfully updated your target", category = "success")
                set_target_session(username)

                break

    return render_template("main/setting.html",
                            username = username,
                            option = option,
                            username_form = username_form,

                            password_form = password_form,
                            new_password_input_error = new_password_input_error,

                            current_form = current_form,
                            current_weight = session["current_weight"],
                            current_height = session["current_height"],
                            new_current_weight_input_error = new_current_weight_input_error,
                            new_current_height_input_error = new_current_height_input_error,

                            goal_form = goal_form,
                            primary_goal_selected = session["primary_goal_selected"],
                            
                            target_form = target_form,
                            current_target_weight = session["target_weight"],
                            current_target_date = session["target_date"])

def set_current_session(username):
    session["current_weight"], session["current_height"] = get_current(username)

def set_target_session(username):
    session["target_weight"], session["target_date"] = get_target(username)

def set_goal_session(username):
    primary_goal = get_primary_goal(username)
    activity_level = get_activity_level(username)

    session["primary_goal_selected"] = None
    session["activity_level_selected"] = None

    for key, value in primary_goal_choices.items():
        if value == primary_goal: session["primary_goal_selected"] = key
    for key, value in activity_level_choices.items():
        if value == activity_level: session["activity_level_selected"] = key
