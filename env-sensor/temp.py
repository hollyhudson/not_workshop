import time
import network
from ubinascii import hexlify
from umqtt.simple import MQTTClient
from config import config
from machine import Pin
from dht import DHT22

########### global variables ##############################

unique_ID = hexlify(network.WLAN().config('mac'))

pins = {
    'sensor': 0, # which pin the temp/humidity sensor is on
}

mq = MQTTClient(config["mqtt_client"], config["mqtt_broker"])
dht = DHT22(Pin(pins["sensor"])) 

######## MQTT Client: starting, connecting, and subscribing ##########

# (client_id, client_ip_address), client_id must be unique
mq.connect()

######### Publishing an MQTT message ########################

# Code involving publishing must come after the client is declared

while True:
	dht.measure()
	temp = str(dht.temperature())
	humidity = str(dht.humidity()) 
	print("temp: " + temp)
	print("humidity: " + humidity)

	mq.publish(topic="env_sensor/temp", msg=temp)
	mq.publish(topic="env_sensor/humidity", msg=humidity)

	# publish once/sec
	time.sleep_ms(1000)
