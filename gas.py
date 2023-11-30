from time import sleep
from gpiozero import Button, LED, MCP3008, Servo

button = Button(27)
led = LED(22)
servo = Servo(17, min_pulse_width=0.5/1000, max_pulse_width=0.75/1000)
thermocouple = MCP3008(channel = 0)

def control():
    print("Pressed")
    servo.min() # Turn gas valve on

    rate = 0
    prev_temp = 0

    while True:
        sleep(0.5)
        print(rate)

        if thermocouple.value > prev_temp:
            if rate < 0:
                rate = 1
            else:
                rate += 1
        elif thermocouple.value < prev_temp:
            if rate > 0:
                rate = -1
            else:
                rate -= 1

        prev_temp = thermocouple.value

        if rate >= 10:
            led.on()
        elif rate <= -10:
            break

    print("Done")
    servo.max() # Turn gas valve off
    led.off()


if __name__ == "__main__":
    servo.max() # Turn gas valve off
    button.when_pressed = control

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        servo.max() # Turn gas valve off
        exit()
