from gpiozero import LED, Button

led = LED(17)
button = Button(27)

while True:
    if button.is_pressed:
        led.on()
    else:
        led.off()
