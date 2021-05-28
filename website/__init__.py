# This is inspired by the article here:
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
#

import platform
import os
import socket

from website.image_manager import Image_manager 


from flask import Flask




def create_app():
    # Create Flask application.
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    with app.app_context():   
  
        


        # import the routes
        from website import routes

        # all is set up correctly so return the app  
        return app


