import time
import network
import secrets
from umqtt.simple import MQTTClient
from machine import Pin

########### global variables ##############################

on = False # is the led on?

########### get on the network ############################

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.essid, secrets.passwd) # your local wifi credentials

########## while waiting to connect to the network ###############

while not wlan.isconnected():
	time.sleep_ms(500)

wlan.ifconfig()

########## example function ##############################

def set_color(msg):
	global r, g, b
	r, g, b = msg.split(b',')
	np.fill((int(r),int(g),int(b)))
	np.write()

########## example function ##############################

def set_state(msg):
	global on
	global r, g, b
	if msg == b'on':
		on = True	
		np.fill((int(r),int(g),int(b)))
		np.write()
		
	elif msg == b'off':
		on = False
		np.fill((0,0,0))
		np.write()

################ MQTT Message switchboard #############################

# topics we recognize and the function to call for that topic
subtopic = {
	b'led_panel/color': set_color,
	b'led_panel/state': set_state,
}

# Decides which function to call for each message
def handle_msg(topic,msg):

	# for debugging
	print("topic:'", topic, "' msg:'", msg, "'")

	if topic in subtopic:
		# call the function for the topic, with the message as parameter
		subtopic[topic](msg)
	else:
		print("topic not recognized")


######## MQTT Client: starting, connecting, and subscribing ##########

# (client_id, client_ip_address), client_id must be unique
mq = MQTTClient("neo_button", "192.168.0.23")
mq.set_callback(handle_msg) # handle_msg() will be called for ALL messages received
mq.connect()
mq.subscribe(b"led_panel/#")

# wait for MQTT messages forever
# when one is received the function we passed to set_callback() will be run
while True:
	mq.check_msg()

######### Publishing an MQTT message ########################

# Code involving publishing must come after the client is declared

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
