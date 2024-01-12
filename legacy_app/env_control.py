import time
import RPi.GPIO as GPIO
import smbus2
import bme280

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
    gpio_control = 16
    GPIO.setup(gpio_control, GPIO.OUT)
    GPIO.output(gpio_control, GPIO.HIGH)
    print('heater on')
    
def stop_heater():
    gpio_control = 16
    GPIO.setup(gpio_control, GPIO.OUT)
    GPIO.output(gpio_control, GPIO.LOW)
    print('heater off')
    
def run_humid(target):
    gpio_control = 5
    GPIO.setup(gpio_control, GPIO.OUT)
    GPIO.output(gpio_control, GPIO.HIGH)
    print('humid on')
    
def stop_humid():
    gpio_control = 5
    GPIO.setup(gpio_control, GPIO.OUT)
    GPIO.output(gpio_control, GPIO.LOW)
    print('humid off')

def env_control(t, h):
    tim, tem, hum = status()
    print(tem, hum)
    print(t, h)
    if tem < t-5:
        run_heater(t+5)
        if hum < h-5:
            run_humid(h+5)
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

temp = 75
humi = 50
t = 1
while t>0:
    env_control(temp, humi)
    t = t+1
    time.sleep(60)