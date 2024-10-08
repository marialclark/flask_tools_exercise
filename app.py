from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

RESPONSES = "responses"

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Shows user the survey."""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/questions/<int:index>', methods=["GET", "POST"])
def questions_page(index):
    """Displays a questions and its choices while protecting against invalid access."""
    responses = session.get(RESPONSES)
    if len(responses) >= len(satisfaction_survey.questions):
        return redirect('/thankyoupage')
    if index != len(responses) or index >= len(satisfaction_survey.questions):
        flash(f"Error: You are trying to access an invalid question.")
        return redirect(f'/questions/{len(responses)}')
    title = satisfaction_survey.title
    question = satisfaction_survey.questions[index].question
    choices = satisfaction_survey.questions[index].choices
    return render_template('questions.html', title=title, question=question, choices=choices)

@app.route('/answer', methods=['POST']) 
def append_ans():  
    """Appends survey question answer to responses list."""
    answer = request.form['answer']
    responses = session[RESPONSES]
    responses.append(answer)
    session[RESPONSES] = responses
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(responses)}')
    return redirect('/thankyoupage')

@app.route('/thankyoupage')
def thankyou():
    return render_template('thankyou.html')

@app.route('/new-session', methods=['POST'])
def new_session():
    """Clears the session responses."""
    session[RESPONSES] = []
    return redirect('/questions/0')