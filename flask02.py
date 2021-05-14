# import the flask and request modules
from flask import Flask, request, render_template_string, redirect, url_for, session

# define an app (this is part of the standard method for using flask)
app = Flask(__name__)

# Set up a secret key that is used to encrypt and decrypt some items passed
# to the browser 
app.config["SECRET_KEY"] = "We just need a secret here: I like yellow."

# Define our first route (the last part of the url for our website application)
# We can define what urls should land in this function. Let's say / and /index
# We can also define the legitimate methods for this page of GET and POST
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
# Now comes the actual function definition for processing this page
def index():

    # Url arguments can be added to the url like this ?name=Peter&age=57
    # Get the url arguments if there are any
    url_arguments = request.args.to_dict(flat=False)

    # if there are any url arguments, print them to the console here
    if len(url_arguments) > 0:
        print(f"\nThere were some url arguments and they were:\n{url_arguments}\n")

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

        # Just for this example, stor the form package in the session 
        # so that when we come back, we still have access to it 
        session["form_package"] = form_package

        # because we have modified the contents of the session, we must 
        # tell the session that it has changed. To me, this seems like
        # a failing but it is required to make the app function as we expect 
        session.modified = True

        # now that we have processed everything we needed to in the post,
        # we do a relocate to the same page with a get
        # This stops the annoying behaviour where it keeps asking if
        # we want to resubmit the form
        return redirect(url_for("index"))

    html = """
        <!DOCTYPE html>
        <html lang="en">

        <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>First Page</title>
        </head>

        <body>
            <div class="container">
                <h1>Our first page</h1>
                <ul>
                <li>
                    <a href="/">Visit this page with no URL arguments</a>
                </li>
                <li>
                    <a href="/?name=Peter&age=57">Visit this page with some URL arguments</a>
                </li>
                <li>
                    <a href="/second_page">Visit our second page....</a>
                </li>

                </ul>
                <form action="" method="post">
                    <label for="first_name">First name:</label><br>
                    <input type="text" id="first_name" name="first_name" value="Peter"><br>
                    <input type="submit" value="Submit">
                </form>  

                {% if url_arguments %}
                    <h2>Url Arguments</h2>
                {% endif %}
                <ul>
                {% for key, value  in url_arguments.items() %} 
                    <li>{{ key }}: {{ value }}</li>
                {% endfor %}
                </ul>

                {% if session %}
                    <h2>Session Variables</h2>
                {% endif %}
                <ul>
                {% for key, value  in session.items() %} 
                    <li>{{ key }}: {{ value }}</li>
                {% endfor %}
                </ul>

            </div>
        </body>
        </html> 
    """

    # Use Jinja to render the HTML and resolve any variables that we pass in
    rendered_html = render_template_string(html, url_arguments=url_arguments)
    return rendered_html

# Now the definition of our second_page
@app.route("/second_page", methods=["GET"])
def second_page():
    # On this page, we don't have any of the sophistication of the first page
    # We simply return a string with a link back to the first page 
    return "<a href=/index?name=Peter&age=57>Visit our home page....</a>"

if __name__ == "__main__":

    # host="0.0.0.0" allows the application to be visisted from 
    # another device on the same network 
    # debug=True allows automatic restart if the file changes 
    app.run(debug=True, host="0.0.0.0")


