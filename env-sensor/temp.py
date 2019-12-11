import time
import network
from ubinascii import hexlify
from umqtt.simple import MQTTClient
from machine import Pin
from dht import DHT22

########### global variables ##############################

unique_ID = hexlify(network.WLAN().config('mac'))

def config  = {
    'mqtt_broker': '192.168.0.12',  # central server for our mqtt network
    'mqtt_client': unique_ID, # this device client ID
    'pin': 0, # which pin the temp/humidity sensor is on
}

mq = MQTTClient(config.mqtt_client, config.mqtt_broker)
dht = DHT22(Pin(config.pin)) 

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
