from gpiozero import LED
from signal import pause

red = LED(22)


red.blink(on_time=1/2, off_time=1/2)
pause()
