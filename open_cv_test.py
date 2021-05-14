import cv2
import os
import numpy as np


# create blank image
blank=np.zeros((500,500, 3), dtype="uint8")
# change colour of blank image to grn
blank[:] = 0,255,0
# change colour to blue
blank[:] = 255,0,0
# change colour to red
blank[:] = 0,0,255


# read images

plant_image= cv2.imread("images/plants01.jpeg")
cat_image = cv2.imread("images/cat01.png")
blackpool_image = cv2.imread("images/blackpool01.jpeg")


####### functions ##########

# change colour

def resize_500(image):
    resized_image = cv2.resize(image, (500,500))
    return resized_image

def change_colour(image, colour):
    image[:] = colour
    return image


def draw_rectangle(image, start, end, colour, thickness):
    image_with_rectangle =cv2.rectangle(image, start, end, colour, thickness)
    return image_with_rectangle

def draw_circle(image, center_coords, radius, colour, thickness):
    image_with_circle = cv2.circle(image, center_coords, radius, colour, thickness)
    return image_with_circle

def draw_circle_in_center(image, radius, colour, thickness):
    center = (image.shape[1]//2, image.shape[0]//2)
    image_with_circle = cv2.circle(image, center, radius, colour, thickness)
    return image_with_circle

def draw_line(image, start_point, end_point, colour, thickness):
    image_with_line =cv2.line(image, start_point, end_point, colour, thickness)
    return image_with_line
    
def convert_to_greyscale(image):
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grey_image

def blur_image(image):
    blurred_image = cv2.GaussianBlur(image, (9,9), cv2.BORDER_DEFAULT)
    return blurred_image

def edge_detector(image):
    image_with_edges = cv2.Canny(image, 125, 175)
    return image_with_edges

def make_black_and_white(image):
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, black_and_white_image) = cv2.threshold(grey_image, 120, 255, cv2.THRESH_BINARY)
    return black_and_white_image

if __name__ == "__main__":


    # create blank image
    blank=np.zeros((500,500, 3), dtype="uint8")
    # change colour of blank image to grn
    blank[:] = 0,255,0
    # change colour to blue
    blank[:] = 255,0,0
    # change colour to red
    blank[:] = 0,0,255


    # read images

    plant_image= cv2.imread("images/plants01.jpeg")
    cat_image = cv2.imread("images/cat01.png")
    blackpool_image = cv2.imread("images/blackpool01.jpeg")

    resize_cat= resize_500(cat_image)

    draw_rectangle(cat_image, (0,0), (200,200), (0,100,230), 2)

    draw_circle(blackpool_image, (30,30), 20, (0,255,255), -1)

    # draw_circle_in_center(cat_image, 20, (0,0,255), 3)

    # draw_line(cat_image, (0,0), (100,100), (0,200,200), 2)

    cat_image = draw_line(cat_image, (0,0), (100,100), (0,0,155), 4)

    greyscale_image = convert_to_greyscale(cat_image)

    # blurred_image = blur_image(cat_image)

    edged_image = edge_detector(cat_image)
    print(edged_image[0])

    cropped_image = edged_image[50:100, 200:300]

    black_and_white = make_black_and_white(blackpool_image)

    # write images to new folder

    cv2.imwrite(os.path.join("output_no_git", "image.png"), blank)
    cv2.imwrite(os.path.join("output_no_git", "cat.png"), cat_image)
    cv2.imwrite(os.path.join("output_no_git", "plant.png"), plant_image)
    cv2.imwrite(os.path.join("output_no_git", "blackpool.png"), blackpool_image )
    # cv2.imwrite(os.path.join("output_no_git", "grey_test.png"), greyscale_image )
    # cv2.imwrite(os.path.join("output_no_git", "blur.png"), blurred_image)
    cv2.imwrite(os.path.join("output_no_git", "cat_edges.png"), edged_image)
    cv2.imwrite(os.path.join("output_no_git", "cat_resize.png"), resize_cat)
    cv2.imwrite(os.path.join("output_no_git", "crop.png"), cropped_image)
    cv2.imwrite(os.path.join("output_no_git", "black_and_white.png"), black_and_white)


    # cv2.waitKey(0)