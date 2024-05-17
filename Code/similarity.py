import cv2
import numpy as np


def compute_similarity_mouse_tracking_based():
    # Read two images. The size of both images must be the same.
    img1 = cv2.imread('output.png')
    img2 = cv2.imread('referance_image.png')

    # compute bitwise XOR on both images
    xor_img = cv2.bitwise_xor(img1, img2)

    # get the total number of pixels
    img_size = xor_img.size

    # get the number of black pixels
    number_of_black_pix = np.sum(xor_img == 0)
    similarity = ((number_of_black_pix / img_size) * 100)

    return similarity


def compute_usability(percentage):
    # check if it is high percentage give it easy otherwise difficult
    if percentage >= 85:
        return 'easy'
    else:
        return 'difficult'


def compute_task_usability(emotion_based_usability, mouse_based_similarity):
    # convert the emotion usability into percentage
    if emotion_based_usability == 'easy':
        emotion_percentage = 100
    else:
        emotion_percentage = 0

    # make sure the mouse_based_similarity is of type float
    mouse_based_similarity = float(mouse_based_similarity)

    # compute the system task similarities based on both emotion and mouse tracking
    general_similarity = (emotion_percentage * 0.50) + (mouse_based_similarity * 0.50)

    # convert the emotion similarity into system usability
    general_usability = compute_usability(general_similarity)

    return general_usability


