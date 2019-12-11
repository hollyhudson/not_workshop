import time
import network
from ubinascii import hexlify
from umqtt.simple import MQTTClient
from machine import Pin,PWM

########### global variables ##############################

unique_ID = hexlify(network.WLAN().config('mac'))

def config  = {
    'mqtt_broker': '192.168.0.12',  # central server for our mqtt network
    'mqtt_client': unique_ID, # this device client ID
    'led_pin': 0,
    'button_pin': 13,
}

mq = MQTTClient(config.mqtt_client, config.mqtt_broker)
led = Pin(config.led_pin, Pin.OUT)
button = Pin(config.button_pin, Pin.IN, Pin.PULL_UP)

pwm_led = PWM(led)

######### turning an LED on and off ##########################

def set_state(msg):
	if msg == b'on':
		pwm_led.duty(500) # 0-1023, 512 is 50% brightness
	elif msg == b'off':
		pwm_led.duty(0) 

def set_dim(msg):
	pwm_led.duty(msg) # 0-1023, 512 is 50% brightness

################ MQTT Message switchboard #############################

# topics we recognize with their respective functions
subtopic = {
	b'led/set': set_state,
	b'led/dim': set_state,
}

def handle_msg(topic,msg):
	# for debugging
	print("topic: ", topic, " msg: ", msg)

	if topic in subtopic:
		# call function associated with topic, passing message as parameter
		subtopic[topic](msg)
	else: 
		print("topic not recognized")

######## MQTT Client: starting, connecting, and subscribing ##########

# start the MQTT client for this microcontroller
mq.set_callback(handle_msg) # handle_msg() is called for ALL messages received
mq.connect()
mq.subscribe(b"led/#") 

# wait for messages forever
# when one is received the function we passed to set_callback() will be run
while True:
	mq.wait_msg()
