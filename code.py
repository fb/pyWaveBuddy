from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.uuid import UUID
from nordic import UARTService
import time

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

while True:
    print("hello")
    ble.start_advertising(advertisement)  # Advertise when not connected.
    while not ble.connected:
        pass

    print("connected!")
    while ble.connected:
        time.sleep(1.0)
        sentence = nmea_csum("$POV,P,1018.35")
        uart.write(sentence)
        uart.write("\n")
        print(sentence)