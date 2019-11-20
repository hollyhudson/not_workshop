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

It's the first address.  Remember this, you'll use it in a bit.

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

#### Setup

To view webrepl in your browser go to [http://micropython.trmm.net/](http://micropython.trmm.net/).  **Note:** make sure your browser doesn't correct it to be `https`.  You'll want to use the `http` site or it won't work.  If you run the HTTPS Everywhere extension, disable it for this page.

Replace the IP address in the text box with the one for your ESP board.  If you forgot the IP address, you can run screen again in a terminal, then:

```
>>> import network
>>> wlan = network.WLAN(network.STA_IF)
>>> wlan.ifconfig()
```


Quit with `ctrl-a` `ctrl-\`

To paste a bunch of code at the prompt do `ctrl-e`.

`ctrl-c` will quit the `while(true)` loop.

#### Workflow

To put code on your board you use the "Send a file" area to send your `.py` files to the board.  You're not limited to one file, you can send several.  If you want one to be the code that gets run automatically whenever the board boots, name it `main.py`.  Other files you send will not overwrite your `main.py` file.

Once you have sent the file to the board to run it you have to import it.  So if I just sent led.py, I type:

```
>>> import led
```

Oh no!  You have a bug!  You'll need to delete that module before you send and import your fix (sorry).  You use the `sys` module for this:

```python
>>> import sys
>>> del sys.modules['led']
```

Now send the debugged file and import again.  (You only need to import `sys` once.)

Lather, rinse, repeat.

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

Hackaday talk about cloudless IoT [https://hackaday.com/2019/11/07/found-footage-elliot-williams-talks-nexus-technologies/](https://hackaday.com/2019/11/07/found-footage-elliot-williams-talks-nexus-technologies/)

Candle, privacy-friendly smarthome [https://www.candlesmarthome.com/](https://www.candlesmarthome.com/)

Snips, private-by-design voice assistant [https://snips.ai/](https://snips.ai/)

MQTT [https://mqtt.org/](https://mqtt.org/)

Node Red, "low code" programming for networked things [https://nodered.org/](https://nodered.org/)

Cloning a Raspberry Pi [https://raspberrypi.stackexchange.com/questions/93315/cloning-the-raspberry-pi-sd-card-as-a-balenaetcher-ready-instal-able-image](https://raspberrypi.stackexchange.com/questions/93315/cloning-the-raspberry-pi-sd-card-as-a-balenaetcher-ready-instal-able-image)

Adafruit ESP8266 Feather Huzzah pinout and guide:
[https://learn.adafruit.com/adafruit-feather-huzzah-esp8266/pinouts/](https://learn.adafruit.com/adafruit-feather-huzzah-esp8266/pinouts/)
