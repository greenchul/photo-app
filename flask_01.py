from flask import Flask, request, render_template, make_response

import cv2
import os
from open_cv_test import blur_image
from image_manager import Image_manager
path_to_image = os.path.join("static", "images", "trees01.jpeg")
image_manager = Image_manager(path_to_image)


app = Flask(__name__)

@app.route("/")
def index():
    rendered_html = render_template("index.html")
    return rendered_html

@app.route("/login")
def login():
    rendered_html = render_template("login.html")
    return rendered_html

@app.route("/edit")
def gallery():
    # Url arguments can be added to the url like this ?name=Peter&age=57
    # Get the url arguments if there are any
    url_arguments = request.args.to_dict(flat=False)
    image_name = "standard"
    # if there are any url arguments, print them to the console here
    if len(url_arguments) > 0:
        print(f"\nThere were some url arguments and they were:\n{url_arguments}\n")
        if url_arguments["modification"][0] == "1":
            print("Mod 1")
            image_name = "blurred"  
            
            
        if url_arguments["modification"][0] == "2":
            image_name = "edged"
        if url_arguments["modification"][0] == "3":
            image_name = "greyscale"
        if url_arguments["modification"][0] == "4":
            image_name = "black_and_white"
        
            
    else:
        image_name = "standard"  

    rendered_html = render_template("edit.html", user="Rachel", image_name = image_name)
    return rendered_html

@app.route("/get_image")
def get_image():

    # Url arguments can be added to the url like this ?image_name=Peter&age=57
    # Get the url arguments if there are any
    url_arguments = request.args.to_dict(flat=False)
    image_name = url_arguments["image_name"][0]

    # print(f"Name in get_spark_image = {image_name}")

    image = image_manager.get_image(image_name)

    retval, buffer = cv2.imencode(".png", image)
    response = make_response(buffer.tobytes())
    response.headers["Content-Type"] = "image/png"

    return response   


@app.route("/upload")
def upload_img():
    rendered_html = render_template("upload.html")
    return

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")





