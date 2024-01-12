import time
import RPi.GPIO as GPIO
import smbus2
import bme280
from flask import Flask, render_template

app = Flask(__name__)

address = 0x77

bus = smbus2.SMBus(1)

calib_params = bme280.load_calibration_params(bus, address)

def c2f(c):
    return (c*9/5)+32

def status():
    data = bme280.sample(bus, address, calib_params)
    temp = c2f(data.temperature)
    humi = data.humidity
    t = data.timestamp
    return (t, temp, humi)



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
def lights_on():
    light_gpio = 26
    GPIO.setup(light_gpio,GPIO.OUT)
    GPIO.output(light_gpio, True)
    print('lights on')
    return()
        
def lights_off():
    light_gpio = 26
    GPIO.setup(light_gpio,GPIO.OUT)
    GPIO.output(light_gpio, False)
    print('lights off')
    return()
        
#script that runs the greenhouse follows...

gh = 1
light_start = 18
light_time = light_start*60*60 #hours
sampling = 120 #secs
light_status = ''
print(status())
while gh > 0:
    timer = 0
    while timer < light_time:
        lights_on()
        light_status ='On'
        time.sleep(sampling)
        timer = timer + sampling
    light_time = light_time - 120
    lights_off_time = 24*60*60 - light_time
    timer = 0
    while timer < lights_off_time:
        lights_off()
        light_status = 'Off'
        time.sleep(sampling)
        timer = timer + sampling
    gh = gh + 1
    
    
@app.route('/')
def index():
    temperature = round(get_temp(),1)
    humidity = round(get_humi(),1)
    return render_template('index.html', temperature=temperature, humidity=humidity, lights=light_status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

