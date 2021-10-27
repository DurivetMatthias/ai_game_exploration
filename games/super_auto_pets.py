import enum
import random
import uuid
import numpy as np
from statistics import mean
from commons.opencv_commons import *
from commons.pyautogui_commons import *
from commons.pathlib_commons import *
from commons.data_commons import *
from ai.template_matching import *
from ai.image_hashing import *
from config import SCEENSHOT_DELAY


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


def wait_for_image(image_path):
    print(f"{image_path=}")
    while True:
        found_position = locate_image(image_path)
        if not found_position:
            continue
        else:
            return found_position


def wait_for_button(button_image_path):
    button_position = wait_for_image(button_image_path)
    click(*button_position)


def choose_name():
    wait_for_image("images/buttons/pick_names.png")
    click(400, 400)
    click(400, 700)
    wait_for_button("images/buttons/confirm_name.png")


def start_game():
    wait_for_button("images/buttons/start_game_button.png")


def speed_up():
    speed_up_position = (1330, 150)
    move_mouse(*speed_up_position)
    sleep(5)
    click(*speed_up_position)
    print('Clicked speed up button')


class TurnResults(enum.Enum):
    win = 'win'
    loss = 'loss'
    draw = 'draw'
    game_over = 'game over'
    game_won = 'Chicken diner!!!'


def wait_for_turn_result():
    while True:
        win_position = locate_image("images/buttons/win_button.png")
        if win_position:
            click(*win_position)
            return TurnResults.win

        loss_position = locate_image("images/buttons/loss_button.png")
        if loss_position:
            click(*loss_position)
            return TurnResults.loss

        draw_position = locate_image("images/buttons/draw_button.png")
        if draw_position:
            click(*draw_position)
            return TurnResults.draw

        game_over_position = locate_image(
            "images/buttons/game_over_button.png")
        if game_over_position:
            click(*game_over_position)
            return TurnResults.game_over

        # TODO :) take screenshot
        # game_won_position = locate_image("images/buttons/win_button.png")
        # if game_won_position:
        #     click(*game_won_position)
        #     return TurnResults.game_won


def wait_for_turn_start():
    while True:
        if not locate_image("images/buttons/end_turn_button.png"):
            continue
        sleep(5)
        break


def wait_for_turn_end():
    while True:
        if locate_image("images/buttons/end_turn_button.png"):
            continue
        sleep(5)
        break


def end_turn():
    wait_for_button("images/buttons/end_turn_button.png")


def click_away_tier_upgrade():
    sleep(2)
    click(960, 0)


def click_away_game_over():
    sleep(5)
    click(960, 0)
    # wait_for_button("images/buttons/game_over_button.png")


def click_away_points():
    sleep(5)
    click(960, 0)
    # wait_for_button("images/buttons/gain_points_button.png")


class Game:
    def __init__(self):
        self.hash_to_animal = {
            md5_hash_image(file_path=file_path): get_filename(file_path) for file_path in get_all_files('images/data/animals')
        }
        self.behavior = BaselineBehavior(self)

    def reset_game_state(self):
        self.turn = 1
        self.tier = 1
        self.gold = 10
        self.my_animals = []
        self.shop_animals = []
        self.frozen_memory = []
        self.wins = 0
        self.losses = 0
        self.game_id = uuid.uuid4()

    def play_multiple_games(self, amount):
        for _ in range(amount):
            self.play_game()

    def play_game(self):
        self.reset_game_state()
        start_game()
        while self.losses < 4 and self.wins < 10:
            if self.turn == 1:
                sleep(5)
            if self.turn in [3, 5, 7, 9, 11]:
                click_away_tier_upgrade()
            wait_for_turn_start()
            for frozen_index in reversed(range(len(self.frozen_memory))):
                self.unfreeze(frozen_index)
            self.play_turn()
            wait_for_turn_end()
            if self.turn == 1:
                choose_name()
                sleep(5)
            speed_up()
            turn_result = wait_for_turn_result()
            self.save_turn_result(turn_result)
            self.increment_turn_and_tier()

    def save_turn_result(self, turn_result):

        if turn_result == TurnResults.win:
            self.wins += 1
        if turn_result == TurnResults.loss:
            self.losses += 1
        if turn_result == TurnResults.game_over:
            click_away_game_over()
            click_away_points()
            self.losses += 1
        if turn_result == TurnResults.game_won:
            # TODO :)
            self.wins += 1

        file_path = "data/games/" + str(self.game_id) + ".csv"
        padded_animals = [str(animal)
                          for animal in [*self.my_animals, *(['empty']*5)][:5]]

        if turn_result == TurnResults.win or turn_result == TurnResults.game_won:
            score = 1
        elif turn_result == TurnResults.draw:
            score = 0.5
        elif turn_result == TurnResults.loss or turn_result == TurnResults.game_over:
            score = 0

        comma_separated_line = ','.join([
            str(self.turn),
            *padded_animals,
            str(self.wins),
            str(self.losses),
            str(score),
        ])

        with open(file_path, 'a') as log_file:
            if(self.turn == 1):
                log_file.write(','.join(['turn', 'animal_0', 'animal_1', 'animal_2',
                               'animal_3', 'animal_4', 'wins', 'losses', 'score']))
            log_file.write('\n')
            log_file.write(comma_separated_line)

    def play_turn(self):
        while self.gold > 0:
            self.read_game_state()
            self.behavior.perform_action()
        self.read_game_state()
        self.behavior.actions_before_combat()
        end_turn()

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
        self.tier = turn_to_tier_mapping.get(self.turn, 6)
        self.gold = 10

    def read_game_state(self):
        sleep(SCEENSHOT_DELAY)
        game_image = read_image(capture_screen())

        small_pedastal_images = get_small_pedastal_images(game_image)
        self.shop_animals = []

        for small_pedastal_image in small_pedastal_images:
            file_path = 'images/screen_capture/temp.png'
            write_image(loaded_image=small_pedastal_image,
                        relative_path=file_path)
            image_hash = md5_hash_image(file_path=file_path)
            image_class = self.hash_to_animal.get(image_hash, 'empty')
            self.shop_animals.append(image_class)

    def freeze(self, animal=None, index=None):
        if animal:
            freeze_index = self.shop_animals.index(animal)
            freeze_position = get_pedastal_positions()[freeze_index]
        else:
            freeze_position = get_pedastal_positions()[index]

        freeze_button_position = (1100, 1000)
        shop_zero_position = get_pedastal_positions()[0]

        click(*freeze_position)
        click(*freeze_button_position)
        self.frozen_memory.append(animal)

    def unfreeze(self, unfreeze_index):
        unfreeze_position = get_pedastal_positions()[unfreeze_index]

        unfreeze_button_position = (1100, 1000)

        click(*unfreeze_position)
        click(*unfreeze_button_position)
        self.frozen_memory = [
            *self.frozen_memory[:unfreeze_index],
            *self.frozen_memory[unfreeze_index+1:],
        ]

    def sell(self):
        sell_index = len(self.my_animals) - 1
        sell_position = get_active_positions()[sell_index]

        sell_button_position = (1200, 1000)

        click(*sell_position)
        click(*sell_button_position)
        self.gold += 1
        self.my_animals = [
            *self.my_animals[:sell_index],
            *self.my_animals[sell_index+1:],
        ]

    def buy(self, animal, combine=False):
        buy_index = self.shop_animals.index(animal)
        buy_position = get_pedastal_positions()[buy_index]

        if combine and animal in self.my_animals:
            drop_index = self.my_animals.index(animal)
            drop_position = get_active_positions()[drop_index]
        else:
            drop_index = len(self.my_animals)
            drop_position = get_active_positions()[drop_index]

        click(*buy_position)
        click(*drop_position)
        self.gold -= 3
        if not combine or animal not in self.my_animals:
            self.my_animals = [
                *self.my_animals[:drop_index],
                animal,
                *self.my_animals[drop_index:],
            ]

    def reroll(self):
        wait_for_button("images/buttons/roll_button.png")
        self.gold -= 1


class BaselineBehavior:
    def __init__(self, game):
        self.game = game
        random.seed(1)

    def perform_action(self):

        if all(['empty' in animal for animal in self.game.shop_animals[:3]]):
            print('everything empty: turn',
                  self.game.turn, 'gold', self.game.gold, 'shop', self.game.shop_animals[:3])
            self.game.reroll()
        else:
            if len(self.game.my_animals) < 5:
                buy_index = random.randint(0, 2)
                while 'empty' in self.game.shop_animals[buy_index]:
                    buy_index = random.randint(0, 2)
                self.attempt_to_buy(
                    self.game.shop_animals[buy_index], combine=False, index=buy_index)
            else:
                for index, animal in enumerate(self.game.shop_animals):
                    if animal in self.game.my_animals:
                        self.attempt_to_buy(animal, combine=True, index=index)
                        return None
                self.game.reroll()

    def actions_before_combat(self):
        for index, animal in enumerate(self.game.shop_animals):
            if animal in self.game.my_animals:
                self.game.freeze(index=index)

    def attempt_to_buy(self, animal, combine=False, index=None):

        # if len(self.game.my_animals) < 5:

        if self.game.gold >= 3:
            self.game.buy(animal, combine=combine)

        else:
            self.game.freeze(index=index)

        # elif len(self.game.my_animals) == 5:

        #     if self.game.gold >= 2:
        #         self.game.sell()
        #         self.game.buy(animal)

        #     else:
        #         self.game.freeze(animal)
