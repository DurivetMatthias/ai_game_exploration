import enum
import numpy as np
from statistics import mean
from commons.opencv_commons import *
from commons.pyautogui_commons import *
from commons.pathlib_commons import *
from commons.data_commons import *
from ai.template_matching import *
from ai.image_hashing import *
from config import SLEEP_TIME


def get_pedastal_positions():
    pedastal_spacing = 144
    first_pedastal_x = 522
    first_pedastal_y = 698

    pedastal_positions = [
        (first_pedastal_x + i*pedastal_spacing, first_pedastal_y) for i in range(7)
    ]

    return pedastal_positions


def get_active_positions():
    pedastal_spacing = 144
    first_pedastal_x = 530
    first_pedastal_y = 400

    pedastal_positions = [
        (first_pedastal_x + i*pedastal_spacing, first_pedastal_y) for i in range(5)
    ]

    return pedastal_positions


def get_pedastal_images(*, game_image, crop_width=9, crop_height=9, x_offset=0, y_offset=0):
    pedastal_positions = get_pedastal_positions()

    pedastal_rectangles = [
        [x + x_offset - crop_width//2, y + y_offset - crop_height//2, crop_width, crop_height] for x, y in pedastal_positions
    ]

    pedastal_images = [
        get_cropped_image(loaded_image=game_image, rectangle=rectangle)
        for rectangle in pedastal_rectangles
    ]

    return pedastal_images


def get_small_pedastal_images(game_image):
    return get_pedastal_images(game_image=game_image, crop_width=9, crop_height=9)


def get_large_pedastal_images(game_image):
    return get_pedastal_images(game_image=game_image, crop_width=101, crop_height=101)


def get_tier_images(game_image):
    return get_pedastal_images(game_image=game_image, crop_width=32, crop_height=32, x_offset=-37, y_offset=-93)


def get_animals():
    return [
        ["ant", "beaver", "cricket", "duck", "fish",
            "horse", "mosquito", "otter", "pig", ],
        ["crab", "dodo", "dog", "elephant", "flamingo", "hedgehog",
            "peacock", "rat", "shrimp", "spider", "swan", ],
        ["badger", "blowfish", "camel", "giraffe", "kangaroo", "ox",
            "rabbit", "sheep", "snail", "turtle", "whale", ],
        ["bison", "deer", "dolphin", "hippo", "monkey",
            "penguin", "rooster", "skunk", "squirel", "worm"],
        ["cow", "crocodile", "parrot", "rhino",
            "scorpion", "seal", "shark", "turkey", ],
        ["cat", "dragon", "fly", "gorilla",
            "leopard", "mammoth", "snake", "tiger"],
    ]


def get_foods():
    return [
        ["apple", "honey"],
        ["cupcake", "meat bone", "sleeping pill"],
        ["garlic", "salad bowl"],
        ["canned food", "pear"],
        ["chili", "chocolate", "sushi"],
        ["melon", "mushroom", "pizza", "steak"],
    ]


def wait_for_button(button_image_path):
    positive_checks = 0
    threshold = 2
    while True:
        sleep(SLEEP_TIME)
        found_position = locate_image(button_image_path)
        if not found_position:
            positive_checks = 0
            sleep(SLEEP_TIME)
            continue

        positive_checks += 1
        if positive_checks >= threshold:
            return found_position
            break


def continue_after_loss():
    x, y = wait_for_button("images/buttons/defeat_button.png")
    click(x, y)


def choose_name():
    wait_for_button("images/buttons/pick_names.png")
    click(400, 400)
    click(400, 700)
    x, y = wait_for_button("images/buttons/confirm.png")
    click(x, y)


def unique_file_name(*, slot=0, money=0, turn=0, suffix=''):
    return "z_slot_" + str(slot+1) + "_money_" + str(money) + "_turn_" + str(turn) + suffix + ".png"


def list_missing_shop_data():
    collected_data = get_all_files('images/data/animals')
    collected_animals = [get_filename(relative_path)
                         for relative_path in collected_data]

    all_animals = get_animals()

    for tier_number, tier in enumerate(all_animals):
        print()
        print(f'tier {tier_number+1}:\n------------------')
        for animal in tier:
            if animal not in collected_animals:
                print(animal, end=', ')


def parse_batch_data():
    shop_image_paths = get_all_files('images/data/shops/todo')
    shop_images = [read_image(shop_image_path)
                   for shop_image_path in shop_image_paths]
    for turn, shop_image in enumerate(shop_images):
        small_pedastal_images = get_small_pedastal_images(shop_image)
        for slot, small_pedastal_image in enumerate(small_pedastal_images):
            write_image(loaded_image=small_pedastal_image,
                        relative_path="images/data/animals/" + unique_file_name(slot=slot, turn=turn))

        large_pedastal_images = get_large_pedastal_images(shop_image)
        for slot, large_pedastal_image in enumerate(large_pedastal_images):
            write_image(loaded_image=large_pedastal_image,
                        relative_path="images/data/animals/" + unique_file_name(slot=slot, turn=turn, suffix='_large'))

        tier_images = get_tier_images(shop_image)
        for slot, tier_image in enumerate(tier_images):
            write_image(loaded_image=tier_image,
                        relative_path="images/data/tiers/" + unique_file_name(slot=slot, turn=turn))


def classify_game_state():
    shop_image_paths = get_all_files('images/data/shops/done')
    shop_images = [read_image(shop_image_path)
                   for shop_image_path in shop_image_paths]

    hash_to_name = {
        md5_hash_image(file_path=file_path): get_filename(file_path) for file_path in get_all_files('images/data/animals')
    }

    for shop_image in shop_images:
        small_pedastal_images = get_small_pedastal_images(shop_image)
        image_classes = []
        for slot, small_pedastal_image in enumerate(small_pedastal_images):
            file_path = 'images/screen_capture/temp.png'
            write_image(loaded_image=small_pedastal_image,
                        relative_path=file_path)
            image_hash = md5_hash_image(file_path=file_path)
            image_class = hash_to_name.get(image_hash, None)
            image_classes.append(image_class)

        for (x, y), image_class in zip(get_pedastal_positions(), image_classes):
            rectangle = [x-50, y-50, 100, 100]
            draw_rectangle(loaded_image=shop_image,
                           rectangle=rectangle)
            draw_text_for_rectangle(
                loaded_image=shop_image, text=image_class, rectangle=rectangle)

        show_image(resize_image(target_width=1280,
                   target_height=720, loaded_image=shop_image))


class Actions(enum.Enum):
    buy = 'buy'
    sell = 'sell'
    freeze = 'freeze'
    move = 'move'
    combine = 'combine'
    roll = 'roll'


class Game:
    def __init__(self):
        self.turn = 1
        self.tier = 1
        self.gold = 10
        self.hash_to_animal = {
            md5_hash_image(file_path=file_path): get_filename(file_path) for file_path in get_all_files('images/data/animals')
        }
        self.active_animals = [],
        self.shop_animals = [],

    def play_multiple_games(*, self, amount):
        for _ in range(amount):
            self.play_game()

    def play_game(self):
        while True:
            self.wait_for_turn_start()
            self.play_turn()
            self.wait_for_turn_end()
            self.increment_turn_and_tier()

    def wait_for_turn_start(self):
        while True:
            if not locate_image("images/buttons/end_turn_button.png"):
                sleep(SLEEP_TIME)
                continue
            break

    def wait_for_turn_end(self):
        while True:
            if locate_image("images/buttons/end_turn_button.png"):
                sleep(SLEEP_TIME)
                continue

            break

    def play_turn(self):
        while self.gold > 0:
            self.read_game_state()
            actions = self.plan_actions()
            for action in actions:
                self.take_action(action)
        self.end_turn()

    def increment_turn_and_tier(self):
        turn_to_tier_mapping = {
            1: 1,
            2: 1,
            3: 2,
            4: 2,
            5: 3,
            6: 3,
            7: 4,
            8: 4,
            9: 5,
            10: 5,
        }
        self.turn += 1
        self.tier = turn_to_tier_mapping.get(new_turn, 6)

    def read_game_state(self):
        # game_image = read_image(capture_screen())
        game_image = read_image('images/data/shops/done/Screenshot (50).png')
        small_pedastal_images = get_small_pedastal_images(game_image)
        self.shop_animals = []

        for small_pedastal_image in small_pedastal_images:
            file_path = 'images/screen_capture/temp.png'
            write_image(loaded_image=small_pedastal_image,
                        relative_path=file_path)
            image_hash = md5_hash_image(file_path=file_path)
            image_class = self.hash_to_animal.get(image_hash, 'empty')
            self.shop_animals.append(image_class)

    def reroll_shop(self):
        click_button("images/buttons/roll_button.png")
        self.gold -= 1

    def end_turn(self):
        click_button("images/buttons/end_turn_button.png")

    def plan_actions(self):
        if self.turn == 1:
            return [
                (Actions.buy, 0, 0),
                (Actions.buy, 1, 1),
                (Actions.buy, 2, 2),
                (Actions.roll, None, None)
            ]
        if turn == 2:
            return [
                (Actions.buy, 0, 0),
                (Actions.buy, 1, 1),
                (Actions.buy, 2, 2),
                (Actions.roll, None, None)
            ]
        else:
            return [
                (Actions.buy, 0, 0),
                (Actions.buy, 1, 1),
                (Actions.buy, 2, 2),
                (Actions.roll, None, None)
            ]

    def take_action(self, actionTuple):
        action, index, index2 = actionTuple
        if action == Actions.roll:
            self.reroll_shop()
        if action == Actions.buy:
            move_mouse(*get_pedastal_positions()[index])
            drag_and_release(*get_active_positions()[index2])
            self.gold -= 3
        else:
            print(actionTuple)
