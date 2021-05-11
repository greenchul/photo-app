from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    rendered_html = render_template("index.html")
    return rendered_html

@app.route("/login")
def login():
    rendered_html = render_template("login.html")
    return rendered_html


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")





