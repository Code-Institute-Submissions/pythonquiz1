import os
import json


from flask import Flask, redirect, render_template, request, flash, jsonify

app = Flask(__name__)
app.secret_key = 'some_secret'
data = []

def return_user_data(filename, data):
    with open(filename, "a") as file:
        file.writelines(data)

def user_input(username, message):
    return_user_data("data/wrong-answer.txt", "({0}) - {1}\n".format(
            username.title(),
            message))

def pull_messages():
    messages = []
    with open("data/wrong-answer.txt", "r") as chat_messages:
        messages = [row for row in chat_messages if len(row.strip()) > 0]
    return messages

def new_user(username):
    return_user_data("data/usernames.txt", "({0}) - {1}\n".format(username.title()))

def get_users():
    users = []
    with open("data/usernames.txt", "r") as user_messages:
        users = user_messages.readlines()
    return users

@app.route('/users/online', methods=["GET"])
def online_users():
    online_data = open("data/online.txt")
    online_users = [row for row in online_data if len(row.strip()) > 0]
    online_data.close()

    return jsonify(online_users)

@app.route('/', methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    # Handle POST request
    if request.method == "POST":
        return_user_data("data/usernames.txt", request.form["username"] + "\n")
        return_user_data("data/online.txt", request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")


@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    """Display chat messages"""
    data = []
    with open("data/question-answer.json", "r") as json_data:
        data = json.load(json_data)

    riddle_index = 0

    if request.method == "POST":
        # Add user to online users file because he is removed when he attempts to post his answer
        # as page considers him unloading the page
        return_user_data("data/online.txt", username + "\n")

        # Get riddle index from hidden field passed in form
        riddle_index = int(request.form["riddle_index"])

        # Get the user response from input field filled by user
        # We turn the answer to lower case because all answers are in lower case
        # so that SNOWBALLS can be as correct as snowballs
        user_response = request.form["message"].lower()

        # Compare the user's answer to the correct answer of the riddle
        if data[riddle_index]["answer"] == user_response:
            # Correct answer
            # Go to next riddle
            riddle_index += 1
        else:
            # Incorrect answer
            user_input(username, user_response + "\n")

    if request.method == "POST":
        if user_response == "hermes" and riddle_index > 19:
            return render_template("congratulations.html")

    messages = pull_messages()

    online_data = open("data/online.txt")
    online_users = [row for row in online_data if len(row.strip()) > 0]
    online_data.close()

    return render_template("quiz.html",
                            username=username, chat_messages=messages, question_answer=data, online_users=online_users, riddle_index=riddle_index)

@app.route('/players', methods=["GET", "POST"])
def players(username):
    """Display chat historical of players"""

    if request.method == "POST":
        new_user(username, request.form["user"] + "\n")
    users = get_users()
    return render_template("game.html",
                            username=username)

@app.route('/<username>/<message>')
def send_message(username, message):
    """Create a new message and redirect back to the chat page"""
    user_input(username, message)
    return redirect(username)

@app.route('/<username>/log_off', methods=["POST"])
def log_user_off(username):
    online_data = open("data/online.txt")
    online_users = [row for row in online_data if len(row.strip()) > 0 and row.strip() != username]
    online_data.close()

    with open("data/online.txt", "w") as online_data:
        for user in online_users:
            online_data.write('%s\n' % user)

    return;


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'), port=int(os.environ.get('PORT')), debug=True)