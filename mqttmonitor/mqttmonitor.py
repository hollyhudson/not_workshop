import time
import network
from umqtt.simple import MQTTClient
from machine import Pin, I2C
import ssd1306

mqtt_server = '192.168.0.10'
wlan = network.WLAN()
essid = wlan.config('essid')
w = 128
h = 32

oled = ssd1306.SSD1306_I2C(w, h, I2C(-1, Pin(5), Pin(4)))
oled.fill(0) # fill the screen with black

color = 0
while True:
	print("connecting to " + essid)
	oled.text("wifi: " + essid, 0, 0, color)
	oled.show()
	if wlan.isconnected():
		break
	color = not color
	time.sleep_ms(200)

ip = wlan.ifconfig()[0];
oled.text("ip: " + ip, 0, 8)
oled.text("mq: " + mqtt_server, 0, 16)
oled.show()
print("ip: " + ip)

def handle_msg(topic,msg):
	print(topic + "=" + msg)
	oled.scroll(0, -8)
	oled.fill_rect(0, h-8, w, 8, 0)
	oled.text(topic + "=" + msg, 0, h-8, 1)
	oled.show()

mq = MQTTClient(str(wlan.config('mac')), mqtt_server)
mq.connect()
mq.set_callback(handle_msg)
mq.subscribe(b"#")

while True:
	mq.check_msg()
