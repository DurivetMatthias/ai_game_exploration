from scipy import spatial
import numpy as np
import itertools
from hashlib import md5
from commons.pathlib_commons import *
from commons.opencv_commons import *


def md5_hash_image(*, file_path):
    with open(file_path, "rb") as binary_image_file:
        return md5(binary_image_file.read()).hexdigest()


def find_exact_match(image_dir):
    image_file_paths = get_all_files(image_dir)
    lookup_table = {}
    for file_path in image_file_paths:
        hashed = md5_hash_image(file_path=file_path)
        if hashed in lookup_table:
            lookup_table[hashed].append(file_path)
        else:
            lookup_table[hashed] = [file_path]

    return lookup_table


def show_exact_matches(image_dir):
    lookup_table = find_exact_match(image_dir)
    for unique_hash in lookup_table:
        print()
        print(unique_hash)
        for file_path in lookup_table[unique_hash]:
            print(get_filename(file_path))
        preview_multiple(lookup_table[unique_hash])


def delete_duplicates(image_dir):
    lookup_table = find_exact_match(image_dir)
    for unique_hash in lookup_table:
        for file_path in lookup_table[unique_hash][1:]:
            delete_file(file_path)


def calculate_hamming_distance(image, image2):
    score = spatial.distance.hamming(image, image2)
    return score


def find_similar_images(image_dir, *, threshold=0.10):
    image_file_paths = get_all_files(image_dir)
    difference_scores = {}
    for file_path in image_file_paths:
        loaded_image = read_image(file_path)
        difference_scores[file_path] = difference_score(loaded_image)

    uniques_to_duplicates = {}

    for image_path1, image_path2 in itertools.combinations(image_file_paths, 2):
        hamming_distance = calculate_hamming_distance(
            difference_scores[image_path1], difference_scores[image_path2])
        print(f"{hamming_distance=}")
        if hamming_distance < threshold:
            if image_path1 in uniques_to_duplicates:
                uniques_to_duplicates[image_path1].append(image_path2)
            else:
                uniques_to_duplicates[image_path1] = [image_path2]
        else:
            uniques_to_duplicates[image_path1] = []

    print(f"{len(uniques_to_duplicates)=}")
    for unique_image_path in uniques_to_duplicates:
        if(len(uniques_to_duplicates[unique_image_path])) > 0:
            preview_multiple(
                [unique_image_path, *uniques_to_duplicates[unique_image_path]])


def intensity_diff(row_res, col_res):
    difference_row = np.diff(row_res)
    difference_col = np.diff(col_res)
    difference_row = difference_row > 0
    difference_col = difference_col > 0
    return np.vstack((difference_row, difference_col)).flatten()


def resize(image, width=30, height=30):
    row_res = cv2.resize(image, (height, width),
                         interpolation=cv2.INTER_AREA).flatten()
    col_res = cv2.resize(image, (height, width),
                         interpolation=cv2.INTER_AREA).flatten('F')
    return row_res, col_res


def difference_score(image, width=30, height=30):
    gray = image_to_greyscale(image)
    row_res, col_res = resize(gray, width, height)
    difference = intensity_diff(row_res, col_res)

    return difference
