# Justin Strauss
# Software Development Period 7
# Final Project

from flask import Flask, render_template, request, redirect, session, url_for, flash
import json, requests

app = Flask(__name__)

secrets = json.load(open("secrets.json"))

@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return redirect("https://www.strava.com/oauth/authorize?client_id={0}" \
           "&response_type=code&redirect_uri={1}&scope={2}" \
           "&approval_prompt=auto".format(secrets['client_id'], secrets['redirect_uri'], "view_private,write"))

@app.route("/oauth2callback")
def oauth2callback():
    if 'access_token' not in session:
        if request.args.has_key('error'):
            return "ERROR"
        code = request.args.get('code')
        session['access_token'] = get_token(code)
        return "Authorization is completed"
    return "You authorized already"

# @app.route("/strava_get_userdata")
# def get_friend():
#     headers = {"Authorization" : "Bearer " + AppData.access_token}
#     response_json = requests.get("https://www.strava.com/api/v3/athlete", headers=headers).json()
#     if "errors" in response_json:
#         return response_json["message"]
#     return ("User data:<br><br>Firstname: " + response_json["firstname"] +
#             "<br>Lastname:" + response_json["lastname"] +
#             "<br>Friends:" + str(response_json["friend_count"]) +
#             "<br>Followers:" + str(response_json["follower_count"]))

@app.route("/logout")
def logout():
    if session['access_token']!=None:
        post_data = {"access_token": session['access_token']}
        requests.post("https://www.strava.com/oauth/deauthorize", data=post_data)
        session.pop('access_token', None)
        return "Goodbye"
    return "Error: you not authorized yet"

def get_token(code):
    post_data = {"client_id": secrets['client_id'],
                 "client_secret": secrets['client_secret'],
                 "code": code}
    response = requests.post("https://www.strava.com/oauth/token", data=post_data)
    token_json = response.json()
    token = token_json["access_token"] if "access_token" in token_json.keys() else ""
    return token

if __name__ == "__main__":
    app.secret_key = "don't store this on github"
    app.run(debug=True, port=4242)