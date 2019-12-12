# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
webrepl.start()
gc.collect()

# Helper to unimport modules, takes a string
def unimport(mod):
	import sys
	if mod in sys.modules.keys():
		del sys.modules[mod]

# Display the network status on the OLED
def _wifi_status_display():
	import network
	import time
	import ssd1306
	from machine import Pin, I2C
	from ubinascii import hexlify

	wlan = network.WLAN()
	essid = wlan.config('essid')
	w = 128
	h = 32

	oled = ssd1306.SSD1306_I2C(w, h, I2C(-1, Pin(5), Pin(4)))
	oled.fill(0) # fill the screen with black

	# Wait a few seconds for the WiFi to come up,
	# but don't block forever on it
	print("essid: " + essid, end='')
	oled.text(essid, 0, 0)
	oled.text(hexlify(wlan.config('mac')), 0, 24)
	oled.show()

	spinner = "\\|/-"

	for i in range(128):
		print(".", end='')
		if wlan.isconnected():
			break
		oled.fill_rect(w-8, h-8, 8, 8, 0)
		oled.text(spinner[i % 4], w-8, h-8)
		oled.show()
		time.sleep_ms(50)

	# Erase the spinner
	oled.fill_rect(w-8, h-8, 8, 8, 0)
	print()

	if wlan.isconnected():
		# OLED screen is 16 chars, worst case is 15 chars
		# (abc.def.ghi.lmn) in the address, so don't put
		# any leading text on the display
		ip = wlan.ifconfig()[0]
		oled.text(ip, 0, 12)
		print("ip: " + ip)
	else:
		oled.text("network failure", 0, 12)
		print("ip: none!")

	oled.show()
	gc.collect()

_wifi_status_display()

# start the local web server for the webrepl
# gzip'ed files are served from ./html
import webserver
webserver.start()
