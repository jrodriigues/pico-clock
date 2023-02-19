from machine import Pin,I2C
import time
import RGB1602
from random import randint

lcd=RGB1602.RGB1602(16,2)
sound = Pin(13, Pin.OUT)
button1 = Pin(12, Pin.IN) # Changes background color

# set start time : {hour1}{hour2}:{minu1}{minu2}:{sec}
hour1 = 2
hour2 = 1
minu1 = 5
minu2 = 5
sec = 0

# set start date : {dd}/{mm}/{yyyy}
day = 20
month = 2
year = 2023

# generate a random RGB color to start the program
# this list will be updated with new values every hour
colors = [randint(0,255),randint(0,255),randint(0,255)]

# reset the LCD before starting
lcd.clear()

while True:
    sound.value(0)
    
    # Condition that prevents seconds from going beyond 59
    if sec == 6:
        sec = 0
        minu2 += 1
        
    # Condition that prevents minutes from going beyond 59
    if minu2 == 10:
        minu2 = 0
        minu1 += 1 
    if minu1 == 6:
        minu1 = 0
        minu2 = 0
        hour2 += 1
        
    # Condition that prevents hours from going beyond 23
    # and starts a new day which triggers the following events:
    # - RGB color changes to a random number
    if hour2 == 10:
        hour2 = 0
        hour1 += 1
        
    if hour2 == 4 and hour1 == 2:
        hour2 = 0
        hour1 = 0
        minu1 = 0
        minu2 = 0
        sec = 0
        day += 1
        colors[0] = randint(0,255)
        colors[1] = randint(0,255)
        colors[2] = randint(0,255)
    
    # Adjust background color and set cursor ready for date printout
    #lcd.setRGB(colors[0],colors[1],colors[2])
    lcd.setCursor(3,1)    
    
    if day < 10 and month < 10:
        lcd.printout(f"0{day}/0{month}/{year}")
    elif day < 10 and month >= 10:
        lcd.printout(f"0{day}/{month}/{year}")
    elif day >= 10 and month < 10:
        lcd.printout(f"{day}/0{month}/{year}")
    elif day >= 10 and month >= 10:
        lcd.printout(f"{day}/{month}/{year}")    
    
    for s in range(10):
        display = f"{hour1}{hour2}:{minu1}{minu2}:{sec}{s}"
        lcd.setCursor(4,0)
        lcd.printout(display)
        
        if button1.value() == 0:
            lcd.setRGB(randint(0,255),randint(0,255),randint(0,255))
            
        time.sleep(1)
    sec += 1
    
    



