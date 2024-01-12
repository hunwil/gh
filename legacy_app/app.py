import time
import RPi.GPIO as GPIO
import smbus2
import bme280
from flask import Flask, render_template

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
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

def get_humi():
    data = bme280.sample(bus, address, calib_params)
    humi = data.humidity
    return humi

def get_temp():
    data = bme280.sample(bus, address, calib_params)
    temp = c2f(data.temperature)
    return temp

def run_heater(target):
    gpio_control = 13
    GPIO.setup(gpio_control, GPIO.OUT)
    GPIO.output(gpio_control, GPIO.HIGH)
    
def stop_heater():
    gpio_control = 13
    GPIO.setup(gpio_control, GPIO.OUT)
    GPIO.output(gpio_control, GPIO.LOW)
    
def run_humid(target):
    gpio_control = 5
    GPIO.setup(gpio_control, GPIO.OUT)
    GPIO.output(gpio_control, GPIO.HIGH)
    
def stop_humid():
    gpio_control = 5
    GPIO.setup(gpio_control, GPIO.OUT)
    GPIO.output(gpio_control, GPIO.LOW)
    

def env_control(t, h):
    tim, tem, hum = status()
    print(tem, hum)
    print(t, h)
    if tem < t-5:
        run_heater(t+5)
        print('heater on')
        if hum < h-5:
            run_humid(h+5)
            print('hum on')
        elif hum > h+5:
            stop_humid()        
    elif hum < h-5:
        run_humid(h+5)
        if tem > (t+5):
            stop_heater()
    elif hum > h+5:
            stop_humid()
    elif tem > t+5:
        stop_heater()
    
    else:
        return()


def lights_on():
    light_gpio = 26
    GPIO.setup(light_gpio,GPIO.OUT)
    GPIO.output(light_gpio, GPIO.HIGH)
    return()
        
def lights_off():
    light_gpio = 26
    GPIO.setup(light_gpio,GPIO.OUT)
    GPIO.output(light_gpio, GPIO.LOW)
    return()



@app.route('/')
def index():
    temperature = round(get_temp(),1)
    humidity = round(get_humi(),1)
    return render_template('index.html', temperature=temperature, humidity=humidity)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
#script that runs the greenhouse follows...

    

