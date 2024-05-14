from application import app
from application.forms.register import *
from application.logics.calculation import *
from application.logics.validation import *

from application.models.mongoDB.post import *
from application.models.mongoDB.get import *

from flask import (
    render_template, redirect, url_for, flash,
    session
)
import bcrypt

@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        insert_user(username, hash_password)

        return redirect(url_for("current_BMI", username = username))

    return render_template("register/00register.html", 
                           form=form)

@app.route("/register/<username>/current-bmi", methods = ["GET", "POST"])
def current_BMI(username):
    verify_current_session(username)

    form = CurrentBMIForm()
    
    if form.validate_on_submit():
        session["current_weight"] = float(form.current_weight.data)
        session["current_height"] = float(form.current_height.data)
        session["BMI"] = calculate_BMI(session["current_weight"], session["current_height"])

        update_current_BMI(username, session["current_weight"], session["current_height"], session["BMI"])

        return redirect(url_for("primary_goal", username = username))

    return render_template("register/01current_BMI.html",
                           username = username,
                           current_weight_input = session["current_weight"],
                           current_height_input = session["current_height"],
                           form = form)

@app.route("/register/<username>/primary-goal", methods = ["GET", "POST"])
def primary_goal(username):
    verify_BMI_session(username)
    verify_primary_goal_input_session(username)

    rec_primary_goal = calculate_rec_primary_goal(session["BMI"])

    form = PrimaryGoalForm()
        
    if form.is_submitted():
        session["primary_goal_input"] = form.primary_goal.data

        if form.submit_back.data:
            return redirect(url_for("current_BMI", username = username))

        if form.submit_next.data:
            if form.validate_on_submit():
                primary_goal = primary_goal_choices[form.primary_goal.data]
                try:
                    validate_primary_goal(session["BMI"], primary_goal)
                except Exception as e:
                    flash(e, category = "warning")
                else:
                    update_primary_goal(username, primary_goal)
                    return redirect(url_for("daily_calories", username = username))          
    
    return render_template("register/02primary_goal.html",
                           rec_primary_goal = rec_primary_goal,
                           current_BMI = session["BMI"],
                           primary_goal_input = session["primary_goal_input"],
                           form = form)

@app.route("/register/<username>/daily-caloires", methods = ["GET", "POST"])
def daily_calories(username):
    verify_current_session(username)
    verify_primary_goal_session(username)

    declare_user_particulars_session()

    form = DailyCaloriesForm(activity_level = session["activity_level_input"])

    if form.is_submitted():
        session["gender"] = form.gender.data
        session["age"] = form.age.data
        session["activity_level_input"] = form.activity_level.data

        if form.submit_back.data:
            return redirect(url_for("primary_goal", username = username))
        
        if form.submit_next.data:
            if form.validate_on_submit():
                activity_level = activity_level_choices[form.activity_level.data]

                update_user_info(username, session["gender"], session["age"], activity_level)
                
                session["daily_calories"] = calculate_daily_calories(session["current_weight"], session["current_height"], 
                                                                     session["age"], session["gender"], activity_level)
                
                if session["primary_goal"] == "maintain":
                    update_user_goal(username, session["daily_calories"])
                    
                    clear_all_register_session()
                    flash("Register Successful", category = "success")
                    return redirect(url_for("login"))
                else:
                    return redirect(url_for("target_goal", username = username))
    
    return render_template("register/03daily_calories.html",
                           primary_goal = session["primary_goal"],
                           gender_input = session["gender"],
                           age_input = session["age"],
                           form = form)

@app.route("/register/<username>/target-goal", methods = ["GET", "POST"])
def target_goal(username):
    verify_current_session(username)
    verify_BMI_session(username)
    verify_user_particulars_session(username)
    verify_daily_calories_session(username)

    declare_target_input_session()

    rec_target_weight, rec_target_date = calculate_rec_target(session["current_weight"], session["current_height"], session["BMI"], 
                                                              session["primary_goal"], session["daily_calories"])

    form = TargetGoalForm()

    if form.is_submitted():
        session["target_weight"] = form.target_weight.data
        session["target_date"] = form.target_date.data

        if form.submit_back.data:
            return redirect(url_for("daily_calories", username = username))

        if form.submit_complete.data:
            if form.validate_on_submit():
                target_weight = float(session["target_weight"])
                target_date = session["target_date"]
            
                try:
                    validate_target_weight(session["current_weight"], target_weight, session["primary_goal"])
                    validate_target_BMI(target_weight, session["current_height"])
                    
                    adc = calculate_ADC(session["current_weight"], target_weight, target_date)

                    validate_target(adc, session["daily_calories"])
                except Exception as e:
                    flash(e, category = "warning")
                else:
                    target_daily_calories = calculate_daily_calories(target_weight, session["current_height"],
                                                                     session["age"], session["gender"], session["activity_level"])
                    update_target(username, target_weight, target_date)
                    update_user_goal(username, target_daily_calories)
                    
                    clear_all_register_session()
                    flash("Register Successful", category = "success")
                    return redirect(url_for("login"))     
                 
    return render_template("register/04target_goal.html",    
                           rec_target_weight = rec_target_weight,
                           rec_target_date = rec_target_date,                       
                           target_weight_input = session["target_weight"],
                           target_date_input = session["target_date"],
                           form = form)

def verify_current_session(username):
    if session.get("current_weight") == None or session.get("current_height") == None:
        session["current_weight"], session["current_height"] = get_current(username)

def verify_BMI_session(username):
    if session.get("BMI") == None:
        session["BMI"] = get_current_BMI(username)

def verify_primary_goal_input_session(username):
    if session.get("primary_goal_input") == None:
        session["primary_goal_input"] = None
        primary_goal_value = get_primary_goal(username)
        for key, value in primary_goal_choices.items():
             if value == primary_goal_value: session["primary_goal_input"] = key

def verify_primary_goal_session(username):
    if session.get("primary_goal_input") == None:
        session["primary_goal"] = get_primary_goal(username)
    else:
        session["primary_goal"] = primary_goal_choices[session["primary_goal_input"]]

def declare_user_particulars_session():
    if session.get("gender") == None:
        session["gender"] = None

    if session.get("age") == None:
        session["age"] = None

    if session.get("activity_level_input") == None:
        session["activity_level_input"] = None
        
def verify_daily_calories_session(username):
    if session.get("daily_calories") == None:
        session["daily_calories"] = get_daily_calories(username)

def verify_user_particulars_session(username):
    if session.get("gender") == None or session.get("age") == None or session.get("activity_level_input"):
        session["gender"], session["age"], session["activity_level"] = get_user_particulars(username)
    else:
        session["activity_level"] = activity_level_choices[session["activity_level_input"]]

def declare_target_input_session():
    if session.get("target_weight") == None:
        session["target_weight"] = None

    if session.get("target_date") == None:
        session["target_date"] = None

def clear_all_register_session():
    session["current_weight"] = None
    session["current_height"] = None
    session["BMI"] = None
    session["primary_goal_input"] = None
    session["primary_goal"] = None
    session["gender"] = None
    session["age"] = None
    session["activity_level_input"] = None
    session["activity_level"] = None
    session["target_weight"] = None
    session["target_date"] = None
