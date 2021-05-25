from flask import Flask, session, redirect, request, render_template_string
from flask_session import Session
import os

# define an app (this is part of the standard method for using flask)
app = Flask(__name__)

session_life_in_seconds = 3600
app.config.update(SECRET_KEY="We just need a secret here: I like yellow.")
app.config.update(SESSION_TYPE="filesystem")
app.config.update(PERMANENT_SESSION_LIFETIME=session_life_in_seconds)
app.config.update(SESSION_FILE_DIR=os.path.join("output_no_git","way_2"))

# Hmmmm How to describe this?
Session(app)

# Define a route in the normal way
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/index")
def index():

    # Url arguments can be added to the url like this ?name=Peter&age=57
    # Get the url arguments if there are any
    url_arguments = request.args.to_dict(flat=False)

    # In this demo app, I allow the session to be cleared down if there
    # is a url argument (clear_session)
    # let's see if I am supposed to clear down the session
    if url_arguments.get("clear_session"):
        keys_to_delete = []
        for key, value in session.items():
            keys_to_delete.append(key)

        for key in keys_to_delete:
            session.pop(key, None)

        # no do a straight redirectback to this page so
        # that we can lose the url arguments
        return redirect("/index")

    # Now see if we have a session name set. If not then set it to default
    try:
        name = session["name"]
    except:
        name = "default name"
        session["name"] = name

    # Let's see if I have a list in the session for
    # all_form_packages. Create one if not
    try:
        _ = session["all_form_packages"]
    except:
        session["all_form_packages"] = []

    # Let's see if I have a list in the session for
    # all_url_arguments. Create one if not
    try:
        _ = session["all_url_arguments"]
        print("all url arguments exists in session")
    except:
        session["all_url_arguments"] = []
        print("all url arguments has just been created in session")

    # if there are any url arguments, print them to the console here
    if len(url_arguments) > 0:
        print(f"\nThere were some url arguments and they were:\n{url_arguments}\n")
        session["all_url_arguments"].append(url_arguments)

    # When pages contain a form, we can access the variables in this function
    # if the form was submitted
    # Create a default form_package in case the form not submitted
    form_package = {}
    # And now check to see if the form was actually submitted
    if request.method == "POST":

        # pull the form fields into a dictionary for ease
        form_package = request.form.to_dict(flat=False)

        # print the form fields to trhe console so we can see it was submitted
        print(f"\nThe form was submitted. The data is:\n{form_package}\n")

        # now update the session with the name from the form
        session["name"] = form_package["first_name"][0]

        session["all_form_packages"].append(form_package)

    # define a session package to pass down
    session_package = {}
    for key, value in session.items():
        print(key, value)
        session_package[key] = value

    # create a string of jinja 
    jinja_html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body style="font-family: sans-serif;margin-left: 30px;">
    <h1>Managing persistent data with sessions - Way 2</h1>
    <ul>
        <li>It's encoded into a cookie which is stored within the browser managed storage</li>
        <li>The state data is all stored on the web server with a "key" accessed storage method</li>
        <li>The web server uses the unique identifier that is passed via the cookie to access the state data</li>
        <li>The unique id in the cookie is encoded but not encrypted</li>
        <li>This demo is designed to be used whilst inpsecting the python source code to understand what is happening</li>
        <li>The python code in the route takes all the url and form data submitted and adds it to the session data</li>
        <li>So you can see these building up as more forms are submitted and more url arguments are used</li>
        </ul>
    <h2>Your name as stored in the session is: {{session_package["name"]}}</h2>
    <p>it's updated when you submit a new name via a form</p>
    <h2>We wrote something in routes that can clear the session down</h2>
    <a href="/?clear_session=True">Clear the session down</a>
    <h2>The following links will do gets with and without url_arguments:</h2>
    <ul>
        <li><a href="/">Get with no URL arguments</a></li>
    </ul>
    <ul>
        <li><a href="/?age={{ range(21, 65) | random }}">Get with a random URL argument</a></li>
    </ul>


    <h2>Submit a form to replace the name stored in the session</h2>
    <form action="\" method="post">
        <label for="first_name">First name:</label><br>
        <input type="text" id="first_name" name="first_name" value="Peter"><br>
        <input type="submit" value="Submit">
    </form>
    <h2>In the section below, you can see the session, form and url packages</h2>

    {% if session_package %}
    <h3>Session Package</h3>
    <div>
        <ul>
            {% for key, value in session_package.items() %}
            <li><strong>Key:</strong> {{ key }}, <strong>Value:</strong> {{ value}}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}

    {% if form_package %}
    <h3>Form Package</h3>
    <div>
        <ul>
            {% for key, value in form_package.items() %}
            <li><strong>Key:</strong> {{ key }}, <strong>Value:</strong> {{ value}}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}

    {% if url_arguments %}
    <h3>URL Arguments</h3>
    <div>
        <ul>
            {% for key, value in url_arguments.items() %}
            <li><strong>Key:</strong> {{ key }}, <strong>Value:</strong> {{ value}}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}

</body>

</html>
    """

    # indicate that the session data has been modified 
    session.modified = True

    # render the jinja_html with jinja 
    html = render_template_string(
        jinja_html,
        session_package=session_package,
        url_arguments=url_arguments,
        form_package=form_package,
    )
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port="5002")

