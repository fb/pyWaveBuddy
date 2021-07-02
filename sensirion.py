import struct

def first_word_to_int(buf):
    # data is 2 bytes big-endian
    return struct.unpack('>h', buf[0:2])[0]

def sdp33_press(buf):
    return first_word_to_int(buf) / 20.0

def test_calc_sdp33():
    assert 1.0 == sdp33_press(bytes([0, 20]))
    assert -1.0 == sdp33_press(bytes([0xff, 0xec]))
    assert -1.0 == sdp33_press(bytes([0xff, 0xec, 0xee]))

def test_calc_shtc3():
    pass
