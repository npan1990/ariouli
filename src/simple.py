import curses
import time
import RPi.GPIO as GPIO
import os
import threading
from lsm303d import LSM303D


PIN14 = 14
PIN15 = 15
PIN23 = 23
PIN24 = 24

LASER = 22
HZ = 1000
LED = 12

TOY = 25


def right(pwm1, pwm2, speed):
    local_speed = 90
    if pwm1 is not None and  pwm2 is not None:
        pwm1.stop()
        pwm2.stop()
    GPIO.output(PIN14, GPIO.LOW)
    GPIO.output(PIN15, GPIO.LOW)
    GPIO.output(PIN23, GPIO.LOW)
    GPIO.output(PIN24, GPIO.LOW)
    pwm1 = GPIO.PWM(PIN14, HZ)
    pwm2 = GPIO.PWM(PIN23, HZ)
    pwm1.start(local_speed)
    pwm2.start(local_speed)
    return pwm1, pwm2

def left(pwm1, pwm2, speed):
    local_speed = 90
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
    pwm1.start(local_speed)
    pwm2.start(local_speed)
    return pwm1, pwm2

def forward(pwm1, pwm2, speed):
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

def backward(pwm1, pwm2, speed):
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

def update_light(light):
    if light:
        print('OK')
        GPIO.output(LED, GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)

def change_toy(toy):
    if toy:
        GPIO.output(TOY, GPIO.HIGH)
    else:
        GPIO.output(TOY, GPIO.LOW)


GPIO.cleanup()

# Declare the GPIO settings
GPIO.setmode(GPIO.BCM)

# set up GPIO pins
GPIO.setup(PIN14, GPIO.OUT)
GPIO.setup(PIN15, GPIO.OUT)
GPIO.setup(PIN23, GPIO.OUT)
GPIO.setup(PIN24, GPIO.OUT)
GPIO.setup(LASER, GPIO.OUT)
GPIO.setup(TOY, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)

GPIO.output(PIN14, GPIO.LOW)
GPIO.output(PIN15, GPIO.LOW)

GPIO.output(PIN23, GPIO.LOW)
GPIO.output(PIN24, GPIO.LOW)
GPIO.output(LASER, GPIO.LOW)




curses.filter()




def main(win):
    measurements = []
    

    win.nodelay(False)
    key = ""
    win.clear()
    win.addstr("Detected key:")
    pwm1 = None
    pwm2 = None


    laser = False
    speed = 50
    light = False


    prev_action = None
    toy = False
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
            elif str(key)=='q':
                action = 20
            elif str(key)=='z':
                action = 25
            elif str(key)=='x':
                action = 26
            elif str(key)=='t':
                action = 7
            else:
                action = 5
        except Exception as e:
            print(e)
            action = 5
            continue            
        if action == 1 and action != prev_action:
            pwm1, pwm2 = stop(pwm1, pwm2)
            pwm1 = None
            pwm2 = None
            pwm1, pwm2 = forward(pwm1, pwm2, speed)
        elif action == 2 and action != prev_action :
            pwm1, pwm2 = stop(pwm1, pwm2)
            pwm1 = None
            pwm2 = None
            pwm1, pwm2 = backward(pwm1, pwm2, speed)
        elif action == 3 and action != prev_action :
            local_speed = speed - 10
            pwm1, pwm2 = stop(pwm1, pwm2)
            pwm1 = None
            pwm2 = None
            pwm1, pwm2 = right(pwm1, pwm2, local_speed)
        elif action == 4 and action != prev_action:
            local_speed = speed - 10
            pwm1, pwm2 = stop(pwm1, pwm2)
            pwm1 = None
            pwm2 = None
            pwm1, pwm2 = left(pwm1, pwm2, local_speed)
        elif action == 5:
            pwm1, pwm2 = stop(pwm1, pwm2)
            if len(measurements) > 2:
                acc = []
                for measurement in measurements:
                    if measurement[1] > 50:
                        acc.append(measurement[1]*100*9.8)
                    else:
                        acc.append(0)
                dt = measurements[-1][0] - measurements[0][0]
                acc = sum(acc)/len(acc)
                x=1/2*acc*dt*dt
                v = acc*dt

        elif action == 25:
            speed += 5
            if speed > 100:
                speed = 100
            win.clear()
            win.addstr("Speed:")
            win.addstr(str(speed))
        elif action == 7:
            toy = not toy
            change_toy(toy)
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
        elif action == 20:
            light = not light
            update_light(light)
        prev_action = action

curses.wrapper(main)
