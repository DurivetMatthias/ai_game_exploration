import numpy as np
from commons.opencv_commons import *
from commons.pathlib_commons import *


def find_target_in_source(*, target, source, class_name, threshold=0.48):
    matching_result = cv2.matchTemplate(source, target, cv2.TM_CCOEFF_NORMED)
    y_locations, x_locations = np.where(matching_result >= threshold)

    width, height = get_width_and_height(target)

    rectangles = [
        [int(x), int(y), int(width), int(height)]
        for (x, y) in zip(x_locations, y_locations)
    ]

    #rectangles = rectangles * 2
    #rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    return [(rectangle, class_name) for rectangle in rectangles]


def display_template_matching(*, rectangles, source):
    for rectangle, class_name in rectangles:
        draw_rectangle(loaded_image=source, rectangle=rectangle)
        draw_text_for_rectangle(
            text=class_name, rectangle=rectangle, loaded_image=source)

    show_image(source)


def multiple_class_template_matching(*, class_names, class_images, source, matching_function=find_target_in_source):
    multi_class_rectangles = []
    for class_name, class_image in zip(class_names, class_images):
        rectangles = matching_function(
            target=class_image, source=source, class_name=class_name)
        multi_class_rectangles.extend(rectangles)
    return multi_class_rectangles


def prepare_multiple_class_targets(targets_directory):
    class_image_paths = get_all_files(targets_directory)
    class_names = [get_filename(image_path)
                   for image_path in class_image_paths]
    class_images = [read_image(str(image_path))
                    for image_path in class_image_paths]

    return class_images, class_names


def prepare_multiple_class_sourcess(sources_directory):
    source_image_paths = get_all_files(sources_directory)
    return [read_image(str(image_path))
            for image_path in source_image_paths]
