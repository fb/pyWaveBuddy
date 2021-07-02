from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.uuid import UUID
from nordic import UARTService
import time
import board

from openvario import make_pov
from sensirion import sdp33_press

ble = BLERadio()
ble.name = "pyWaveBuddy"

uart = UARTService()

advertisement = ProvideServicesAdvertisement(uart)

i2c = board.I2C()
while not i2c.try_lock():
    pass

i2c.writeto(0x21, bytes([0x3F, 0xF9])) # stop
i2c.writeto(0x21, bytes([0x36, 0x15])) # continous mode

while True:
    if not ble.connected and not ble.advertising:
        print("start advertising")
        ble.start_advertising(advertisement)

    if ble.connected and ble.advertising:
        print("stop advertising")
        ble.stop_advertising()

    time.sleep(0.1)
    sentence = ''
    pov = []

    buf = bytearray(9)
    i2c.readfrom_into(0x21, buf)
    pov.append('Q')
    pov.append('{:1.1f}'.format( sdp33_press(buf) ))

    if pov:
        sentence = make_pov(pov)

    if ble.connected and sentence:
        uart.write(sentence)
        uart.write("\n")

    print(sentence, ble.advertising, ble.connected)
