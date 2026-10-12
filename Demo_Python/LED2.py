from gpiozero import LED
from time import sleep

red = LED(17)

while True:
    red.toggle()
    sleep(1)
