import rp2
from config import *
import uasyncio
from methods import get_input
import time
import json

rp2.country('PL')

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
        lcd.putstr("Config not detected")
        time.sleep(2)
        lcd.clear()

        lcd.putstr("Enter new password")
        time.sleep(2)
        lcd.clear()

        config = {}

        #TODO Secure password by hashing it
        config['password'] = await get_input()
        lcd.putstr(json.dumps(config['password']))

        #TODO Input for wifi credentials

        file = open('config.txt', 'w+')
        file.write(json.dumps(config))
        file.close()

uasyncio.run(main())