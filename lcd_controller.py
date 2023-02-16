import math
import time
import uasyncio
from machine import Pin
from pico_i2c_lcd import I2cLcd
from machine import I2C
import os

# Decorator to make sure lcd is not blocked and display is clear
def before_use(func):
    def decorator(*args):
        args[0].lcd.clear()
        args[0].lcd.move_to(0, 0)
        return func(*args)

    return decorator

# Class to control lcd and buttons, clear, print etc. main goal is to make sure code is clean
class LcdController:
    def __init__(self):
        self.button_up = Pin(28, Pin.IN, Pin.PULL_DOWN)
        self.button_next = Pin(27, Pin.IN, Pin.PULL_DOWN)
        self.button_down = Pin(26, Pin.IN, Pin.PULL_DOWN)
        self.button_confirm = Pin(15, Pin.IN, Pin.PULL_DOWN)

        self.i2c = I2C(id=0, scl=Pin(17), sda=Pin(16), freq=100000)
        self.lcd = I2cLcd(self.i2c, 0x27, 2, 16)

    async def handle_button(self, handle_up_function, handle_down_function, handle_next_function, callback):
        while (1):
            if (self.button_up.value()):
                handle_up_function()
                time.sleep(1)
            if (self.button_down.value()):
                handle_down_function()
                time.sleep(1)
            if (self.button_next.value()):
                handle_next_function()
                time.sleep(1)
            if (self.button_confirm.value()):
                return callback()

    @before_use
    def print_on_lcd(self,msg, delay = 3):
        self.lcd.putstr(msg)
        time.sleep(delay)

    @before_use
    def print_multiple(self, list_of_msg, delay = 3):
        for msg in list_of_msg:
            self.lcd.clear()
            self.lcd.move_to(0, 0)
            self.lcd.putstr(msg)
            time.sleep(delay)

    @before_use
    async def get_input(self):
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
            self.lcd.move_to(len(value) % 16, 1 if math.floor(len(value) / 16) % 2 != 0 else 0)

        def handle_confirm():
            nonlocal value
            value += char_list[current_char]
            self.lcd.clear()
            self.lcd.hide_cursor()
            return value

        def print_current_input():
            # move cursor back by one column to overwrite last char
            last_position = [self.lcd.cursor_x, self.lcd.cursor_y]
            self.lcd.putchar(char_list[current_char])
            self.lcd.move_to(last_position[0], last_position[1])

        self.lcd.show_cursor()

        print_current_input()

        return uasyncio.run(self.handle_button(change_char_up, change_char_down, handle_next, handle_confirm))

    @before_use
    async def get_select(self, options):
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
            self.lcd.clear()
            return options[current_option]

        def print_current_input():
            self.lcd.putstr(options[current_option])

        print_current_input()

        return uasyncio.run(self.handle_button(change_char_up, change_char_down, lambda *args: None, handle_confirm))
