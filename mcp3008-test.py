from gpiozero import MCP3008

thermocouple = MCP3008(channel=0)
known_res = 99.8
calc_res = known_res / (1 - thermocouple.value)

while True:
    print(thermocouple.value)
    # print(calc_res)

