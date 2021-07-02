from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.uuid import UUID
from nordic import UARTService
import time
import board

from openvario import make_pov

ble = BLERadio()
ble.name = "pyWaveBuddy"

uart = UARTService()

advertisement = ProvideServicesAdvertisement(uart)


def sdp_res_to_press(res):
    i = result[0] << 8 | result[1]
    if i & (1 << 15):
        i -= 0x8FFF
    return i / 20.0

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
    result = bytearray(9)
    i2c.readfrom_into(0x21, result)
    pov = []
    pov.append('Q')
    pov.append('{:1.1f}'.format( sdp_res_to_press(result) ))
    sentence = make_pov(pov)
    if ble.connected:
        uart.write(sentence)
        uart.write("\n")
    print(sentence, ble.advertising, ble.connected)
