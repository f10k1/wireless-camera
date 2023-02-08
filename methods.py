import math
import time
import uasyncio
from config import *

async def handle_button(handle_up_function, handle_down_function, handle_next_function, callback):
    while(1):
        if (button_up.value()):
            handle_up_function()
            time.sleep(1)
        if (button_down.value()):
            handle_down_function()
            time.sleep(1)
        if (button_next.value()):
            handle_next_function()
            time.sleep(1)
        if (button_confirm.value()):
            return callback()

def print_on_lcd(msg):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(msg)
    time.sleep(2)
    lcd.clear()

async def get_input():
    char_list = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!" + '"' + "#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    current_char = 0
    value = ""

    def change_char_up():
        nonlocal current_char
        current_char += 1 if len(char_list) > current_char else -1
        print_current_input()
    def change_char_down():
        nonlocal current_char
        current_char = current_char - 1 if current_char > 0 else len(char_list) - 1
        print_current_input()
    def handle_next():
        nonlocal value, current_char
        value += char_list[current_char]
        current_char = 0
        # check whitch column and row cursor should be showed
        lcd.move_to(len(value)%16, 1 if math.floor(len(value)/16)%2 != 0 else 0)
    def handle_confirm():
        nonlocal value
        value += char_list[current_char]
        lcd.clear()
        lcd.hide_cursor()
        return value
    def print_current_input():
        #move cursor back by one column to overwrite last char
        last_position = [lcd.cursor_x, lcd.cursor_y]
        lcd.hal_write_data(ord(char_list[current_char]))
        lcd.move_to(last_position[0], last_position[1])


    lcd.show_cursor()
    print_current_input()

    return uasyncio.run(handle_button(change_char_up, change_char_down, handle_next, handle_confirm))

async def get_select(options):
    current_option = 0

    def change_char_up():
        nonlocal current_option
        current_option += 1 if len(options) > current_option else -1
        print_current_input()
    def change_char_down():
        nonlocal current_option
        current_option = current_option - 1 if current_option > 0 else len(options) - 1
        print_current_input()
    def handle_confirm():
        lcd.clear()
        return options[current_option]
    def print_current_input():
        print_on_lcd(options[current_option])

    print_current_input()

    return uasyncio.run(handle_button(change_char_up, change_char_down, lambda *args: None, handle_confirm))
