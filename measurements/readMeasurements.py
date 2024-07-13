#Here some description





#======================================

import gpiozero
import serial

import time
import requests
import json
import schedule

import os
from dotenv import load_dotenv

from gpiozero.pins.mock import MockFactory
gpiozero.Device.pin_factory = MockFactory()

from gpiozero import CPUTemperature

#======================================

def recvFromArduino():
    global startMarker, endMarker

    ck = ""
    x = "q"  # any value that is not an end- or startMarker
    byteCount = -1  # to allow for the fact that the last increment will be one too many

    # wait for the start character
    while True:
        x = ser.read()
        if x:
            if ord(x) == startMarker:
                break
            else:
                print("Received unexpected character:", x)

    # save data until the end marker is found
    while True:
        x = ser.read()
        print(x)
        if x:
            if ord(x) == endMarker:
                break
            elif ord(x) != startMarker:
                ck += x.decode("utf-8")  # change for Python3
                byteCount += 1
        else:
            print("No data received. Waiting for data...")




    return(ck)

#============================

def waitForArduino():

    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    global startMarker, endMarker

    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            pass

        msg = recvFromArduino()

        print (msg)

#======================================

def connectToArduino(start, location, cpu_temp, OutsideTemperature, ending):
    waitingForReply = False

    sendToArduino(start, location, cpu_temp, OutsideTemperature, ending)

    waitingForReply = True

    if waitingForReply == True:

      while ser.inWaiting() == 0:
          pass

          dataRecvd = recvFromArduino()
          print ("Reply Received  " + dataRecvd)
          waitingForReply = False

          print ("===========")

          time.sleep(1)


           # API CALL
#======================================

load_dotenv()

api_key = os.getenv('APIkey')
city = os.getenv('city')
url = "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric" % (city, api_key)  #Get city and units from api


def RetvieweWeather(url):
    response = requests.get(url)
    weatherdata = json.loads(response.text)
    return '{:.2f}'.format(weatherdata["main"]["temp"]) + ' C'


OutsideTemperature = RetvieweWeather(url)

def SaveWeather():
    global OutsideTemperature
    result = RetvieweWeather(url)
    # if OutsideTemperature is not None:
    #     # Compare with the previous result
    #     if result > OutsideTemperature:
    #         print(f"New result ({result}) is greater than previous result ({OutsideTemperature})")
    #     elif result < OutsideTemperature:
    #         print(f"New result ({result}) is less than previous result ({OutsideTemperature})")
    #     else:
    #         print(f"New result ({result}) is equal to previous result ({OutsideTemperature})")
    OutsideTemperature = result

#Determine the execution cycle for SaveWeather function
schedule.every(15).minutes.do(SaveWeather)

#======================================

# SERIAL Configuration
#======================================

# NOTE the user must ensure that the serial port and baudrate are correct
serPort = '/dev/ttyACM1'
baudRate = 115200
ser = serial.Serial(serPort, baudRate, timeout=1)
print ("Serial port " + serPort + " opened  Baudrate " + str(baudRate))
#======================================

# VARIABLES
#======================================

specialCharacterMap =  {ord('ä'):'a'}
startMarker = 60
endMarker = 62
start = "<"
location = city.translate(specialCharacterMap)

#initialializing temp values

iniTemp1 = 20
iniTemp2 = 10.2
ending = ">"
divider = ","
waitForArduino()

#======================================

#   DATA to arduino
#======================================

def sendToArduino(start, location, iniTemp1, iniTemp2, ending):
    ser.write(start.encode('utf-8')) 

    ser.write(location.encode('utf-8')) 
    ser.write(divider.encode('utf-8')) 

    ser.write(str(iniTemp1).encode('utf-8')) 
    ser.write(divider.encode('utf-8')) 

    ser.write(str(iniTemp2).encode('utf-8')) 
    ser.write(divider.encode('utf-8')) 

    ser.write(ending.encode('utf-8')) 
    
#======================================

#   MAIN PROGRAM
#======================================

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
    ser.reset_input_buffer()

    while True:
     cpu = CPUTemperature().temperature
     cpu_temp = round(cpu, 1)                            # rounding to 1 decimal

     connectToArduino(start, location, cpu_temp, OutsideTemperature, ending)

     schedule.run_pending()
     time.sleep(1)

     ser.close

