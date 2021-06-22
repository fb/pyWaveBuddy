# SPDX-FileCopyrightText: 2019 Dan Halbert for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`nordic`
====================================================

This module provides Services used by Nordic Semiconductors.

"""

from adafruit_ble import Service
from adafruit_ble.uuid import VendorUUID
from adafruit_ble.characteristics.stream import StreamOut, StreamIn

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE.git"


SERVICE_UUID = "7067452c-0513-41a0-a0bd-b8582a217bb0"
TX_CHARACTERISTIC_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB"

class UARTService(Service):
    """
    Provide UART-like functionality via the Nordic NUS service.

    :param int timeout:  the timeout in seconds to wait
      for the first character and between subsequent characters.
    :param int buffer_size: buffer up to this many bytes.
      If more bytes are received, older bytes will be discarded.

    See ``examples/ble_uart_echo_test.py`` for a usage example.
    """

    # pylint: disable=no-member
    uuid = VendorUUID(SERVICE_UUID)
    _server_tx = StreamOut(
        uuid=VendorUUID(TX_CHARACTERISTIC_UUID),
        timeout=1.0,
        buffer_size=64,
    )
    _server_rx = StreamIn(
        uuid=VendorUUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
        timeout=1.0,
        buffer_size=64,
    )

    def __init__(self, service=None):
        super().__init__(service=service)
        self.connectable = True
        if not service:
            self._rx = self._server_rx
            self._tx = self._server_tx
        else:
            # If we're a client then swap the characteristics we use.
            self._tx = self._server_rx
            self._rx = self._server_tx

    def read(self, nbytes=None):
        """
        Read characters. If ``nbytes`` is specified then read at most that many bytes.
        Otherwise, read everything that arrives until the connection times out.
        Providing the number of bytes expected is highly recommended because it will be faster.

        :return: Data read
        :rtype: bytes or None
        """
        return self._rx.read(nbytes)

    def readinto(self, buf, nbytes=None):
        """
        Read bytes into the ``buf``. If ``nbytes`` is specified then read at most
        that many bytes. Otherwise, read at most ``len(buf)`` bytes.

        :return: number of bytes read and stored into ``buf``
        :rtype: int or None (on a non-blocking error)
        """
        return self._rx.readinto(buf, nbytes)

    def readline(self):
        """
        Read a line, ending in a newline character.

        :return: the line read
        :rtype: bytes or None
        """
        return self._rx.readline()

    @property
    def in_waiting(self):
        """The number of bytes in the input buffer, available to be read."""
        return self._rx.in_waiting

    def reset_input_buffer(self):
        """Discard any unread characters in the input buffer."""
        self._rx.reset_input_buffer()

    def write(self, buf):
        """Write a buffer of bytes."""
        self._tx.write(buf)
