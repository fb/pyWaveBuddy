
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

def make_pov(lst):
    return nmea_csum("$POV," + ",".join([str(l) for l in lst]))

def test_pov():
    assert "$POV,P,1018.35*39" == make_pov(['P',1018.35])
    assert "$POV,H,58.42*24" == make_pov(['H',58.42])
    pov = []
    pov.append('Q')
    pov.append('23.3')
    sentence = make_pov(pov)
    assert "$POV,Q,23.3*04" == sentence
    pov = []
    pov.append('Q')
    pov.append('23.3')
    pov.append('H')
    pov.append('58.42')
    assert "$POV,Q,23.3,H,58.42*69" == make_pov(pov)

def test_checksum():
    assert "$POV,P,1018.35*39" == nmea_csum("$POV,P,1018.35")

