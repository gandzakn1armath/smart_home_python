"""
Ներբեռնում ենք Python 3.6.8 տարբերակը
Ներբեռնում ենք pad4pi գրադարանը(pip install pad4pi)
Ներբեռնում ենք firebase գրադարանը(pip install python-firebase)
Ներբեռնում ենք gpiozero գրադարանը(pip install gpiozero)
"""
from pad4pi import rpi_gpio  #Ներմուծում ենք pad4pi գրադարանը
import time  #Ներմուծում ենք time գրադարանը
import RPi.GPIO as GPIO    #Ներմուծում ենք RPI.GPIO գրադարանը
from firebase import firebase   #Ներմուծում ենք RPI.GPIO գրադարանը
from  gpiozero import PWMOutputDevice, Buzzer    #Ներմուծում ենք gpiozero գրադարանը
from time import sleep    #Ներմուծում ենք time գրադարանի sleep բաժինը
import threading    #Ներմուծում ենք threading գրադարանը

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

try:
        firebase = firebase.FirebaseApplication("https://smart-home-800bc-default-rtdb.firebaseio.com/", None)
        #firebase.put("",'SECURITY',1)
except Exception:
        print("No internet")

in1 = 14
in2 = 15
in3 = 3
in4 = 2
relay = 4

doorIsOpen = 26
doorIsClose = 27
buzzer = PWMOutputDevice(22)
keypadInput = ""

isLedsOn = True
COL_PINS = [13,6,5,0]		
ROW_PINS = [21,20,16,19] 
GPIO.setup(23,GPIO.IN)
yellowR = PWMOutputDevice(in1)
yellowL = PWMOutputDevice(in2)
blueL = PWMOutputDevice(in3)
blueR = PWMOutputDevice(in4)
relayR = PWMOutputDevice(relay)
doorR = PWMOutputDevice(doorIsOpen)
doorL = PWMOutputDevice(doorIsClose)
door = 26
myGPIO = 21 
KEYPAD = [
			["1","2","3","A"],
			["4","5","6","B"],
			["7","8","9","C"],
			["*","0","#","D"]]
def key_pressed(key):
        global keypadInput
        if key != "D" and key != "C" and key != "B" and key != "A"and key != "*" and key != "#":
                keypadInput += key
        elif key == "D":
                try:
                        pinCode = firebase.get('PIN_CODE',None)
                        print(pinCode)
                        print(keypadInput)
                        if pinCode == keypadInput:
                                getDoor = firebase.get('DOOR',None)
                                print(getDoor)
                                if getDoor:
                                        firebase.put("",'DOOR',0)
                                        firebase.put("",'LED_YELLOW',0)
                                        firebase.put("",'LED_BLUE',0)
                                        firebase.put("",'LED_GREEN',0)
                                       
                                else:
                                        firebase.put("",'DOOR',1)
                                        firebase.put("",'LED_YELLOW',1)
                                        firebase.put("",'LED_BLUE',1)
                                        firebase.put("",'LED_GREEN',1)
                                        
                                keypadInput = ""
                        else:
                                buzzer.on()
                                sleep(1)
                                buzzer.off()
                                keypadInput = ""
                except Exception:
                        keypadInput = ""
                        buzzer.on()
                        sleep(0.1)
                        buzzer.off()
                        sleep(0.1)
                        buzzer.on()
                        sleep(0.1)
                        buzzer.off()
                        sleep(0.1)
                        buzzer.on()
                        sleep(0.1)
                        buzzer.off()
                        
	
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
keypad.registerKeyPressHandler(key_pressed)

def yellowOn():
        yellowR.on()
        yellowL.off()

    
def yellowOff():
        yellowR.off()
        yellowL.off()
    
def blueOn():
        blueR.on()
        blueL.off()
    
def blueOff():
        blueR.off()
        blueL.off()
    
def greenOn():
        relayR.on()
    
def greenOff():
        relayR.off()
    
def openDoor():
        doorR.on()
        doorL.off()
    
def closeDoor():
        doorR.off()
        doorL.on()

def ledOn():
        greenOn()
        yellowOn()
        blueOn()

def ledOff():
        greenOff()
        yellowOff()
        blueOff()
     
def blue():
        global isLedsOn
        while True:
                if isLedsOn:
                        try:
                                getBlue = firebase.get('LED_BLUE',None)
                                if getBlue == 1:
                                        blueOn()
                                else:
                                        blueOff()
                        except KeyboardInterrupt:
                                keypad.cleanup()
                                print("Keypad Controller is interrupted")
                                break
                        except Exception:
                        
                                try:
                                        sleep(2)
                                except  KeyboardInterrupt:
                                        print("\nFinish")
                                        break
                                
def yellow():
        global isLedsOn
        while True:
                if  isLedsOn:
                        try:
                                getYellow = firebase.get('LED_YELLOW',None)
                                if getYellow == 1:
                                        yellowOn()
                                else:
                                        yellowOff()
                        except KeyboardInterrupt:
                                keypad.cleanup()
                                print("Keypad Controller is interrupted")
                                break
                        except Exception:
                                try:
                                        sleep(2)
                                except  KeyboardInterrupt:
                                        print("\nFinish")
                                        break
                                
def green():
        global isLedsOn
        while True:
                if isLedsOn:
                        try:
                                getGreen = firebase.get('LED_GREEN',None)
                                if getGreen == 1:
                                        greenOn()
                                else:
                                        greenOff()
                        except KeyboardInterrupt:
                                keypad.cleanup()
                                print("Keypad Controller is interrupted")
                                break
                        except Exception:
                                try:
                                        sleep(2)
                                except  KeyboardInterrupt:
                                        print("\nFinish")
                                        break
                                
threadBlue = threading.Thread(target=blue)
threadYellow = threading.Thread(target=yellow)
threadGreen = threading.Thread(target=green)

def ledThreadOn():
        threadBlue.start()
        threadYellow.start()
        threadGreen.start()
        
def ledThreadOff():
        pass
        
def sensor():
        while True:
                sensorL = GPIO.input(23)
                if sensorL:  
                        try:
                                firebase.put("",'SENSOR',1)
                                security = firebase.get('SECURITY',None)
                                global isLedsOn
                                if  security:
                                        isLedsOn = False
                                        buzzer.on()
                                        i  = 5
                                        while i > 0:
                                                ledOn()
                                                buzzer.value = 1
                                                sleep(0.5)
                                                buzzer.value = 0.2
                                                ledOff()
                                                sleep(0.5)
                                                i-=1
                                        isLedsOn = True
                                        buzzer.off()
                                sleep(8)
                                firebase.put("",'SENSOR',0)
                        except Exception:
                                sleep(2)
                                        
                        
threadSensor = threading.Thread(target=sensor)        
threadSensor.start()

def door():
        while True:
                try:
                        getDoor = firebase.get('DOOR',None)
                        if getDoor:
                                openDoor()
                        else:
                                closeDoor()
                except KeyboardInterrupt:
                        keypad.cleanup()
                        print("Keypad Controller is interrupted")
                        break
                except Exception:
                        try:
                                sleep(2)
                        except  KeyboardInterrupt:
                                print("\nFinish")
                                break
                        

threadDoor = threading.Thread(target=door)
threadDoor.start()
#start leds thread
ledThreadOn()

while True:
        try:
                sleep(0.5)
        except KeyboardInterrupt:
                keypad.cleanup()
                print("Keypad Controller is interrupted")
                break
        except KeyboardInterrupt:
                ledThreadOff()
                threadDoor.do_run = False
                threadSensor.do_run = False
                print("\nFinish")
                break
            
            

    

