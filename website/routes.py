from flask import Flask, request, render_template, make_response, session
from flask_session import Session
import secrets
import json
from flask_dropzone import Dropzone
import cv2
import os
from website import Image_manager

# path_to_image = os.path.join("static", "images", "trees01.jpeg")

basedir = os.path.abspath(os.path.dirname(__file__))


from flask import current_app as app

session_life_in_seconds = 3600
app.config.update(SECRET_KEY="We just need a secret here: I like yellow.")
app.config.update(SESSION_TYPE="filesystem")
app.config.update(PERMANENT_SESSION_LIFETIME=session_life_in_seconds)
app.config.update(SESSION_FILE_DIR=os.path.join("output_no_git","way_2"))

# Hmmmm How to describe this?
Session(app)


app.config.update(
    UPLOADED_PATH = os.path.join(basedir, 'uploads', "output_no_git"),
    DROPZONE_ALLOWED_FILE_TYPE = "image",
    DROPZONE_MAX_FILES = "1" 

)
 
dropzone = Dropzone(app)
@app.route("/upload", methods=['POST', 'GET'])    
def upload(): 
    if request.method == "POST":
        file = request.files.get('file')
        file_name = f"uploaded_{secrets.token_urlsafe(10)}_{file.filename}"
        file.save(os.path.join(app.config['UPLOADED_PATH'], file_name))
        session["uploaded_file"] = file_name
        print(session)
    rendered_html = render_template("upload.html")
    return rendered_html

@app.route("/")
def index():
    url_arguments = request.args.to_dict(flat=False)
    if "name" in url_arguments:
        session["name"] = url_arguments["name"][0]

    rendered_html = render_template("index.html")
    return rendered_html



@app.route("/edit")
def edit():
    # Url arguments can be added to the url like this ?name=Peter&age=57
    # Get the url arguments if there are any
    url_arguments = request.args.to_dict(flat=False)
    image_modification = "standard"
    # if there are any url arguments, print them to the console here
    if len(url_arguments) > 0:
        print(f"\nThere were some url arguments and they were:\n{url_arguments}\n")
        if url_arguments["modification"][0] == "1":
            print("Mod 1")
            image_modification = "blurred"  
            
            
        if url_arguments["modification"][0] == "2":
            image_modification = "edged"
        if url_arguments["modification"][0] == "3":
            image_modification = "greyscale"
        if url_arguments["modification"][0] == "4":
            image_modification = "black_and_white"
        
            
    else:
        image_modification = "standard"  

    rendered_html = render_template("edit.html", user="Rachel", image_modification = image_modification)
    return rendered_html

@app.route("/get_image")
def get_image():

   
    url_arguments = request.args.to_dict(flat=False)
    image_modification = url_arguments["image_modification"][0]
    image_name = session["uploaded_file"]
    print(image_name)
    path_to_image = os.path.join(basedir, "uploads", "output_no_git", image_name)
    print(path_to_image)
    print(image_modification)

    
    image_manager = Image_manager(path_to_image)  

 
    image = image_manager.get_image(image_modification)

    retval, buffer = cv2.imencode(".png", image)
    response = make_response(buffer.tobytes())
    response.headers["Content-Type"] = "image/png" 

    return response   



@app.route("/puzzle")
def puzzle():
    image_name = session["uploaded_file"]
    path_to_image = os.path.join(basedir, "uploads", "output_no_git", image_name)
    print(f"puzzle image is {image_name}")
    cat_image = cv2.imread(path_to_image)
    # cat_image = cv2.resize(cat_image, (500))
    new_height = 400
    scale = new_height/cat_image.shape[0] 
    print(scale)
    new_width = int(cat_image.shape[1] * scale)
    print(new_width)
    cat_image = cv2.resize(cat_image, (new_width, new_height))

    print(cat_image.shape) 

    number_of_rows = 4
    number_of_cols = 5

    if cat_image.shape[1] % number_of_cols:
        # the image is not an exact multiple wide
        desired_width = round(cat_image.shape[1]/number_of_cols) * number_of_cols
        desired_height = round(cat_image.shape[0]/number_of_rows) * number_of_rows
        image = cv2.resize(cat_image, (desired_width, desired_height))
        

        
    else:
        image = cat_image  

    tile_width = int(image.shape[1] / number_of_cols)
    tile_height = int(image.shape[0] / number_of_rows)  

    
    paths_to_image = []  

    for row_index in range(number_of_rows):
        tile_row_index = tile_height * row_index
        for col_index in range(number_of_cols):
            tile_col_index = tile_width * col_index
            tile = image[tile_row_index: tile_row_index + tile_height, tile_col_index: tile_col_index + tile_width]
            file_name = f"row_{row_index}_col_{col_index}.png"
            path_to_image = os.path.join("static", "images", "puzzle", "output_no_git", file_name)
            paths_to_image.append( path_to_image)
            cv2.imwrite(os.path.join(basedir, path_to_image), tile)  

    paths_to_image_as_json = json.dumps(paths_to_image)
    rendered_html = render_template("puzzle.html", paths_to_image = paths_to_image, number_of_rows = number_of_rows, number_of_cols = number_of_cols, paths_to_image_as_json = paths_to_image_as_json)
    return rendered_html

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")        
    




