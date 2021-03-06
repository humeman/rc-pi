"""
utils/gpio.py

Contains controls for Pi GPIO pins.
"""

import RPi.GPIO as GPIO

from utils import exceptions

pins = {
    7: "PWMA",
    11: "AIN2",
    12: "AIN1",
    13: "STBY",
    15: "BIN1",
    16: "BIN2",
    18: "PWMB"
}

motors = {
    1: {
        "in1": 12,
        "in2": 11,
        "pwm": 7
    },
    2: {
        "in1": 15,
        "in2": 16,
        "pwm": 18
    }
}


def setup():
    GPIO.setmode(GPIO.BOARD)

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

    for motor in motors.values():
        motor["pwm"] = GPIO.PWM(motor["pwm"], 60)

def standby(state):
    if state:
        GPIO.output([x for x, y in pins.items() if y == "STBY"][0], GPIO.LOW)

    else:
        GPIO.output([x for x, y in pins.items() if y == "STBY"][0], GPIO.HIGH)

def set_motor(motor, state):
    m = motors[motor]
    
    if state == "forward":
        GPIO.output(m["in1"], GPIO.HIGH)
        GPIO.output(m["in2"], GPIO.LOW)

        #GPIO.output(m["pwm"], GPIO.HIGH)

    elif state == "backward": 
        GPIO.output(m["in1"], GPIO.LOW)
        GPIO.output(m["in2"], GPIO.HIGH)

        #GPIO.output(m["pwm"], GPIO.HIGH)

    elif state == "stop":
        # Reset all the pins
        for name, pin in m.items():
            if name != "pwm":
                GPIO.output(pin, GPIO.LOW)

    else:
        raise exceptions.InvalidState("State must be one of 'forward', 'backward', or 'stop'")

def set_pwm(motor, speed):
    m = motors[motor]

    m["pwm"].start(speed)

def stop():
    for pin, pin_type in pins.items():
        if "PWM" not in pin_type:
            GPIO.output(pin, GPIO.LOW)

        for motor in motors.values():
            motor["pwm"].stop()
        
def cleanup():
    GPIO.cleanup()
