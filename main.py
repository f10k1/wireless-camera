import rp2
import uasyncio
import time
import json
from lcd_controller import  LcdController
from wifi_api import Wifi

rp2.country('PL')

wifi = Wifi()
lcd = LcdController()
async def main():
    try:
        raise Exception('')
        file = open('config.txt', 'r')
        configuration = json.loads(file.read())
        file.close()
        if ('password' in configuration):
            pass
            #TODO LCD output
            #TODO password check
            #TODO internet connection
        else:
            raise Exception("No configuration")
    except:

        lcd.print_on_lcd("Config not detected")

        lcd.print_on_lcd("Enter new password")

        config = {}

        #TODO Secure password by hashing it
        config['password'] = await lcd.get_input()

        lcd.print_on_lcd("Pick your wifi")

        while(not wifi.is_connected()):
            ssid = await lcd.get_select(wifi.get_ssid_list())

            lcd.print_on_lcd("Enter password")

            password = await lcd.get_input()

            await wifi.connect(ssid, password)

        config['ssid'] = ssid
        config['wifi-password'] = password

        file = open('config.txt', 'w+')
        file.write(json.dumps(config))
        file.close()

uasyncio.run(main())