from flask import Flask, render_template, request, redirect, session, url_for, flash
import urllib2, json, urllib, math, time, string

app = Flask(__name__)

secrets = json.load(open("secrets.json"))

@app.route("/")
def index():
    if 'user' not in session:
        return redirect("/login")
    return "<h1>Welcome %s</h1>"%(session['user'])

@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route("/login")
def login():
    url="https://www.strava.com/oauth/authorize"
    data = urllib.urlencode(secrets['request_redirect'])
    req = urllib2.Request(url+"?"+data)
    response = urllib2.urlopen(req)
    result = response.read()
    return result

@app.route("/oauth2callback")
def oauth2callback():
    if request.args.has_key('error'):
        return "ERROR"

    url = "https://www.strava.com/oauth/token"
    code = request.args.get('code')
    values = secrets['request_token']
    values['code'] = code

    data = urllib.urlencode(values)
    req = urllib2.Request(url,data)
    response = urllib2.urlopen(req)
    rawresult = response.read()
    d = json.loads(rawresult)
    url = "https://www.strava.com/api/v3/athlete?access_token=%s"%(d['access_token'])
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    rawresult = response.read()
    d = json.loads(rawresult)
    session['user']=d['email']
    return redirect("/")

if __name__ == '__main__':
    	app.secret_key = "don't store this on github"
	app.debug = True
	app.run(host='0.0.0.0',port=4242)