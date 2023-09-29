import threading
from time import sleep
from gpiozero import Servo, Button

# global status
status = False


def pressed():
    global status
    status = not status


def servo_control():
    servo = Servo(17, min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000)
    global status
    while True:
        sleep(16 / 1000)
        if status:
            servo.min()
        else:
            servo.max()


if __name__ == "__main__":
    button = Button(23)
    button.when_pressed = pressed

    # Create Thread for servo control
    servo_thread = threading.Thread(target=servo_control)

    # Set Thread to run in background
    servo_thread.setDaemon(True)

    # Start Thread
    servo_thread.start()

    # Wait for thread to complete (it should not)
    servo_thread.join()
