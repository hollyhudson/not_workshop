import time
import network
import secrets
from umqtt.simple import MQTTClient
from machine import Pin

########### global variables ##############################

mq = MQTTClient("led", "192.168.0.10")
my_led = Pin(0, Pin.OUT) # which pin your LED is connected to

########### get on the network ############################

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.essid, secrets.passwd) # your local wifi credentials

########## while waiting to connect to the network ###############

while not wlan.isconnected():
	time.sleep_ms(500)

wlan.ifconfig()

######### turning an LED on and off ##########################

def set_state(msg):
	if msg == b'on':
		my_led.on() 
	elif msg == b'off':
		my_led.off() 

################ MQTT Message switchboard #############################

# topics we recognize with their respective functions
subtopic = {
	b'my_led/state': set_state,
}

def handle_msg(topic,msg):
	# for debugging
	print("topic:'", topic, "' msg:'", msg, "'")

	if topic in subtopic:
		# call function associated with topic, passing message as parameter
		subtopic[topic](msg)
	else: 
		print("topic not recognized")

######## MQTT Client: starting, connecting, and subscribing ##########

# start the MQTT client for this microcontroller
mq.set_callback(handle_msg) # handle_msg() is called for ALL messages received
mq.connect()
mq.subscribe(b"my_led/#") 

# wait for messages forever
# when one is received the function we passed to set_callback() will be run
while True:
	mq.wait_msg()
