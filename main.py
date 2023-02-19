from machine import Pin,I2C
import time
import RGB1602

lcd=RGB1602.RGB1602(16,2)

sec = 0
minu1 = 2
minu2 = 6
hour1 = 0
hour2 = 1

lcd.clear()
lcd.setRGB(255,0,0)

lcd.setCursor(3,1)
lcd.printout("19/02/2023")

while True:
    # prevents seconds from going beyond 59
    if sec == 6:
        sec = 0
        minu2 += 1
        # prevents minutes from going beyond 59
        if minu2 == 9:
            minu1 += 1
            if minu1 == 6:
                minu1 = 0
                hour2 = 1
                # prevents hours from going beyond 23
                if hour2 == 3 and hour1 == 2:
                    hour2, hour1, minu1, minu2, sec = 0
    for s in range(10):
        display = f"{hour1}{hour2}:{minu1}{minu2}:{sec}{s}"
        lcd.setCursor(4,0)
        lcd.printout(display)
        time.sleep(1)
    sec += 1
    
    
