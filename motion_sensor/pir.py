import time
import network
from ubinascii import hexlify
from umqtt.simple import MQTTClient
from machine import Pin

########### global variables ##############################

unique_ID = hexlify(network.WLAN().config('mac'))

def config  = {
    'mqtt_broker': '192.168.0.12',  # central server for our mqtt network
    'mqtt_client': unique_ID, # this device client ID
    'pin': 0, # which pin the pir sensor is on
}

mq = MQTTClient(config.mqtt_client, config.mqtt_broker)
pir = Pin(config.pin, Pin.IN)

######## MQTT Client: starting, connecting, and subscribing ##########

mq.connect()

######### Publishing an MQTT message ########################

# Code involving publishing must come after the client is declared

last_pir_value = False

# edge-triggered (detects when value changes state)
while True:
	new_pir_value = pir.value()

	if last_pir_value == new_pir_value:
		continue
	
	last_pir_value = new_pir_value	
	
	if new_pir_value:
		print("omg motion!!!")
		mq.publish(topic="pir/motion", msg="True")
	else:
		print("motion stopped")
		mq.publish(topic="pir/motion", msg="False")

	time.sleep(0.1)
