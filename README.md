# Project repo that contains files for a personalised multi-function clock alarm using RPi Pico microcontroller. 

## Equipment used
* RGB 16x2 LCD Display (I2C compatible) - [link](https://thepihut.com/products/rgb-16x2-i2c-lcd-display-3-3v-5v?variant=39862439444675)
* RTC module for Raspberry Pi - [link](https://thepihut.com/products/mini-rtc-module-for-raspberry-pi)
* Tactile push buttons - [link](https://thepihut.com/products/tactile-switch-buttons-6mm-tall-x-10-pack)
* Jumper wires (various sizes)
* Half breadboard - [link](https://thepihut.com/products/raspberry-pi-breadboard-half-size)
* Buzzer - [link](https://thepihut.com/products/buzzer-5v-breadboard-friendly)
* Resistors (10k and 220 Ohm) 
* MicroUSB 3x AA battery holder for power supply - [link](https://thepihut.com/products/microusb-battery-holder-3xaa)
* Exterior case (3D print created using tinkercad) - [click to download STL file](https://github.com/jrodriigues/pico-clock/files/11189986/pico-alarm-clock-case.zip)

***

Currently, main.py is still using the onboard RTC module of the Raspberry Pi Pico as I am still trying to find a working driver for the above RTC (that specific module is meant to be used with a Raspberry Pi, not a Pico microcontroller, so I am still trying to find a way to make the I2C work with it). ***DS3231.py*** is my current test driver.

The file ***RGB1602.py*** is the driver that controls the LCD display, which is provided by the seller Waveshare.

