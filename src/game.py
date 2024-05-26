import curses
import time
import RPi.GPIO as GPIO
import os
from lsm303d import LSM303D

PIN14 = 14
PIN15 = 15
PIN23 = 23
PIN24 = 24

LASER = 4
HZ = 1000

#set GPIO Pins
GPIO_TRIGGER = 20
GPIO_ECHO = 21
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def forward(pwm1, pwm2, speed):
    if pwm1 is not None and  pwm2 is not None:
        pwm1.stop()
        pwm2.stop()
    GPIO.output(PIN14, GPIO.LOW)
    GPIO.output(PIN15, GPIO.LOW)
    GPIO.output(PIN23, GPIO.LOW)
    GPIO.output(PIN24, GPIO.LOW)
    pwm1 = GPIO.PWM(PIN14, HZ)
    pwm2 = GPIO.PWM(PIN23, HZ)
    pwm1.start(speed)
    pwm2.start(speed)
    return pwm1, pwm2

def backward(pwm1, pwm2, speed):
    if pwm1 is not None and  pwm2 is not None:
        pwm1.stop()
        pwm2.stop()
    GPIO.output(PIN14, GPIO.LOW)
    GPIO.output(PIN15, GPIO.LOW)
    GPIO.output(PIN23, GPIO.LOW)
    GPIO.output(PIN24, GPIO.LOW)
    GPIO.output(PIN14, GPIO.LOW)
    GPIO.output(PIN23, GPIO.LOW)
    pwm1 = GPIO.PWM(PIN15, HZ)
    pwm2 = GPIO.PWM(PIN24, HZ)
    pwm1.start(speed)
    pwm2.start(speed)
    return pwm1, pwm2

def right(pwm1, pwm2, speed):
    if pwm1 is not None and  pwm2 is not None:
        pwm1.stop()
        pwm2.stop()
    GPIO.output(PIN14, GPIO.LOW)
    GPIO.output(PIN15, GPIO.LOW)
    GPIO.output(PIN23, GPIO.LOW)
    GPIO.output(PIN24, GPIO.LOW)
    GPIO.output(PIN15, GPIO.LOW)
    GPIO.output(PIN23, GPIO.LOW)
    pwm1 = GPIO.PWM(PIN14, HZ)
    pwm2 = GPIO.PWM(PIN24, HZ)
    pwm1.start(speed)
    pwm2.start(speed)
    return pwm1, pwm2

def left(pwm1, pwm2, spee)d:
    if pwm1 is not None and  pwm2 is not None:
        pwm1.stop()
        pwm2.stop()
    GPIO.output(PIN14, GPIO.LOW)
    GPIO.output(PIN15, GPIO.LOW)
    GPIO.output(PIN23, GPIO.LOW)
    GPIO.output(PIN24, GPIO.LOW)
    GPIO.output(PIN14, GPIO.LOW)
    GPIO.output(PIN24, GPIO.LOW)
    pwm1 = GPIO.PWM(PIN15, HZ)
    pwm2 = GPIO.PWM(PIN23, HZ)
    pwm1.start(speed)
    pwm2.start(speed)
    return pwm1, pwm2

def stop(pwm1, pwm2):
    if pwm1 is not None and  pwm2 is not None:
        pwm1.stop()
        pwm2.stop()
    GPIO.output(PIN14, GPIO.LOW)
    GPIO.output(PIN15, GPIO.LOW)
    GPIO.output(PIN23, GPIO.LOW)
    GPIO.output(PIN24, GPIO.LOW)
    pwm1 = None
    pwm2 = None
    return pwm1, pwm2

def update_laser(laser):
    if laser:
        GPIO.output(LASER, GPIO.HIGH)
    else:
        GPIO.output(LASER, GPIO.LOW)




def main(win):
    GPIO.cleanup()

    # Declare the GPIO settings
    GPIO.setmode(GPIO.BCM)

    # set up GPIO pins
    GPIO.setup(PIN14, GPIO.OUT)
    GPIO.setup(PIN15, GPIO.OUT)
    GPIO.setup(PIN23, GPIO.OUT)
    GPIO.setup(PIN24, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)

    GPIO.output(PIN14, GPIO.LOW)
    GPIO.output(PIN15, GPIO.LOW)

    GPIO.output(PIN23, GPIO.LOW)
    GPIO.output(PIN24, GPIO.LOW)
    GPIO.output(4, GPIO.LOW)

    win.nodelay(False)
    key = ""
    win.clear()
    win.addstr("Detected key:")
    pwm1 = None
    pwm2 = None


    laser = False
    speed = 50


    prev_action = None
    while True:
        action = 100000
        curses.flushinp()
        try:
            key = win.getkey()
            win.clear()
            win.addstr("Detected key:")
            win.addstr(str(key))
            if str(key)=='KEY_UP':
                action = 2
            elif str(key)=='KEY_DOWN':
                action = 1
            elif str(key) == 'KEY_LEFT':
                action = 4
            elif str(key)=='KEY_RIGHT':
                action = 3
            elif str(key)=='l':
                action = 10
            elif str(key)=='z':
                action = 25
            elif str(key)=='x':
                action = 26
            else:
                action = 5
        except Exception as e:
            win.addstr(str(e))
            action = 5
            continue            
        if action == 1 and action != prev_action:
            pwm1, pwm2 = forward(pwm1, pwm2, speed)
        elif action == 2 and action != prev_action :
            pwm1, pwm2 = backward(pwm1, pwm2, speed)
        elif action == 3 and action != prev_action :
            pwm1, pwm2 = right(pwm1, pwm2, speed)
        elif action == 4 and action != prev_action:
            pwm1, pwm2 = left(pwm1, pwm2, speed)
        elif action == 5:
            pwm1, pwm2 = stop(pwm1, pwm2)
        elif action == 25:
            speed += 5
            if speed > 100:
                speed = 100
            win.clear()
            win.addstr("Speed:")
            win.addstr(str(speed))
        elif action == 26:
            speed -= 5
            if speed < 20:
                speed = 20
            win.clear()
            win.addstr("Speed:")
            win.addstr(str(speed))
        elif action == 10:
            laser = not laser
            update_laser(laser)
        prev_action = action

curses.wrapper(main)
