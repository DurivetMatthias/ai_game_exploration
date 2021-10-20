from time import sleep
import pyautogui
from config import SLEEP_TIME


def display_ready_button():
    pyautogui.alert('The program is ready to start')
    sleep(SLEEP_TIME)


def display_end_message():
    pyautogui.alert('The program has finished')


def capture_screen():
    file_path = 'images/screen_capture/current_screen.png'
    pyautogui.screenshot(file_path)
    return file_path


def locate_image(image_path):
    return pyautogui.locateCenterOnScreen(image_path)


def click_button(image_path):
    x, y = locate_image(image_path)
    click(x, y)


def click(x, y):
    pyautogui.click(x, y)
    sleep(SLEEP_TIME)
