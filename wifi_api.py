import network
import time
from lcd_controller import LcdController

lcd = LcdController()

class Wifi:
    def __init__(self):
        #initialize network library
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.disconnect()

        self.ssid = ""

    async def connect(self, ssid, password):
        self.ssid = ssid

        self.wlan.connect(self.ssid, password)

        while (self.get_connection_message() == -1): continue


    def get_ssid_list(self):
        return [val[0].decode('utf-8') for val in self.wlan.scan() if val[0].decode('utf-8') != ""]  # check if wlan is public

    def get_connection_message(self):
        status = self.wlan.status()
        if (status == network.STAT_IDLE):
            lcd.print_on_lcd('No connection')
            return 0
        elif (status == network.STAT_CONNECTING):
            lcd.print_on_lcd('Connecting...')
            return -1
        elif (status == network.STAT_WRONG_PASSWORD):
            lcd.print_on_lcd('Wrong password')
            return 0
        elif (status == network.STAT_NO_AP_FOUND):
            lcd.print_on_lcd('No responce from network')
            return 0
        elif (status == network.STAT_CONNECT_FAIL):
            lcd.print_on_lcd('Connection failed')
            return 0
        elif (status == network.STAT_GOT_IP):
            lcd.print_on_lcd('Connected')
            return 1
        else:
            lcd.print_on_lcd("Connection failed")
            return 0


    def get_ip(self):
        return self.wlan.ifconfig()[0]

    def is_connected(self):
        return self.wlan.isconnected()