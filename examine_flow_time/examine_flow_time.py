from time import sleep
from buildhat import Motor

motor = Motor('A')
motor.on()
motor.stop()

motor.run_for_degrees(135, speed=35)
sleep(0.1)
motor.run_for_degrees(-135, speed=35)
