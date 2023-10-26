from src import app
from flask import render_template, request, redirect, url_for
from src.models.User import findUserByUsername

#route index
@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        username = request.form["username"]
        try:
            user = findUserByUsername(username)
            data = {
                "username": user.username,
                "email": user.email
            }
        except Exception as err:
            print (err)

    else:
        data = {
            "username": "Not specified",
            "email": "Not specified"
        }
    return render_template('index.html.j2', data = data)

