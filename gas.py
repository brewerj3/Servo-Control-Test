from gpiozero import Button, LED, MCP3008, Servo
from math import sqrt
from time import sleep
from signal import pause

# Raspberry Pi components
button = Button(27)
led = LED(22)
servo = Servo(17, min_pulse_width=0.5 / 1000, max_pulse_width=0.875 / 1000)
thermocouple = MCP3008(channel=0)

# Resistor values
r_k = 99.8  # Known resistor in series with thermocouple
r_0 = 100  # Resistance of thermocouple at 0 Degrees Celsius
r_w = 0.53  # Resistance of thermocouple wires

# Thermocouple parameters
a = 3.9083E-3
b = -5.775E-7

# Array parameters
length = 10


def get_temperature():
    r_t = (thermocouple.value * r_k) / (1 - thermocouple.value)  # Thermocouple resistance
    r_f = r_t - r_w  # Thermocouple resistance excluding wires
    t_c = (-a + sqrt(a ** 2 - 4 * b * (1 - r_f / r_0))) / (2 * b)  # Temperature in Celsius
    t_f = 1.8 * t_c + 32  # Temperature in Fahrenheit
    return round(t_f, 3)


def start():
    servo.min()  # Gas on

    # Initial setup
    temperature = get_temperature()
    temps = [temperature for i in range(length)]
    average_temp = temperature
    prev_average_temp = temperature
    rates = [0 for i in range(length)]
    average_rate = 0
    prev_average_rate = 0
    i = 0
    lit = False
    count = 0

    while True:
        sleep(0.2)  # Sleep 0.5 seconds

        temps[i] = get_temperature()
        prev_average_temp = average_temp
        average_temp = round(sum(temps) / length, 3)
        rates[i] = round(average_temp - prev_average_temp, 3)
        prev_average_rate = average_rate
        average_rate = round(sum(rates) / length, 3)

        i = (i + 1) % length

        if not lit:
            count += 1

        if average_rate > 1:
            led.on()
            lit = True
        elif lit and average_rate - prev_average_rate < -0.2:
            break
        elif count > 25:  # If not lit within 5 seconds, turn off gas
            break

        if i % 5 != 0:
            continue

        print(f'Average Rate: {average_rate} Rates: {rates}')
        print(f'Average Temp: {average_temp} Temps: {temps}')
        print()

    servo.max()  # Gas off
    led.off()


if __name__ == "__main__":
    servo.max()  # Gas off
    button.when_pressed = start

    try:
        pause()
    except KeyboardInterrupt:
        servo.max()  # Gas off
        exit()
