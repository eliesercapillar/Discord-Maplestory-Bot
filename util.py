import numpy as np
import cv2


def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsv[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lower_limit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upper_limit = np.array([180, 255, 255], dtype=np.uint8)
        print("Hue was over 165")
    elif hue <= 15:  # Lower limit for divided red hue
        lower_limit = np.array([0, 100, 100], dtype=np.uint8)
        upper_limit = np.array([hue + 10, 255, 255], dtype=np.uint8)
        print("Hue less than 15")
    else:
        lower_limit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upper_limit = np.array([hue + 10, 255, 255], dtype=np.uint8)
        print("Hue was between 15 and 165")

    return lower_limit, upper_limit


