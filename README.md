## Names

**CIot**
	Cloudless Internet of Things (?)

**IoT**
	Intranet of Things (psuedonymous on Hackaday)

**LANoT**
	Local Area Network of Things (?)

**LANoH**
	Local Area Network of Hacky-things (Eliot Williams on Hackaday)

**NoT**
	Network of Things 

**SNoT**
	Secure Network of Things

## Setting up an ESP board

### Flashing micropython onto the board

http://micropython.org/download

```
geode❀ ~🐟  esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash
esptool.py v2.8
Serial port /dev/tty.SLAB_USBtoUART
Connecting........_
Detecting chip type... ESP8266
Chip is ESP8266EX

Features: WiFi
Crystal is 26MHz
MAC: 18:fe:34:d4:0d:3e

Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 9.1s
Hard resetting via RTS pin...
geode❀ ~🐟  esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect 0 Desktop/esp8266-20190529-v1.11.bin
esptool.py v2.8
Serial port /dev/tty.SLAB_USBtoUART
Connecting........_
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
Crystal is 26MHz
MAC: 18:fe:34:d4:0d:3e
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Auto-detected Flash size: 4MB
Flash params set to 0x0040
Compressed 617880 bytes to 402086...
Wrote 617880 bytes (402086 compressed) at 0x00000000 in 9.7 seconds (effective 511.6 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
geode❀ ~🐟  screen /dev/tty.
tty.AVSamsungSoundbarK450K-  tty.SLAB_USBtoUART
tty.Bluetooth-Incoming-Port  tty.SOC
tty.MALS                     tty.usbserial-00FEB022
geode❀ ~🐟  screen /dev/tty.SLAB_USBtoUART
[screen is terminating]
geode❀ ~🐟  screen /dev/tty.SLAB_USBtoUART 115200
```

Hit `enter` to get a prompt.

Hit `ctrl-D` to reset it, which will display the version of micropython that's flashed to the board.

In screen, put the board on your local network by:

```
>>> import network
>>> wlan = network.WLAN(network.STA_IF)
>>> wlan.active(True)
#8 ets_task(4020f4d8, 28, 3fff9e28, 10)
>>> wlan.connect("your_wifi", "password") # your local wifi credentials
```

To see your board's ip address:

```
>>> wlan.ifconfig()
('192.168.0.38', '255.255.255.0', '192.168.0.1', '192.168.0.1')
```

It's the first address.

### Enabling webrepl

```
>>> import webrepl_setup
WebREPL daemon auto-start status: disabled

Would you like to (E)nable or (D)isable it running on boot?
(Empty line to quit)
> E
To enable WebREPL, you must set password for it
New password (4-9 chars): mypassword
Confirm password: mypassword
Changes will be activated after reboot
Would you like to reboot now? (y/n)
```

Confirm everything is working by lighting up an LED:

```
>>> from machine import Pin                                                
>>> p = Pin(14,Pin.OUT)                                                      
>>> p.on()                                                                     
>>> p.off()                                                                    
>>> from machine import PWM                                                    
>>> pwm = PWM(p)                                                             
>>> pwm.duty(100)                                                              
```

Valid values for `duty()` are 0 to 1023.

### Using webrepl

Use tab to find the right one:

```
geode ~  screen /dev/tty.
tty.AVSamsungSoundbarK450K-  tty.SLAB_USBtoUART
tty.Bluetooth-Incoming-Port  tty.SOC
tty.MALS                     tty.usbserial-00FEAED4
geode ~  screen /dev/tty.SLAB_USBtoUART 115200
```

Quit with `ctrl-a` `ctrl-\`

To paste a bunch of code at the prompt do `ctrl-e`.

`ctrl-c` will quit the `while(true)` loop.

OR

use "send file" button to send, but then you must do

import led

(or whatever filename) to run it

if you name it `main.py` it will run it when the micro boots.

`randomname.py` will not overwrite `main.py` on the board, so if it gets unplugged, it when it's plugged in again it will run `main.py`

```python
import sys
del sys.modules['module_to_delete']
del sys.modules['pattern']
```

### Troubleshooting

**Can't connect to micropython.org/webrepl**

Try the `http` site and _not_ the `https` site.  If you try to access from the `https` site browsers may refuse to serve the "insecure content" from the websocket.

## MQTT

```bash
> mosquitto_pub -h [host ip] -t [topic] -m [message]
> mosquitto_pub -h 129.168.0.23 -t led -m 5
```

**microA/#**
	all topics for that microcontroller

**microA/+/led**
	all led topics for that microcontroller

## To Do

### Document the QOS settings for mqtt

The broker will hold the last message sent, and if you run
`mq.wait_msg()` the board will listen for a message again and get
whatever was sent in the interim (with the current qos configuration,
this can be changed).

## Resources

"How Consumer IoT Devices Expose Information" [https://labs.ripe.net/Members/anna_maria_mandalari_2/how-consumer-iot-devices-expose-information](https://labs.ripe.net/Members/anna_maria_mandalari_2/how-consumer-iot-devices-expose-information)

Adafruit ESP8266 Feather Huzzah pinout and guide:
[https://learn.adafruit.com/adafruit-feather-huzzah-esp8266/pinouts/](https://learn.adafruit.com/adafruit-feather-huzzah-esp8266/pinouts/)
