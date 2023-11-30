import threading
from time import sleep
from gpiozero import Button, Servo

status = False
button = Button(27)
servo1 = Servo(2, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
servo2 = Servo(3, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

def pressed():
    global status
    status = not status
    print("Pressed")


def servo_control():
    global status
    while True:
        sleep(16/1000)
        if status:
            servo1.min()
            servo2.min()
        else:
            servo1.max()
            servo2.max()


if __name__ == "__main__":
    servo1.min()
    servo2.min()
    button.when_pressed = pressed
    
    servo_thread = threading.Thread(target = servo_control)
    servo_thread.setDaemon(True)
    servo_thread.start()
    servo_thread.join()
