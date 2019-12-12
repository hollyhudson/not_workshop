import time
import network
import secrets
import urandom
from config import config
from ubinascii import hexlify
from umqtt.simple import MQTTClient
from machine import Pin
from neopixel import NeoPixel

########### global variables ##############################

pins  = {
    'pixel': 0,
    'num_pixels': 7,
}

mq = MQTTClient(config["mqtt_client"], config["mqtt_broker"])
np = NeoPixel(Pin(pins["pixel"], Pin.OUT), pins["num_pixels"])

# red, green, and blue values for the leds
r, g, b = 0, 0, 0
disco_r, disco_g, disco_b = 0, 0, 0
on = False
discoing = False
counter = []

######### helper functions ###############################

# the only random function in micropython is urandom.getrandbits()
# and you can't do disco mode without a little randomness
def random(low,high):
	result = int(low + urandom.getrandbits(8) * (high - low) / 256)
	return result

######### LED control functions ##########################

def disco_pattern():
	global disco_r, disco_g, disco_b

	for i in range(NUM_PIXELS):
		# after the LED has been lit for some time, change it's color
		if counter[i] == 0:
			counter[i] == random(100,500)
			# pick a very random new color for the LED
			if random(0,2) == 0:
				disco_r = random(0,50)
			else:
				disco_r = 0	
			if random(0,2) == 0:
				disco_g = random(0,50)
			else:
				disco_g = 0	
			if random(0,2) == 0:
				disco_b = random(0,50)
			else:
				disco_b = 0	

			np[i] = (disco_r, disco_g, disco_b)
		else:
			counter[i] = counter[i] - 1

	np.write()	

def all_off():
	np.fill((0,0,0))
	np.write()

def all_on():
	np.fill((int(r),int(g),int(b)))
	np.write()

def set_color(msg):
	global r, g, b
	r, g, b = msg.split(b',')
	all_on()

def set_state(msg):
	global on

	if msg == b'on':
		on = True	
		all_on()

	elif msg == b'off':
		on = False
		all_off()

def set_disco(msg):
	global discoing
	
	if msg == b'off':
		discoing = False
		all_off()
	
	elif msg == b'on':
		global counter

		discoing = True

		#start with a fresh pattern
		counter.clear()
		for i in range(NUM_PIXELS):
			counter.append(random(100,500))

################ MQTT Message switchboard #############################

# topics we recognize with their respective functions
subtopic = {
	b'pixels/color': set_color,
	b'pixels/set': set_state,
	b'pixels/disco': set_disco,
}

def handle_msg(topic,msg):
	print("topic:'", topic, "' msg:'", msg, "'")
	
	if topic in subtopic:
		# call function associated with topic, passing message as parameter
		subtopic[topic](msg)	
	else:
		print("topic not recognized")

######## MQTT Client: starting, connecting, and subscribing ##########

# start the MQTT client for this microcontroller
mq.set_callback(handle_msg) # handle_msg is called for ALL messages received
mq.connect()
mq.subscribe(b"pixels/#") # specify the topic to subscribe to (led in this case)

# wait for messages forever
# when one is received the function we passed to set_callback() will be run
other_counter = 0
while True:
	if discoing == True:
		disco_pattern()
	mq.check_msg()


