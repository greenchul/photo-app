import cv2
import os

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
    def get_image(self, image_name):
        if image_name == "standard":
            return self.image
        if image_name == "blurred":
            return self.blur_image()



if __name__ == "__main__":
    path_to_image = os.path.join(".", "static", "images", "cat01.jpeg")
    image_manager = Image_manager(path_to_image)
    print(image_manager.name)
    print(image_manager.image.shape)