from application import app

from flask import render_template

@app.route("/about/about-us")
def about_us():

    return render_template("about/about_us.html")

@app.route("/about/privacy-policy")
def privacy_policy():

    return render_template("about/privacy_policy.html")
