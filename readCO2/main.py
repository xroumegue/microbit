from microbit import display, pin0, pin14, button_a
from time import sleep
from tm1637 import TM1637
from sgp30 import SGP30
from struct import pack

C = SGP30()
lcd = TM1637(pin0, pin14)

display.scroll("...CO2...")
i=0
f=None

while True:
    m = C.eCO2()
    lcd.show("{:04d}".format(m))
    if m > 600:
        display.show("!", clear = True, wait = True)
    if button_a.is_pressed():
        f = open('meas.dat', 'wb')
        i = 0
    if f:
        if i < 8192:
            f.write(pack("H", m))
            i += 1
            display.show("+", clear = True, wait = False)
        else:
            f.close()
            f = None
    sleep(1)
