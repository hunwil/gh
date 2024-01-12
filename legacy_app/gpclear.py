import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

gpio_a = 5
gpio_b = 26
gpio_c = 16
GPIO.setup(gpio_a, GPIO.OUT)
GPIO.setup(gpio_b, GPIO.OUT)
GPIO.setup(gpio_c, GPIO.OUT)

GPIO.output(gpio_a, False)
GPIO.output(gpio_b, False)
GPIO.output(gpio_c, False)
GPIO.cleanup()