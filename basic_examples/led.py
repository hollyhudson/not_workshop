# Code for an LED and a button on the ESP board
# press the button, the LED comes on, all local control, no MQTT

import time
from machine import Pin

########### global variables ##############################

button = Pin(13, Pin.IN, Pin.PULL_UP) # which pin your LED is connected to
led = Pin(0, Pin.OUT) # which pin your LED is connected to

######## MQTT Client: starting and connecting ##########
########## publishing an MQTT message ###############

########## main programming loop ###############

# code for momentary switch behavior, toggle behavior is below
# Since this is in the top-level while True loop, it's the default behavior
last_button_value = True # not pressed

while True:
	button_value = button.value()

	if last_button_value == button_value:
		continue

	last_button_value = button_value

	if not button_value:
		print("pressed!!!!!")
		led.on()
	else:
		print("not pressed")
		led.off()
	
	time.sleep(0.1)

# below is the code for toggle behavior
# to use run led.toggle() in the webrepl
def toggle():
	last_button_value = True # not pressed
	led_on = False # is the LED on?

	while True:
		button_value = button.value()
	
		if last_button_value == button_value:
			continue

		last_button_value = button_value
		
		if button_value:
			# button was released/unpressed
			print("button was released")
			continue
	
		led_on = not led_on
		print("pressed!!!!!")
		if led_on:
			led.on()
		else:
			led.off()
	
		time.sleep(0.1)
