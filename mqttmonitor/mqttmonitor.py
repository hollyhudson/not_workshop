import time
import network
from umqtt.simple import MQTTClient
from machine import Pin, I2C
import ssd1306

mqtt_server = '192.168.0.44'
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
	s = topic + "=" + msg
	l = int(w / 8) # chars per line

	oled.fill(0)

	if len(s) > 0*l:
		oled.text(s[0*l:1*l], 0, 0*8)
	if len(s) > 1*l:
		oled.text(s[1*l:2*l], 0, 1*8)
	if len(s) > 2*l:
		oled.text(s[2*l:3*l], 0, 2*8)
	if len(s) > 3*l:
		oled.text(s[3*l:4*l], 0, 3*8)
		if len(s) > 4*l:
			oled.fill_rect(w-3*8, h-8, 3*8, h, 1)
			oled.text("...", w-3*8, h-8, 0)

	oled.show()

mq = MQTTClient(str(wlan.config('mac')), mqtt_server)
mq.connect()
mq.set_callback(handle_msg)
mq.subscribe(b"#")

while True:
	mq.check_msg()
