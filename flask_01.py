from flask import Flask, request, render_template, make_response
import json
from flask_dropzone import Dropzone
import cv2
import os
from image_manager import Image_manager
from image_manager import get_path_to_image
# path_to_image = os.path.join("static", "images", "trees01.jpeg")

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config.update(
    UPLOADED_PATH = os.path.join(basedir, 'uploads'),
    DROPZONE_ALLOWED_FILE_TYPE = "image",
    DROPZONE_MAX_FILES = "1" 

)
 
dropzone = Dropzone(app)
@app.route("/upload", methods=['POST', 'GET'])    
def upload(): 
    if request.method == "POST":
        file = request.files.get('file')
        file.save(os.path.join(app.config['UPLOADED_PATH'], file.filename))
    rendered_html = render_template("upload.html")
    return rendered_html

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

   
    url_arguments = request.args.to_dict(flat=False)
    image_name = url_arguments["image_name"][0]

    path_to_image = get_path_to_image()
    image_manager = Image_manager(path_to_image)  

 
    image = image_manager.get_image(image_name)

    retval, buffer = cv2.imencode(".png", image)
    response = make_response(buffer.tobytes())
    response.headers["Content-Type"] = "image/png"

    return response   



@app.route("/puzzle")
def puzzle():
    path_to_image = get_path_to_image()
    cat_image = cv2.imread(path_to_image)
    cat_image = cv2.resize(cat_image, (500,500))
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
            path_to_image = os.path.join("static", "images", "puzzle", file_name)
            paths_to_image.append(path_to_image)
            cv2.imwrite(path_to_image, tile)   

    paths_to_image_as_json = json.dumps(paths_to_image)
    rendered_html = render_template("puzzle.html", paths_to_image = paths_to_image, number_of_rows = number_of_rows, number_of_cols = number_of_cols, paths_to_image_as_json = paths_to_image_as_json)
    return rendered_html

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")        
    




