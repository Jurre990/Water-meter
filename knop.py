import os
import time
from datetime import date
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import shelve

def UpdateDatabase(count):
    d = shelve.open("/home/pi/Desktop/database")
    print(count)
    d["totaal"] += count
    try:
        d[str(date.today())] += count
    except:
        d[str(date.today())] = count

    d.close()

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
chan0 = AnalogIn(mcp, MCP.P0)

waterFlow = False
magnetClose = False
cycleCount = 0
timeVar = time.time()
while True:
    if ((time.time()-timeVar)>5 and waterFlow==True):
        print("waterflow stopped")
        waterFlow = False
        #update database
        UpdateDatabase(cycleCount)
        cycleCount = 0
    if (chan0.value>33000):
        waterFlow=True
        if (magnetClose==False):
            magnetClose=True
            cycleCount += 1
            print(str(cycleCount) + " " + str(time.time()-timeVar))
            timeVar = time.time()
    else:
        magnetClose = False
    time.sleep(0.1)