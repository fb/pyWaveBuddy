from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.uuid import UUID
from nordic import UARTService
import time
import board

SERVICE_UUID = "7067452c-0513-41a0-a0bd-b8582a217bb0"
CHARACTERISTIC_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB"

ble = BLERadio()
ble.name = "ble_uart.py"

uart = UARTService()

advertisement = ProvideServicesAdvertisement(uart)

"""
input is an NMEA sentence including the leading '$' and excluding '*'
example: an input of
"$POV,P,1018.35" will return
"$POV,P,1018.35*39"
"""
def nmea_csum(input):
    csum = 0

    for c in input[1:]:
        csum ^= ord(c)

    return input + "*{:02x}".format(csum)

def sdp_res_to_press(res):
    i = result[0] << 8 | result[1]
    if i & (1 << 15):
        i -= 0x8FFF
    return i / 20.0

i2c = board.I2C()
while not i2c.try_lock():
    pass

while True:
    print("hello")
    i2c.writeto(0x21, bytes([0x3F, 0xF9])) # stop
    i2c.writeto(0x21, bytes([0x36, 0x15])) # continous mode
    ble.start_advertising(advertisement)  # Advertise when not connected.
    while not ble.connected:
        pass

    print("connected!")
    while ble.connected:
        time.sleep(0.1)
        result = bytearray(9)
        i2c.readfrom_into(0x21, result)
        sentence = nmea_csum("$POV,Q,{:1.1f}".format( sdp_res_to_press(result) ) )
        uart.write(sentence)
        uart.write("\n")
        print(sentence)