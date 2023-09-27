from gpiozero import Servo
from time import sleep

servo = Servo(17, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

while True:
    servo.min()
    sleep(2)
    servo.mid()
    sleep(2)
    servo.max()
    sleep(2)
