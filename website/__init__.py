# This is inspired by the article here:
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
#

import platform
import os
import socket

from website.image_manager import Image_manager 


from flask import Flask

# create dir structures 
basedir = os.path.abspath(os.path.dirname(__file__))
try:
    path = os.path.join(basedir, "uploads")
    os.mkdir(path)
except:
    pass

try: 
    path = os.path.join(path, "output_no_git")
    os.mkdir(path)
except:
    pass

try:
    path = os.path.join(basedir, "static", "images")
    os.mkdir(path)
except:
    pass

try:
    path = os.path.join(basedir, "static", "images", "puzzle")
    os.mkdir(path)
except:
    pass

try:
    path = os.path.join(basedir, "static", "images", "puzzle", "output_no_git")
    os.mkdir(path)
except:
    pass


def create_app():
    # Create Flask application.
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    with app.app_context():   
  
        


        # import the routes
        from website import routes

        # all is set up correctly so return the app  
        return app


