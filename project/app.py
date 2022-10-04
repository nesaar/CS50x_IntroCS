import os
import cs50
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# gamestart = datetime(2022,9,15)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///flashword.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET","POST"])
def index():
    # if the session data was not found then assume this is the fist time the user is playing
    # set defaults
    if not session.get('numberofplays'):
        numberOfPlays = 0
        session['numberofplays'] = numberOfPlays
    else:
        numberOfPlays = session['numberofplays']
    
    if not session.get('gameswon'):
        gamesWon = 0
        session['gameswon'] = gamesWon
    else:
        gamesWon = session['gameswon']
    
    if not session.get('scoreone'):
        scoreOne = 0
        session['scoreone'] = scoreOne
    else:
        scoreOne = session['scoreone']
    
    if not session.get('scoretwo'):
        scoreTwo = 0
        session['scoretwo'] = scoreTwo
    else:
        scoreTwo = session['scoretwo']
    
    if not session.get('scorethree'):
        scoreThree = 0
        session['scorethree'] = scoreThree
    else:
        scoreThree = session['scorethree']

    if not session.get('scorefour'):
        scoreFour = 0
        session['scorefour'] = scoreFour
    else:
        scoreFour = session['scorefour']

    print("======== DEBUG INFO SESSION ========")
    print(numberOfPlays)
    print(gamesWon)

    # get the word of the day
    wordoftheday = db.execute("SELECT * FROM soundslike LIMIT 1")

    print("======== DEBUG INFO WORDOFTHEDAY ========")
    print(wordoftheday)

    soundslike = wordoftheday[0]['soundslike']
    description = wordoftheday[0]['description']
    exq = wordoftheday[0]['exq']
    exa = wordoftheday[0]['exa']

    print("======== DEBUG INFO VARIABLES NEEDED ========")
    print(soundslike)
    print(description)
    print(exq)
    print(exa)
    print(request.method)
    print(request.headers)

    session['gameswon'] = gamesWon
    session['soundslike'] = soundslike
    session['description'] = description
    session['exq'] = exq
    session['exa'] = exa

    if request.method == "GET":
        print("======== DEBUG INFO GET ========")
        return render_template("index.html", soundslike=soundslike, description=description, exq=exq, exa=exa, session=session)
    elif request.method == "POST":
        print("======== DEBUG INFO POST ========")
        print(session)
        return redirect("/game")


@app.route("/game", methods=["GET","POST"])
def game():
    wordoftheday = db.execute("SELECT * FROM soundslike LIMIT 1")

    print(wordoftheday)

    soundslike = wordoftheday[0]['soundslike']
    description = wordoftheday[0]['description']
    exq = wordoftheday[0]['exq']
    exa = wordoftheday[0]['exa']

    print("======== DEBUG INFO /GAME GET ========")
    print(wordoftheday[0]['id'])
    print(exq)
    print(exa)

    questionsoftheday = db.execute("SELECT * FROM soundslikeQA WHERE soundslike_id = ?", wordoftheday[0]['id'])
    session['questionsoftheday'] = questionsoftheday

    print("======== DEBUG INFO /GAME GET ========")
    print(questionsoftheday)

    if request.method == "GET":
        return render_template("game.html", questionsoftheday=questionsoftheday, soundslike=soundslike, description=description, exq=exq, exa=exa)
    elif request.method == "POST":
        ans = [{'id': 1, 'uanswer':'', 'correct':'red'},{'id': 2, 'uanswer':'', 'correct':'red'},
            {'id': 3, 'uanswer':'', 'correct':'red'},{'id': 4, 'uanswer':'', 'correct':'red'},
            {'id': 5, 'uanswer':'', 'correct':'red'}]

        ans[0]['uanswer'] = request.form.get("Q1")
        ans[1]['uanswer'] = request.form.get("Q2")
        ans[2]['uanswer'] = request.form.get("Q3")
        ans[3]['uanswer'] = request.form.get("Q4")
        ans[4]['uanswer'] = request.form.get("Q5")

        score = 0

        if ans[0]['uanswer'].lower() == questionsoftheday[0]['answer']:
            score += 1
            ans[0]['correct'] = '#228B22'
        if ans[1]['uanswer'].lower() == questionsoftheday[1]['answer']:
            score += 1
            ans[1]['correct'] = '#228B22'
        if ans[2]['uanswer'].lower() == questionsoftheday[2]['answer']:
            score += 1
            ans[2]['correct'] = '#228B22'
        if ans[3]['uanswer'].lower() == questionsoftheday[3]['answer']:
            score += 1
            ans[3]['correct'] = '#228B22'
        if ans[4]['uanswer'].lower() == questionsoftheday[4]['answer']:
            score += 1
            ans[4]['correct'] = '#228B22'

        print("======== DEBUG INFO /GAME POST ========")
        print(ans)
        print(questionsoftheday)
        print(score)

        # read the session data for stats purposes and saving
        numberOfPlays = session['numberofplays']
        gamesWon = session['gameswon']
        scoreOne = session['scoreone']
        scoreTwo = session['scoretwo']
        scoreThree = session['scorethree']
        scoreFour = session['scorefour']

        if score == 5:
            gamesWon += 1
        elif score == 4:
            scoreFour += 1
        elif score == 3:
            scoreThree += 1
        elif score == 2:
            scoreTwo += 1
        elif score == 1:
            scoreOne += 1

        numberOfPlays += 1

        # write the session variables for storage
        session['numberofplays'] = numberOfPlays
        session['gameswon'] = gamesWon 
        session['scoreone'] = scoreOne 
        session['scoretwo'] = scoreTwo
        session['scorethree'] = scoreThree
        session['scorefour'] = scoreFour  
        session['score'] = score
        session['ans'] = ans

        print("======== DEBUG INFO /GAME POST SESSION ========")
        print(session)

        return redirect("/score")

@app.route("/score")
def score():
    return render_template("score.html", score=session['score'], questionsoftheday=session['questionsoftheday'],
        soundslike=session['soundslike'], description=session['description'], exq=session['exq'],
            exa=session['exa'], ans=session['ans'])

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)