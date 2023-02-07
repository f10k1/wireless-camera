from pico_i2c_lcd import I2cLcd
from machine import I2C
import rp2
from machine import Pin

rp2.country('PL')

buttonUp = Pin(28, Pin.IN, Pin.PULL_DOWN)
buttonOk = Pin(27, Pin.IN, Pin.PULL_DOWN)
buttonDown = Pin(26, Pin.IN, Pin.PULL_DOWN)
buttonConfirm = Pin(15, Pin.IN, Pin.PULL_DOWN)

i2c = I2C(id=0,scl=Pin(17),sda=Pin(16),freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
