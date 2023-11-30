from math import sqrt
from gpiozero import MCP3008
from time import sleep

r_0 = 100
r_k = 99.8
r_w = 0.57
a = 3.9083E-3
b = -5.775E-7

thermocouple = MCP3008(channel = 0)

while True:
    sleep(1)
    r_t = (thermocouple.value * r_k) / (1 - thermocouple.value)
    r_f = r_t - r_w
    t_c = (-a + sqrt(a ** 2 - 4 * b * (1 - r_f/r_0))) / (2 * b)
    t_f = 1.8 * t_c + 32
    print(f'Resistance (Ohms): {r_f:.3f} Temperature (Fahrenheit): {t_f:.3f}')
