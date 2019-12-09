import time
import network
from umqtt.simple import MQTTClient
from machine import Pin

########### global variables ##############################

mq = MQTTClient("button", "192.168.0.10")
button = Pin(14, Pin.IN, Pin.PULL_UP) # which pin your LED is connected to

########### get on the network ############################

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.essid, secrets.passwd) # your local wifi credentials

########## while waiting to connect to the network ###############

while not wlan.isconnected():
	time.sleep_ms(500)

wlan.ifconfig()

######## MQTT Client: starting and connecting ##########

# start the MQTT client for this microcontroller
mq.connect()

########## publishing an MQTT message ###############

def momentary():
	last_button_value = True # not pressed

	while True:
		button_value = button.value()
	
		if last_button_value == button_value:
			continue

		last_button_value = button_value

		if not button_value:
			print("pressed!!!!!")
			mq.publish(topic="my_led/state", msg="on")
		else:
			print("not pressed")
			mq.publish(topic="my_led/state", msg="off")
	
		time.sleep(0.1)

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
			mq.publish(topic="my_led/state", msg="on")
		else:
			mq.publish(topic="my_led/state", msg="off")
	
		time.sleep(0.1)
