from machine import Pin
from pico_i2c_lcd import I2cLcd
from machine import I2C

button_up = Pin(28, Pin.IN, Pin.PULL_DOWN)
button_next = Pin(27, Pin.IN, Pin.PULL_DOWN)
button_down = Pin(26, Pin.IN, Pin.PULL_DOWN)
button_confirm = Pin(15, Pin.IN, Pin.PULL_DOWN)

i2c = I2C(id=0,scl=Pin(17),sda=Pin(16),freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)