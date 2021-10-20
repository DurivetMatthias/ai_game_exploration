import numpy as np
from statistics import mean
from commons.opencv_commons import *
from commons.pyautogui_commons import *
from commons.pathlib_commons import *
from commons.data_commons import *
from ai.template_matching import *
from config import SLEEP_TIME


def get_screen_image():
    screen_path = capture_screen()
    return read_image(screen_path)


def get_animal_images(game_image):
    shop_animal_rectangles = [
        [526, 698, 9, 9],
        [670, 698, 9, 9],
        [814, 698, 9, 9],
    ]

    shop_animal_images = [
        get_cropped_image(loaded_image=game_image, rectangle=rectangle)
        for rectangle in shop_animal_rectangles
    ]

    return shop_animal_images


def get_full_animal_images(game_image):
    shop_animal_rectangles = [
        [456, 574, 143, 180],
        [600, 574, 143, 180],
        [744, 574, 143, 180],
    ]

    shop_animal_images = [
        get_cropped_image(loaded_image=game_image, rectangle=rectangle)
        for rectangle in shop_animal_rectangles
    ]

    return shop_animal_images


def get_tier_images(game_image):
    shop_animal_tiers = [
        [460, 581, 48, 48],
        [604, 581, 48, 48],
        [748, 581, 48, 48],
    ]

    shop_tier_images = [
        get_cropped_image(loaded_image=game_image, rectangle=rectangle)
        for rectangle in shop_animal_tiers
    ]

    return shop_tier_images


def check_if_endturn_button_exists():
    image_path = "images/buttons/end_turn_button.png"
    position = locate_image(image_path)
    if not position:
        return False
    else:
        return True


def wait_for_turn_start():
    positive_checks = 0
    threshold = 2
    while True:
        if not check_if_endturn_button_exists():
            positive_checks = 0
            sleep(SLEEP_TIME)
            continue

        if positive_checks >= threshold:
            break

        positive_checks += 1
        sleep(SLEEP_TIME)


def wait_for_turn_end():
    positive_checks = 0
    threshold = 2
    while True:
        if check_if_endturn_button_exists():
            positive_checks = 0
            sleep(SLEEP_TIME)
            continue

        if positive_checks >= threshold:
            break

        positive_checks += 1
        sleep(SLEEP_TIME)


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


def reroll_shop():
    click_button("images/buttons/roll_button.png")


def end_turn():
    click_button("images/buttons/end_turn_button.png")


def continue_after_loss():
    x, y = wait_for_button("images/buttons/defeat_button.png")
    click(x, y)


def choose_name():
    wait_for_button("images/buttons/pick_names.png")
    click(400, 400)
    click(400, 700)
    x, y = wait_for_button("images/buttons/confirm.png")
    click(x, y)


def update_turn_and_tier(turn):
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
        11: 6,
        12: 6,
    }
    new_turn = turn + 1
    new_tier = turn_to_tier_mapping.get(new_turn, 6)
    return new_turn, new_tier


def unique_file_name(*, slot, money, suffix=''):
    return "slot_" + str(slot+1) + "_" + "money_" + str(money) + suffix + ".png"


def collect_shop_data():
    display_ready_button()

    turn = 1
    tier = 1

    while turn == 1:
        wait_for_turn_start()
        print(f"{turn=}")
        print(f"{tier=}")

        for money in reversed(range(10)):
            reroll_shop()
            screen_image = get_screen_image()

            animal_images = get_animal_images(screen_image)
            for slot, animal_image in enumerate(animal_images):
                write_image(loaded_image=animal_image,
                            relative_path="images/data/animals/" + unique_file_name(slot=slot, money=money))

            full_animal_images = get_full_animal_images(screen_image)
            for slot, full_animal_image in enumerate(full_animal_images):
                write_image(loaded_image=full_animal_image,
                            relative_path="images/data/animals/" + unique_file_name(slot=slot, money=money, suffix='_full'))

            tier_images = get_tier_images(screen_image)
            for slot, tier_image in enumerate(tier_images):
                write_image(loaded_image=tier_image,
                            relative_path="images/data/tiers/" + unique_file_name(slot=slot, money=money))

        end_turn()
        if turn == 1:
            choose_name()

        turn, tier = update_turn_and_tier(turn)
        wait_for_turn_end()
        continue_after_loss()

    display_end_message()
