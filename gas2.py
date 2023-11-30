from gpiozero import Button, LED, MCP3008, Servo
from math import sqrt
from time import sleep

# Raspberry Pi components
button = Button(27)
led = LED(22)
servo = Servo(17, min_pulse_width=0.5 / 1000, max_pulse_width=0.75 / 1000)

thermocouple = MCP3008(channel=0)

# Resistor values
r_k = 99.8  # Known resistor in series with thermocouple
r_0 = 100  # Resistance of thermocouple at 0 Degrees Celsius
r_w = 0.53  # Resistance of thermocouple wires

# Thermocouple parameters
a = 3.9083E-3
b = -5.775E-7


def start():
    servo.min()  # Gas on
    rate = 0
    prev_temp = 0

    while True:
        sleep(0.5)  # Sleep 0.5 seconds

        r_t = (thermocouple.value * r_k) / (1 - thermocouple.value)  # Thermocouple resistance
        r_f = r_t - r_w  # Thermocouple resistance excluding wires

        t_c = (-a + sqrt(a ** 2 - 4 * b * (1 - r_f / r_0))) / (2 * b)  # Temperature in Celsius
        t_f = 1.8 * t_c + 32  # Temperature in Fahrenheit

        print(f'Resistance: {r_t:.3f} Temperature: {t_f:.3f}')

        if t_f > prev_temp:
            if rate < 0:
                rate = 1
            else:
                rate += 1
        elif t_f < prev_temp:
            if rate > 0:
                rate = -1
            else:
                rate -= 1

        prev_temp = t_f

        if rate >= 10:
            led.on()
        elif rate <= -10:
            break

    servo.max()  # Gas off
    led.off()


if __name__ == "__main__":
    servo.max()  # Gas off
    button.when_pressed = start

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        servo.max()  # Gas off
        exit()
