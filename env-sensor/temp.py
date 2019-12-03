import time
import network
import secrets
from umqtt.simple import MQTTClient
from machine import Pin
from dht import DHT22

########### global variables ##############################

dht_sensor = DHT22(Pin(14)) # which pin your NeoPixels are connected to

########### get on the network ############################

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.essid, secrets.passwd) # your local wifi credentials

########## while waiting to connect to the network ###############

while not wlan.isconnected():
	time.sleep_ms(500)

wlan.ifconfig()

######## MQTT Client: starting, connecting, and subscribing ##########

# (client_id, client_ip_address), client_id must be unique
mq = MQTTClient("dht_sensor", "192.168.0.10")
mq.connect()

######### Publishing an MQTT message ########################

# Code involving publishing must come after the client is declared

while True:
	dht_sensor.measure()
	temp = str(dht_sensor.temperature())
	humidity = str(dht_sensor.humidity()) 
	print("temp: " + temp)
	print("humidity: " + humidity)

	mq.publish(topic="env_sensor/temp", msg=temp)
	mq.publish(topic="env_sensor/humidity", msg=humidity)

	# publish once/sec
	time.sleep_ms(1000)
