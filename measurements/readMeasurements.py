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

    # ck = ""
    # x = "q" # any value that is not an end- or startMarker
    # byteCount = -1 # to allow for the fact that the last increment will be one too many
    # print("before ser.read", x)
    # # wait for the start character
    # while ord(x) != startMarker:
    #     x = ser.read()
    #     print("after inputting ser.read", x)

    # # save data until the end marker is found
    #     while ord(x) != endMarker:
    #         if ord(x) != startMarker:
    #             ck = ck + x.decode("utf-8") # change for Python3
    #             byteCount += 1
    #             x = ser.read()

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

        print (msg) # python3 requires parenthesis
        print ()

#======================================

def runTest(start, location, temp, temp1, ending):
    waitingForReply = False

    sendToArduino(start, location, temp, temp1, ending)

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

# with open('APIkey.txt') as f:
#    api_key = f.readline()
# api_key = api_key.strip()

# with open('city.txt') as f:
#     city = f.readline()
# city = city.strip()

url = "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric" % (city, api_key)  #Get city and units from api




#def get_temperature(weatherdata):
#    print ("weatherdata is: ", weatherdata)
#    if weatherdata != null:                                  #outside temp convert to float also determine under which topics data can be found in API request
 #   cityTemperature = '{:.2f}'.format(weatherdata["main"]["temp"]) + ' C'

#    else:
#       cityTemperature = 0.0

  #  print ("cityTemperature is: ", cityTemperature)

#    return cityTemperature



def RetvieweWeather(url):
    print("I'm working...")
    response = requests.get(url)
    weatherdata = json.loads(response.text)
    cityTemperature = '{:.2f}'.format(weatherdata["main"]["temp"]) + ' C'

    print ("Retview", cityTemperature)

    return cityTemperature




Initialweather = RetvieweWeather(url)


def SaveWeather():

    global Initialweather
    result = RetvieweWeather(url)

    print("insideSaveWeather", Initialweather)


    if Initialweather is not None:
        # Compare with the previous result
        if result > Initialweather:
            print(f"New result ({result}) is greater than previous result ({Initialweather})")
        elif result < Initialweather:
            print(f"New result ({result}) is less than previous result ({Initialweather})")
        else:
            print(f"New result ({result}) is equal to previous result ({Initialweather})")

    Initialweather = result

schedule.every(1).minutes.do(SaveWeather)


#def InitialWeather():
#    cityTemperature = RetvieweWeather(url)
#    print ("initialcitytemp", cityTemperature)
#    return cityTemperature


#weather = result



#print("weather", weather)




#def updateWeather(previous_result):

 #   print ("weather", weather)
#    print ("previousresult", previous_result)


#schedule.every(15).seconds.do(updateWeather)





#def run_temperature_display(data):                           #Set lcd preferences also this function uses variables url, mcp, lcd, city
#    while(True):                                            #constantly run request and save it to variable data#
#        return get_temperature(data)                                     # Important to have some delay, since API calls can only be made 1000 per day.

#======================================

# SERIAL Configuration
#======================================

# NOTE the user must ensure that the serial port and baudrate are correct

print ()
print ()

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
    ser.write(start.encode('utf-8')) # change for Python3

    ser.write(location.encode('utf-8')) # change for Python3
    ser.write(divider.encode('utf-8')) # change for Python3

    ser.write(str(iniTemp1).encode('utf-8')) # change for Python3
    ser.write(divider.encode('utf-8')) # change for Python3

    ser.write(str(iniTemp2).encode('utf-8')) # change for Python3
    ser.write(divider.encode('utf-8')) # change for Python3

    ser.write(ending.encode('utf-8')) # change for Python3
    
#======================================

#Saving data to .tsv file
#=====================================

def write_to_file():

    f = open('dataFile.tsv','a') # open file if it does not exist

    
    #time_stamp = time.time()
    temperature = run_request(url) # read the temperature
    #date_stamp = datetime.date()
    
    time_stamp= time.localtime() # get struct_time
    date_stamp = time.strftime("%m/%d/%Y, %H:%M:%S", time_stamp) #make it readable
    f.write(str(date_stamp) + "\t"+ str(temperature)+ "\n") # write it to the file 
    f.closed # close the file
    
#======================================

#   MAIN PROGRAM
#======================================

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
    ser.reset_input_buffer()



    #cityTemperature = weather

    while True:
     print ("in main previous_result", Initialweather)
#     print ("updateWeather", updateWeather())
#     print (RetvieweWeather(url))

#     SaveWeather()
     cpu = CPUTemperature().temperature
     cpu_temp = round(cpu, 1)                            # rounding to 1 decimal
     temp = cpu_temp

     temp1 = 12

     runTest(start, location, temp, temp1, ending)

     schedule.run_pending()


     time.sleep(1)

     ser.close

