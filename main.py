import numpy as np
from statistics import mean
from commons.opencv_commons import *
from commons.pyautogui_commons import *
from commons.pathlib_commons import *
from commons.data_commons import *
from ai.template_matching import *
from ai.image_hashing import *
from games import super_auto_pets


# def test_commons():
#     relative_path = "images/fullscreen.png"
#     loaded_image = read_image(relative_path)
#     width, height = get_width_and_height(loaded_image)
#     gray = image_to_greyscale(loaded_image)
#     resized = resize_image(
#         loaded_image=gray, target_width=800, target_height=600)
#     rectangle = [300, 100, 200, 100]
#     draw_rectangle(loaded_image=loaded_image, rectangle=rectangle)
#     draw_text_for_rectangle(text='text for rectangle',
#                             loaded_image=loaded_image, rectangle=rectangle)


# def test_template_matching():
#     source_path = "images/fullscreen.png"
#     target_path = "images/targets/animal_box.png"
#     source = read_image(source_path)
#     target = read_image(target_path)
#     rectangles = find_target_in_source(
#         target=target, source=source, class_name="ant")

#     targets_directory = "images/targets"
#     class_image_paths = get_all_files(targets_directory)
#     class_names = [get_filename(image_path)
#                    for image_path in class_image_paths]
#     class_images = [read_image(str(image_path))
#                     for image_path in class_image_paths]
#     multiple_class_rectangles = multiple_class_template_matching(
#         source=source, class_names=class_names, class_images=class_images)


# def extract_targets_from_sprites():
#     sprites_path = "images/sprites"
#     sprite_paths = get_all_files(sprites_path)
#     target_shape = [80, 70]
#     target_start_x = 217
#     mean = 129
#     y_measurements = [70, 197, 332, 456]
#     target_rectangles_in_sprites = [
#         [target_start_x, 70, *target_shape],
#         [target_start_x, 70+mean, *target_shape],
#         [target_start_x, 70+mean+mean, *target_shape],
#         [target_start_x, 70+mean+mean+mean, *target_shape],
#     ]

#     diff = [rect2[1]-rect1[1] for rect1,
#             rect2 in zip(target_rectangles_in_sprites[0:3], target_rectangles_in_sprites[1:4])]

#     sprites = [read_image(sprite_path) for sprite_path in sprite_paths]
#     animal_names_in_order = [
#     ["ant", "beaver", "cricket", "duck", "fish",
#         "horse", "mosquito", "otter", "pig", ],
#     ["crab", "dodo", "dog", "elephant", "flamingo", "hedgehog",
#         "peacock", "rat", "shrimp", "spider", "swan", ],
#     ["badger", "blowfish", "camel", "giraffe", "kangaroo", "ox",
#         "rabbit", "sheep", "snail", "turtle", "whale", ],
#     ["bison", "deer", "dolphin", "hippo", "monkey",
#         "penguin", "rooster", "skunk", "squirel", "worm"],
#     ["cow", "crocodile", "parrot", "rhino",
#         "scorpion", "seal", "shark", "turkey", ],
#     ["cat", "dragon", "fly", "fly", "gorilla",
#         "leopard", "mammoth", "snake", "tiger"],
# ]

# food_names_in_order = [
#     ["apple", "honey"],
#     ["cupcake", "meat bone", "sleeping pill"],
#     ["garlic", "salad bowl"],
#     ["canned food", "pear"],
#     ["chili", "chocolate", "sushi"],
#     ["melon", "mushroom", "melon", "mushroom", "pizza", "steak"],
# ]

#     target_names_in_order = [
#         *flatten(animal_names_in_order), *flatten(food_names_in_order)]

#     game_objects = []

#     for sprite in sprites:
#         for rectangle in target_rectangles_in_sprites:
#             cropped_image = get_cropped_image(
#                 loaded_image=sprite, rectangle=rectangle)
#             target_name = target_names_in_order[len(game_objects)]
#             game_objects.append((cropped_image, target_name))
#             flipped_image = flip_image_horizontaly(cropped_image)
#             flipped_image[np.all(
#                 flipped_image == (29, 14, 0), axis=-1)] = (8, 106, 41)
#             transparent_image = flipped_image
#             resized_image = resize_image(
#                 loaded_image=transparent_image, target_width=63, target_height=55)

#             write_image(loaded_image=resized_image,
#                         relative_path="images/targets/" + target_name + ".png")


# def check_all_sources_for_all_targets():
#     class_images, class_names = prepare_multiple_class_targets(
#         "images/targets")

#     source_images = prepare_multiple_class_sourcess("images/sources")

#     active_animals_source_rect = [220, 175, 378, 91]
#     shop_animals_source_rect = [222, 328, 229, 91]

#     for source in source_images:
#         active_source = get_cropped_image(
#             loaded_image=source, rectangle=active_animals_source_rect)
#         shop_source = get_cropped_image(
#             loaded_image=source, rectangle=shop_animals_source_rect)

#         rectangles = multiple_class_template_matching(
#             class_images=class_images, class_names=class_names, source=active_source)
#         display_template_matching(rectangles=rectangles, source=active_source)


# def check_source_for_target(*, source_name, target_name):
#     source_path = "images/sources/" + source_name + ".png"
#     target_path = "images/targets/" + target_name + ".png"
#     source = read_image(source_path)
#     target = read_image(target_path)
#     rectangles = find_target_in_source(
#         target=target, source=source, class_name="ant")
#     display_template_matching(rectangles=rectangles, source=source)


# def collect_live_data():
#     source_path = "images/sources/fullscreen.png"
#     source = read_image(source_path)

#     active_animals_rectangle = [437, 275, 752, 259]
#     active_animals_image = get_cropped_image(
#         loaded_image=source, rectangle=active_animals_rectangle)

#     shop_animals_rectangle = [437, 567, 469, 259]
#     shop_animals_image = get_cropped_image(
#         loaded_image=source, rectangle=shop_animals_rectangle)

#     shop_foods_rectangle = [1153, 567, 327, 259]
#     shop_foods_image = get_cropped_image(
#         loaded_image=source, rectangle=shop_foods_rectangle)

#     active_animal_rectangles = [
#         [456, 282, 143, 248],
#         [600, 282, 143, 248],
#         [744, 282, 143, 248],
#         [888, 282, 143, 248],
#         [1032, 282, 143, 248],
#     ]

#     active_animal_images = [
#         get_cropped_image(loaded_image=source, rectangle=rectangle)
#         for rectangle in active_animal_rectangles
#     ]

#     shop_animal_rectangles = [
#         [456, 570, 143, 248],
#         [600, 570, 143, 248],
#         [744, 570, 143, 248],
#     ]

#     shop_animal_images = [
#         get_cropped_image(loaded_image=source, rectangle=rectangle)
#         for rectangle in shop_animal_rectangles
#     ]

#     animal_names = ["mosquito", "ant", "cricket",
#                     "beaver", "pig", "duck", "horse", "fish"]
#     animal_images = [
#         *active_animal_images, *shop_animal_images]

#     [write_image(loaded_image=animal_image, relative_path="images/targets/"+animal_name+".png")
#      for animal_image, animal_name in zip(animal_images, animal_names)]


# def sanity_check():
#     source = read_image("images/targets/ant.png")
#     target = source
#     rectangles = find_target_in_source(
#         target=target, source=source, class_name="ant")
#     display_template_matching(rectangles=rectangles, source=source)


if __name__ == "__main__":
    # super_auto_pets.parse_batch_data()
    # show_exact_matches('images/data/tiers')
    # show_exact_matches('images/data/animals')
    # delete_low_occurences(image_dir='images/data/animals', threshold=5)
    # delete_low_occurences(image_dir='images/data/tiers', threshold=5)
    # delete_duplicates('images/data/animals')
    # delete_duplicates('images/data/tiers')
    # super_auto_pets.list_missing_shop_data()
    super_auto_pets.classify_game_state()
