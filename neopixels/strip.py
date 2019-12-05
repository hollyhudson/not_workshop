# Template file for NeoPixel patterns

import time
import network
import secrets
import urandom
from umqtt.simple import MQTTClient
from machine import Pin
from neopixel import NeoPixel

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.essid, secrets.passwd) # your local wifi credentials

NUM_PIXELS = 7
# NeoPixel(Pin([pin number], Pin.OUT), [number of pixel])
np = NeoPixel(Pin(0, Pin.OUT), NUM_PIXELS) 

# red, green, and blue values for the leds
r, g, b = 0, 0, 0
pattern_r, pattern_g, pattern_b = 0, 0, 0
on = False
pattern_on = False
counter = []

# the only random function in micropython is urandom.getrandbits()
# and you can't do pattern mode without a little randomness
def random(low,high):
	result = int(low + urandom.getrandbits(8) * (high - low) / 256)
	return result

# keep trying to connect to the wifi until we suceed
while not wlan.isconnected():
        np.fill((10,0,0))
        np.write()
        time.sleep_ms(200)
        np.fill((0,0,0))
        np.write()
        time.sleep_ms(300)
np.fill((0,0,10))
np.write()

wlan.ifconfig()

def pattern():
	global pattern_r, pattern_g, pattern_b

	for i in range(NUM_PIXELS):
		# after the LED has been lit for some time, change it's color
		if counter[i] == 0:
			counter[i] == random(100,500)
			# pick a very random new color for the LED
			if random(0,2) == 0:
				pattern_r = random(0,50)
			else:
				pattern_r = 0	
			if random(0,2) == 0:
				pattern_g = random(0,50)
			else:
				pattern_g = 0	
			if random(0,2) == 0:
				pattern_b = random(0,50)
			else:
				pattern_b = 0	

			np[i] = (pattern_r, pattern_g, pattern_b)
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

def set_pattern(msg):
	global pattern_on
	
	if msg == b'off':
		pattern_on = False
		all_off()
	
	elif msg == b'on':
		global counter

		pattern_on = True

		#start with a fresh pattern
		counter.clear()
		for i in range(NUM_PIXELS):
			counter.append(random(100,500))

# topics we recognize with their respective functions
subtopic = {
	b'led/color': set_color,
	b'led/state': set_state,
	b'led/pattern': set_pattern,
}

def handle_msg(topic,msg):
	print("topic:'", topic, "' msg:'", msg, "'")
	
	if topic in subtopic:
		# call function associated with topic, passing message as parameter
		subtopic[topic](msg)	
	else:
		print("topic not recognized")

# start the MQTT client for this microcontroller
mq = MQTTClient("neo", "192.168.0.10")
mq.set_callback(handle_msg) # handle_msg is called for ALL messages received
mq.connect()
mq.subscribe(b"led/#") # specify the topic to subscribe to (led in this case)

# wait for messages forever
# when one is received the function we passed to set_callback() will be run
other_counter = 0
while True:
	if pattern_on == True:
		pattern()
	mq.check_msg()


