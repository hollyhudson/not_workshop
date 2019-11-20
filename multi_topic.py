import time
import network
import secrets
from umqtt.simple import MQTTClient
from machine import Pin
from neopixel import NeoPixel

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.essid, secrets.passwd) # your local wifi credentials

np = NeoPixel(Pin(15, Pin.OUT), 32) # which pin your NeoPixels are connected to

# red, green, and blue values for the leds
r, g, b = 0, 0, 0
on = False

# keep trying to connect to the wifi until we suceed
while not wlan.isconnected():
	np.fill((10,0,0))
	np.write()
	time.sleep_ms(200)
	np.fill((0,0,0))
	np.write()
	time.sleep_ms(300)

wlan.ifconfig()

def set_color(msg):
	global r, g, b
	r, g, b = msg.split(b',')
	np.fill((int(r),int(g),int(b)))
	np.write()

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

# topics we recognize with their respective functions
subtopic = {
	b'led_panel/color': set_color,
	b'led_panel/state': set_state,
}

def handle_msg(topic,msg):
	global r, g, b
	print("topic:'", topic, "' msg:'", msg, "'")

	if topic in subtopic:
		# call the function for the topic, with the message as parameter
		subtopic[topic](msg)
	else:
		print("topic not recognized")


# start the MQTT client for this microcontroller
mq = MQTTClient("neo", "192.168.0.23")
mq.set_callback(handle_msg) # handle_msg will be called for ALL messages received
mq.connect()
mq.subscribe(b"led_panel/#") # specify the topic to subscribe to (led in this case)

# wait for messages forever
# when one is received the function we passed to set_callback() will be run
while True:
	mq.check_msg()
