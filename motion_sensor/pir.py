import time
import network
import secrets
from umqtt.simple import MQTTClient
from machine import Pin

########### global variables ##############################

pir = Pin(14, Pin.IN)

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
mq = MQTTClient("pir", "192.168.0.10")
#mq.set_callback(handle_msg) # handle_msg() will be called for ALL messages received
mq.connect()
#mq.subscribe(b"led_panel/#")

# wait for MQTT messages forever
# when one is received the function we passed to set_callback() will be run
#while True:
#	mq.check_msg()

######### Publishing an MQTT message ########################

# Code involving publishing must come after the client is declared

# edge-triggered (detects when value changes state)

last_pir_value = False

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
