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
    for unique_hash in sorted(lookup_table, key=lambda x: -len(lookup_table[x])):
        print()
        print(unique_hash)
        for file_path in lookup_table[unique_hash][:5]:
            print(get_filename(file_path), len(lookup_table[unique_hash]))
        preview_multiple(lookup_table[unique_hash][:5])


def delete_duplicates(image_dir):
    lookup_table = find_exact_match(image_dir)
    for unique_hash in lookup_table:
        for file_path in lookup_table[unique_hash][1:]:
            delete_file(file_path)


def delete_low_occurences(*, image_dir, threshold):
    lookup_table = find_exact_match(image_dir)
    for unique_hash in lookup_table:
        if len(lookup_table[unique_hash]) < threshold:
            for file_path in lookup_table[unique_hash]:
                delete_file(file_path)
