import time
import network
import secrets
from umqtt.simple import MQTTClient
from machine import Pin
from neopixel import NeoPixel

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.essid, secrets.passwd) # your local wifi credentials

NUM_PIXELS = 32
# NeoPixel(Pin([pin number], Pin.OUT), [number of pixel])
np = NeoPixel(Pin(15, Pin.OUT), NUM_PIXELS) 

# keep trying to connect to the wifi until we suceed
while not wlan.isconnected():
        np.fill((10,0,0))
        np.write()
        time.sleep_ms(200)
        np.fill((0,0,0))
        np.write()
        time.sleep_ms(300)

wlan.ifconfig()

def set_led(topic,msg):
        print("topic:'", topic, "' msg:'", msg, "'")
        np.fill((int(msg),int(msg),int(msg)))
        np.write()
		# if topic == button or if topic == led
		# do something with msg

# start the MQTT client for this microcontroller
mq = MQTTClient("neo", "192.168.0.23")
mq.set_callback(set_led) # set_led will be called for ALL messages received
mq.connect()
mq.subscribe(b"led") # specify the topic to subscribe to (led in this case)

# wait for messages forever
# when one is received the function we passed to set_callback() will be run
while True:
        mq.wait_msg()
