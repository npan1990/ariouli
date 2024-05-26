from gpiozero import Servo
from time import sleep

servo = Servo(17)

try:
	while True:
		for i in range(-100,100,1):
			servo.value = i*0.01
			sleep(0.05)
except KeyboardInterrupt:
	print("Program stopped")
