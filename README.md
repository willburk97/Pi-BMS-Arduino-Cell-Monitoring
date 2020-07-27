# Pi-BMS-Arduino-Cell-Monitoring

Still very much a work in progress, but this is the early stage of a BMS, Battery Management System using an Arduino (nano) to monitor each Cell within a pack
and a Raspberry Pi as the SPI master collecting the data from each Arduino and ultimately controlling everything / displaying the data to a monitor and sending
the data to Adafruit io for remote monitoring.

I connected one Arduino for comm testing and then started testing using Opto-Couplers/Opto-Isolators (I don't know the difference).  The opto-couplers will be
necessary because the Arduinos will not have a common ground, nor will they have the same ground as the Pi (all but one will not, technically).  Opto-couplers
are inherently slow though so I had to slow down the SPI comm a lot. I also only tested with one opto-coupler on the clock signal (since this was the fastest signal.)
To make this work each Arduino will need it's own 4 opto-couplers (MISO, MOSI, CLK, and ENA).  Since I'm building a 4S (li-ion) BMS, I'll need 16 total opto-couplers.

I think I've decided to go another route...  In a separate repository, I used ESP-12E modules to monitor each cell and then simply upload via WiFi to Adafruit io. 
This "simplified" the common ground issue. Any device, such as a Pi could simply pull this data off WiFi/internet.  WHat I don't like about that solution is the need
for internet access.  I prefer the idea of being able to sample the batteries every few seconds and making real-time decisions. With the adafruit io I can only update
every 60 seconds or so (on their free plan) because of data update restrictions.

My original BMS used multiple voltage dividers to monitor each cell, but scaling (at 4S) 16 volts down to the A/D converter input of 5v (or whatever) has inherent accuracy
issues. (Especially since, to calculate Cell 4's voltage you have to measure all 4 cells and subtract cells 1-3 which adds to the inaccuracies.  I'm thinking this was
accurate enough and I may go back to this. (But with an ESP32 (new ESP8266) which has built in wifi...or with a Raspbery Pi with an add-on A/D converter.)


My BMS's have all mostly been setup to simply monitor the voltages and turn off my load if one cell gets too low.  With my ESP-12E BMS's (and this Arduino-Pi style
if I wanted to) I was easily able to ad a mosfet and a load resistor in order to drain down the high batteries and keep the pack balanced.  Before this I just balanced it
manually when it got out of balance. My "cells" are ~1.4 kwh cells (160P 18650 batteries) so it wasn't a big deal to just connect a charger for a few hours to the weak one.
