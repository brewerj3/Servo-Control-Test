from gpiozero import Button, Servo
from time import sleep
from signal import pause

status = False
button = Button(22)
servo1 = Servo(17, min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000)
servo2 = Servo(27, min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000)


def control():
    global status
    sleep(0.5)

    if status:
        servo1.max()
        servo2.max()
    else:
        servo1.min()
        servo2.min()

    status = not status


if __name__ == "__main__":
    servo1.min()
    servo2.min()
    button.when_pressed = control

    try:
        pause()
    except KeyboardInterrupt:
        servo1.min()
        servo2.min()
        sleep(1)
        exit()
