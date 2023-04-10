from machine import Pin, I2C, RTC, PWM
import time
import RGB1602
from random import randint

# Global variables

SETTINGS = [
    "Set alarm",
    "Show message"
]

MESSAGES = [
    "Test message!!"
]

# Buzzer variables - PWM
BUZZ_FREQ = 4000
BUZZ_DUTY = 65536 / 2
BUZZ_LENGTH = 10

# Initiate main clock, pico rtc, lcd, buzzer and buttons
rtc = machine.RTC()
rtc.datetime((2023, 2, 26, 3, 22, 15, 30, 50))
lcd = RGB1602.RGB1602(16, 2)
buzzer = PWM(Pin(26))

# Changes background color               ---> green wire
buttonRGB = Pin(12, Pin.IN)

# Select menu entry                      ---> yellow wire
buttonMulti = Pin(15, Pin.IN)

# Enters and navigates menu entries      ---> white wire
buttonSettings = Pin(7, Pin.IN)


""" Initiate rtc module (STILL TESTING)
i2c = machine.I2C(1, sda=machine.Pin(2),scl=machine.Pin(3),freq=400000)
rtc = DS3231(i2c) """


def setColorRed(lcd):
    """ Change lcd background color to red """

    lcd.setRGB(255, 0, 0)


def setColorBlue(lcd):
    """ Change lcd background color to blue """

    lcd.setRGB(0, 0, 255)


def setColorGreen(lcd):
    """ Change lcd background color to green """

    lcd.setRGB(0, 255, 0)


def changeRGB(lcd):
    """ Change lcd background color to one of the following 3:
    Blue, Red, Green """
    
    rnd = randint(1, 3)

    if rnd == 1:
        setColorBlue(lcd)

    elif rnd == 2:
        setColorGreen(lcd)

    elif rnd == 3:
        setColorRed(lcd)

def rgbHandler(pin):
    """ Routine for buttonRGB irq """

    global buttonRGB_state

    # Prevent multiple routines simultaneously
    buttonRGB.irq(handler=None)

    print(" ---------- RGB TRIGGER ROUTINE INIT ---------- ")

    if buttonRGB.value() == 0 and buttonRGB_state == 1:
        changeRGB(lcd)
        time.sleep(0.2)
        print(" *** Color changed *** ")

    buttonRGB.irq(handler=rgbHandler)
    
    print(" ---------- RGB TRIGGER ROUTINE END ---------- \n")

def settingsHandler(pin):
    """ Routine for buttonSettings irq
    
    - The 0.2 sleeps are to prevent multiple
      reads on the same button press.
    - There are 2 timers in this routine which will
      end this routine if no buttons are pressed:
      1) mainTimer will be activated in the main menu
      2) menuTimer will be activated after entering a menu entry """

    global buttonSettings_state
    global alarmHour
    global alarmMinute

    buttonSettings.irq(handler=None)
    time.sleep(0.2)

    print(" ---------- SETTINGS TRIGGER ROUTINE INIT ---------- ")

    lcd.clear()
    mainTimer = 100
    menuTimer = 100
    setting = 0

    while mainTimer > 0:
        # Stops the interrupt once the last setting is reached
        # and the main program is resumed

        if setting == len(SETTINGS):
            break

        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.printout(SETTINGS[setting])

        # Changes for the next menu entry

        if buttonSettings.value() == 0:
            lcd.clear()
            time.sleep(0.2)
            lcd.setCursor(0, 0)
            lcd.printout(SETTINGS[setting])
            setting += 1
            mainTimer = 100
            continue

        # Enters the current entry and reset the 10s timer

        if buttonMulti.value() == 0:
            time.sleep(0.2)
            # setting = 0 --> set alarm function
            # set hour first, then minutes - one loop for each
            # After the minute loop, display the alarm timer set

            if setting == 0:
                while menuTimer > 0:
                    lcd.clear()
                    lcd.setCursor(0, 0)
                    lcd.printout(f"Hour: {formatNumber(alarmHour)}")

                    if buttonSettings.value() == 0:
                        alarmHour += 1
                        if alarmHour > 23:
                            alarmHour = 0

                        time.sleep(0.2)
                        menuTimer = 100

                    if buttonMulti.value() == 0:
                        menuTimer = 100
                        break

                    menuTimer -= 1
                    time.sleep(0.1)

                # Prevents a second read after hour assignment

                time.sleep(0.2)
                
                while menuTimer > 0:
                    lcd.clear()
                    lcd.setCursor(0, 0)
                    lcd.printout(f"Minute: {formatNumber(alarmMinute)}")

                    if buttonSettings.value() == 0:
                        alarmMinute += 1
                        
                        if alarmMinute > 59:
                            alarmMinute = 0
                            
                        time.sleep(0.2)
                        menuTimer = 100

                    if buttonMulti.value() == 0:
                        menuTimer = 100
                        lcd.setCursor(0, 0)
                        lcd.printout("Alarm set to:")
                        lcd.setCursor(0, 1)
                        lcd.printout(
                            f"{formatNumber(alarmHour)}:{formatNumber(alarmMinute)}")

                        time.sleep(2)
                        break

                    menuTimer -= 1

                    # Reset the alarm variables in case no buttons are pressed
                    # just before exiting the menuTimer loop

                    if menuTimer == 1:
                        alarmHour = 0
                        alarmMinute = 0

                    time.sleep(0.1)
                break

            # Prints a random message from the MESSAGES variable

            elif setting == 1:
                index = randint(0, len(MESSAGES0))
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.printout(MESSAGES0[index])
                time.sleep(5)
                break

        mainTimer -= 1
        time.sleep(0.1)

    buttonSettings.irq(handler=settingsHandler,
                       trigger=machine.Pin.IRQ_FALLING)

    print(" ---------- SETTINGS TRIGGER ROUTINE END ---------- \n")

def formatDate():
    """ Function to return a date string with format dd/MM/yyyy """

    if rtc.datetime()[2] < 10 and rtc.datetime()[1] < 10:
        date = (
            f"0{rtc.datetime()[2]}/0{rtc.datetime()[1]}/{rtc.datetime()[0]}")

    elif rtc.datetime()[2] < 10 and rtc.datetime()[1] >= 10:
        date = (
            f"0{rtc.datetime()[2]}/{rtc.datetime()[1]}/{rtc.datetime()[0]}")

    elif rtc.datetime()[2] >= 10 and rtc.datetime()[1] < 10:
        date = (
            f"{rtc.datetime()[2]}/0{rtc.datetime()[1]}/{rtc.datetime()[0]}")

    elif rtc.datetime()[2] >= 10 and rtc.datetime()[1] >= 10:
        date = (f"{rtc.datetime()[2]}/{rtc.datetime()[1]}/{rtc.datetime()[0]}")

    return date

def formatTime():
    """ Function to return a time string with format hh:mm:ss """

    timeString = ""

    if rtc.datetime()[4] < 10:
        timeString += "0" + str(rtc.datetime()[4]) + ":"

    else:
        timeString += str(rtc.datetime()[4]) + ":"

    if rtc.datetime()[5] < 10:
        timeString += "0" + str(rtc.datetime()[5]) + ":"

    else:
        timeString += str(rtc.datetime()[5]) + ":"

    if rtc.datetime()[6] < 10:
        timeString += "0" + str(rtc.datetime()[6])

    else:
        timeString += str(rtc.datetime()[6])

    return timeString


def formatNumber(number):
    """ Function to return a formatted string for hour/minute/second """

    value = 0

    if number < 10:
        value = f"0{number}"

    else:
        value = str(number)

    return value

# Assign irq's
buttonRGB.irq(handler=rgbHandler, trigger=machine.Pin.IRQ_FALLING)
buttonSettings.irq(handler=settingsHandler, trigger=machine.Pin.IRQ_FALLING)

# Initiate the LCD background color and buttons' current state
setColorGreen(lcd)
buttonRGB_state = buttonRGB.value()
buttonSettings_state = buttonSettings.value()
buttonMulti_state = buttonMulti.value()


# Alarm variables and initial buzzer config
alarmHour = 0
alarmMinute = 0
buzzer.freq(BUZZ_FREQ)
buzzer.duty_u16(0)

def main():

    global alarmHour
    global alarmMinute
    global BUZZ_LENGTH

    while True:
        # Update the button values at every clock pulse
        # which will be used in the event of an irq

        buttonRGB_state = buttonRGB.value()
        buttonSettings_state = buttonSettings.value()
        buttonMulti_state = buttonMulti.value()

        # Update the clock display with the RTC time

        lcd.setCursor(0, 0)
        lcd.clear()
        lcd.printout(formatTime())
        lcd.setCursor(0, 1)
        lcd.printout(formatDate())

        # Activate buzzer if alarm is triggered

        if rtc.datetime()[4] == alarmHour and rtc.datetime()[5] == alarmMinute:

            # Checks for button press for an early alarm stop
            if buttonMulti.value() == 0:
                buzzer.duty_u16(0)
                alarmHour = 0
                alarmMinute = 0
                BUZZ_LENGTH = 10
                continue

            # Alternates between low and high values for alarm sound until timer finishes
            if BUZZ_LENGTH > 0:
                if BUZZ_LENGTH % 2 == 0:
                    buzzer.duty_u16(int(BUZZ_DUTY))

                else:
                    buzzer.duty_u16(0)
                BUZZ_LENGTH -= 1

            else:
                buzzer.duty_u16(0)
                alarmHour = 0
                alarmMinute = 0
                BUZZ_LENGTH = 10

        time.sleep(1)

main()
