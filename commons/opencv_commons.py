"""This file contains basic functions to use opencv."""

import cv2


def read_image(relative_path):
    return cv2.imread(relative_path)


def write_image(*, loaded_image, relative_path):
    cv2.imwrite(relative_path, loaded_image)


def show_image(loaded_image):
    cv2.imshow("show_image()", loaded_image)
    cv2.waitKey(0)


def preview_image(relative_path):
    window_name = relative_path
    loaded_image = read_image(relative_path)
    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, 1920//2, 1080//2)
    cv2.imshow(window_name, loaded_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def preview_multiple(relative_paths):
    for i, relative_path in enumerate(relative_paths):
        window_name = relative_path
        loaded_image = read_image(relative_path)
        cv2.namedWindow(window_name)
        spacing = 140
        start_pos = 1920//2 - (spacing//2 * len(relative_paths))
        offset = spacing * i
        cv2.moveWindow(window_name, start_pos + offset, 1080//2)
        cv2.imshow(window_name, loaded_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def image_to_greyscale(loaded_image):
    return cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)


def get_width_and_height(loaded_image):
    return loaded_image.shape[1], loaded_image.shape[0]


def resize_image(*, loaded_image, target_width, target_height):
    return cv2.resize(loaded_image, (target_width, target_height))


def draw_rectangle(*, loaded_image, rectangle):
    top_left = (rectangle[0], rectangle[1])
    bottom_right = (rectangle[0]+rectangle[2], rectangle[1]+rectangle[3])
    cv2.rectangle(loaded_image, top_left, bottom_right, (0, 255, 0), 1)


def draw_text_for_rectangle(*, text, loaded_image, rectangle):
    cv2.putText(loaded_image, text,
                (rectangle[0], rectangle[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


def get_cropped_image(*, loaded_image, rectangle):
    y_start = rectangle[1]
    y_end = rectangle[1]+rectangle[3]
    x_start = rectangle[0]
    x_end = rectangle[0]+rectangle[2]
    return loaded_image[y_start:y_end, x_start:x_end].copy()


def flip_image_verticaly(loaded_image):
    return cv2.flip(loaded_image, 0)


def flip_image_horizontaly(loaded_image):
    return cv2.flip(loaded_image, 1)


def flip_image_diagonaly(loaded_image):
    return cv2.flip(loaded_image, -1)
