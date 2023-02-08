import rp2
from config import *
import uasyncio
from methods import *
import time
import json
from wifi_api import Wifi

rp2.country('PL')

wifi = Wifi()
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
        print_on_lcd("Config not detected")

        print_on_lcd("Enter new password")

        config = {}

        #TODO Secure password by hashing it
        config['password'] = await get_input()

        print_on_lcd("Pick your wifi")

        while(not wifi.is_connected()):
            ssid = await get_select(wifi.get_ssid_list())

            print_on_lcd("Enter password")

            password = await get_input()

            wifi.connect(ssid, password)

        config['ssid'] = ssid
        config['wifi-password'] = password

        file = open('config.txt', 'w+')
        file.write(json.dumps(config))
        file.close()

uasyncio.run(main())