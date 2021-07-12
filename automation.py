import time
from flask import Flask, render_template
import pywemo
import serial
import os.path
from os import path

deviceName = "<device name>"
#devices = ""
#devices = pywemo.discover_devices()

address = "<wemo ip address>"
port = pywemo.ouimeaux_device.probe_wemo(address)
url = 'http://%s:%i/setup.xml' % (address, port)

class WemoSwitch:
    def __init__(self, deviceName):
        self.name = deviceName
    def FindDevice(self):
        #for i in range(len(devices)):
            #if devices[i].name == self.name:
            return pywemo.discovery.device_from_description(url, None)

state_dict = {
    1:"on",
    0:"off"
}

if path.exists('/dev/ttyACM0'):
    ser=serial.Serial('/dev/ttyACM0', 9600)
    print(f'found /dev/ttyACM0')
else:
    ser=serial.Serial('/dev/ttyACM1', 9600)
    print(f'found /dev/ttyACM1')

def SendIRPower():
    ser.write(b'1')
    arduinoLine = ser.readline()
    print(arduinoLine)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Home Automation Web Server Online'

@app.route('/wemo/<state>')
def wemo_power(state):
    Switch = WemoSwitch(deviceName).FindDevice()
    if state =='on':
        if Switch.get_state() == 0:
            print(Switch.name)
            Switch.on()
            time.sleep(15)
            SendIRPower()
            print(f'{deviceName} state is {state}')
            return f"wemo state is {state}"
    if state =='off':
        print(Switch.name)
        Switch.off()
        print(f'{deviceName} state is {state}')
        return f"wemo state is {state}"
    if state =='toggle':
        print(Switch.name)
        Switch.toggle()
        time.sleep(15)
        SendIRPower()
        state = Switch.get_state()
        print(f'{deviceName} state is {state_dict[state]}')
        return f"wemo state is {state_dict[state]}"
    if state =='ir':
        SendIRPower()
        print(f'IR signal sent')
        return f"IR signal sent"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)