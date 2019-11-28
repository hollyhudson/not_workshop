# Pulsating pattern

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

NUM_PIXELS = 24
# NeoPixel(Pin([pin number], Pin.OUT), [number of pixel])
np = NeoPixel(Pin(15, Pin.OUT), NUM_PIXELS) 
onboard_led = Pin(0, Pin.OUT)

# red, green, and blue values for the leds
r, g, b = 0, 0, 0
pattern_r, pattern_g, pattern_b = 0, 0, 0
on = False
pattern_on = False
stay_black = []
directions = []
brightness = []
pink = []

# the only random function in micropython is urandom.getrandbits()
# and you can't do pattern mode without a little randomness
def random(low,high):
	result = int(low + urandom.getrandbits(8) * (high - low) / 256)
	return result

# keep trying to connect to the wifi until we succeed
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
	global brightness, directions, stay_black

	for i in range(NUM_PIXELS):
		if brightness[i] == 0:
			# after the LED has been lit for some time, 
			# put it in dormant mode
			if stay_black[i] == 0:

				# reset the stay_black counter for next time
				stay_black[i] == random(100,5000)
				
				directions[i] = 1
				brightness = 1

				# pick a new color for the led
				if random(0,2) == 0:
					# pink mode
					pink[i] = True 
					pattern_r = 10
					pattern_g = 0
					pattern_b = 3
				else:
					# orange mode
					pink[i] = False
					pattern_r = 5
					pattern_g = 10
					pattern_b = 10
			else:
				# stay_black counter is still running, decrement
				stay_black[i] = stay_black[i] - 1

		else:
			# pixel is going up or down, not at zero
			brightness[i] = brightness[i] + directions[i]
			# change direction at some point
			max_brightness = 40
			min_brightness = 20
			if brightness[i] == max_brightness:
				directions[i] = -1;
			# set the r, g, and b based on new brightness and direction
			if pink == True:
				# pink mode	
				pattern_r = brightness[i]
				pattern_g = 0
				pattern_b = brightness[i]/3
			else:
				# orange mode
				pattern_r = brightness[i]
				pattern_g = brightness[i]/5
				pattern_b = 0

		np[i] = (pattern_r, pattern_g, pattern_b)

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
		global directions, brightness 

		pattern_on = True

		#start with a fresh pattern
		for i in range(NUM_PIXELS):
			directions[i] = 1
			brightness[i] = 0
			
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


