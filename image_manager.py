import cv2
import os
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADED_PATH = os.path.join(basedir, 'uploads'),

def load_images_from_folder():
    images=[]
    for filename in os.listdir(os.path.join(basedir, 'uploads')):
        
        images.append(filename)
    return images

def get_path_to_image():
    uploaded_images = load_images_from_folder()
    

    uploaded_image = uploaded_images[0]
    image_path = f"uploads/{uploaded_image}"
    return image_path

class Image_manager:
    """
    this class manages images and transforms them
    """
    def __init__(self, path_to_image) :
        self.name = "modifier"
        self.path_to_image = path_to_image
        self.images = {}
        self.read_image()
    def read_image(self):
        self.image = cv2.imread(self.path_to_image)
        self.images["standard"] = self.image
    def blur_image(self):
        blurred_image = cv2.GaussianBlur(self.image, (9,9), cv2.BORDER_DEFAULT)
        return blurred_image
    def edge_detect(self):
        image_with_edges = cv2.Canny(self.image, 125, 175)
        return image_with_edges
    def greyscale(self):
        grey_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return grey_image
    def black_and_white(self):
        grey_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        (thresh, black_and_white_image) = cv2.threshold(grey_image, 120, 255, cv2.THRESH_BINARY)
        return black_and_white_image
    def get_image(self, image_name):
        if image_name == "standard":
            return self.image
        if image_name == "blurred":
            return self.blur_image()
        if image_name == "edged":
            return self.edge_detect()
        if image_name == "greyscale":
            return self.greyscale()
        if image_name == "black_and_white":
            return self.black_and_white()



if __name__ == "__main__":
    path_to_image = os.path.join(".", "static", "images", "trees01.jpeg")
    image_manager = Image_manager(path_to_image)
    print(image_manager.name, path_to_image)

    print(image_manager.image.shape)