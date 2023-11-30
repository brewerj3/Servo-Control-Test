import threading
from time import sleep
from gpiozero import Button, LED, MCP3008, Servo

status = False
thermocouple = MCP3008(channel = 0)
led = LED(22)

def pressed():
    global status
    status = True


def servo_control():
    global status
    servo = Servo(17, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    count = 0

    if(status):
        servo.max()
        while(True):
            sleep(100/1000)
            if(count == 10):
                print("Hello")
                count = 0
            else:
                count = count + 1



if __name__ == "__main__":
    button = Button(27)
    button.when_pressed = pressed

    servo_thread = threading.Thread(target = servo_control)
    servo_thread.setDaemon(True)
    servo_thread.start()
    servo_thread.join()
