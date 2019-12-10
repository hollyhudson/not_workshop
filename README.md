<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Names](#names)
- [Things on ESP boards](#things-on-esp-boards)
  - [Flashing micropython onto the board](#flashing-micropython-onto-the-board)
    - [setup.py script method](#setuppy-script-method)
    - [Manual method](#manual-method)
      - [Enabling webrepl](#enabling-webrepl)
  - [Is it working?](#is-it-working)
  - [Using webrepl](#using-webrepl)
    - [Setup](#setup)
    - [Workflow](#workflow)
- [MQTT](#mqtt)
  - [Installation](#installation)
  - [Commands](#commands)
  - [Configuration](#configuration)
- [Node Red](#node-red)
  - [Installation](#installation-1)
  - [Node Editor](#node-editor)
  - [APIs](#apis)
  - [Saving your work](#saving-your-work)
- [SNoT - Secure Network of Things](#snot---secure-network-of-things)
  - [Securing MQTT](#securing-mqtt)
  - [Securing Node Red](#securing-node-red)
- [Troubleshooting](#troubleshooting)
- [To Do](#to-do)
  - [Document the QOS settings for mqtt](#document-the-qos-settings-for-mqtt)
- [Setting up a Raspberry Pi](#setting-up-a-raspberry-pi)
  - [Basic Setup](#basic-setup)
- [Best Practices](#best-practices)
  - [Circuits](#circuits)
  - [MQTT](#mqtt-1)
- [Resources](#resources)
  - [Hardware](#hardware)
  - [Software](#software)
  - [Products](#products)
  - [Tutorials and Talks](#tutorials-and-talks)
  - [Readings](#readings)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Names

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

# Things on ESP boards

[https://github.com/Heltec-Aaron-Lee/WiFi_Kit_series](https://github.com/Heltec-Aaron-Lee/WiFi_Kit_series)

## Flashing micropython onto the board

### setup.py script method

You'll want to install esptool and ampy with pip or pip3:

```bash
> pip3 install esptool.py
> pip3 install pip3 install adafruit-ampy
```

Run the setup script in the boot directory:

Type the beginning of the command, then hit `tab` to find the correct serial port:

```bash
> ./setup.sh /dev/tty.[tab]
tty.AVSamsungSoundbarK450K-  tty.SLAB_USBtoUART
tty.Bluetooth-Incoming-Port  tty.SOC
tty.MALS                     tty.usbserial-01DAA363
```

then finish typing the command:

```bash
> ./setup.sh /dev/tty.SLAB_USBtoUART wifi_name wifi_password
```

If your esp board is now showing the wifi network name and an IP address, it worked.

### Manual method

First, let's erase whatever is on the ESP board, and flash it with MicroPython.  We'll use esptool for both steps, which you can install with `pip` with one of the following (or however else you like to do python package management):

```bash
> pip install esptool.py
> pip3 install esptool.py
```

The code you'll want to flash can be found at [http://micropython.org/download](http://micropython.org/download).  

You have to specify which USB port your board is on, and you can find that by typing `[tab]` after `/dev/tty.` to see what the possibilities are:

```bash
> esptool.py --port /dev/tty.
tty.AVSamsungSoundbarK450K-  tty.SLAB_USBtoUART
tty.Bluetooth-Incoming-Port  tty.SOC
tty.MALS                     tty.usbserial-00FEB022
```

That `SLAB_USBtoUART` one is the one we want. First erase:

```bash
> esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash
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
```

Then flash:

```bash
> esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect 0 esp8266-20190529-v1.11.bin
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
```

Finally, run `screen`, which will let us interact directly with the serial (USB) port so that we can get an interactive python prompt from our python installation on the board:

```bash
> screen /dev/tty.SLAB_USBtoUART 115200
```

Hit `enter` to get a prompt.

Hit `ctrl-D` to reset it, which will display the version of micropython that's flashed to the board.

To quit type `ctrl-A` `ctrl-\`.

In screen, put the board on your local network by:

```python
>>> import network
>>> wlan = network.WLAN(network.STA_IF)
>>> wlan.active(True)
#8 ets_task(4020f4d8, 28, 3fff9e28, 10)
>>> wlan.connect("your_wifi", "password") # your local wifi credentials go here
```

To see your board's ip address:

```
>>> wlan.ifconfig()
('192.168.0.38', '255.255.255.0', '192.168.0.1', '192.168.0.1')
```

It's the first address.  **Remember this**, you'll use it in a bit.

#### Enabling webrepl

```python
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

## Is it working?

If you have an ESP with an onboard LED, you can confirm everything is working by lighting up an LED:

```python
>>> from machine import Pin                                                
>>> p = Pin(14,Pin.OUT)                                                      
>>> p.on()                                                                     
>>> p.off()                                                                    
```

If you have one with an OLED screen, import the libraries and instantiate an object:

```python
>>> import machine
>>> import ssd1306
>>> i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
>>> oled = ssd1306.SSD1306_I2C(128, 32, i2c)
```

And here are some basic commands:

```python
>>> oled.fill(1) # fill the screen with white (actually blue)
>>> oled.fill(0) # fill the screen with black
>>> oled.text("hello",0,0,1) # ("text", x, y, black/white)
>>> oled.show() # actually display now
>>> oled.invert() # invert colors
>>> oled.pixel(x, y, c) # address one pixel
```

Full documentation for the OLED screen is here: [https://docs.micropython.org/en/latest/library/framebuf.html](https://docs.micropython.org/en/latest/library/framebuf.html)

You can always find more info with `dir()` and `help()`:

```python
dir(oled)
help(oled)
```

But for full documentation you'll want to check out the micropython documentation pages online: [http://docs.micropython.org/en/latest/](http://docs.micropython.org/en/latest/)

## Using webrepl

### Setup

To view webrepl in your browser go to [http://micropython.trmm.net/](http://micropython.trmm.net/).  **Note:** make sure your browser doesn't correct it to be `https`.  You'll want to use the `http` site or it won't work.  If you run the HTTPS Everywhere extension, disable it for this page.

Replace the IP address in the text box with the one for your ESP board, and hit `Connect`.  If you forgot the IP address, you can run screen again in a terminal, then:

```python
>>> import network
>>> wlan = network.WLAN(network.STA_IF)
>>> wlan.ifconfig()
```

You'll see at the bottom it says use `ctrl-A` and `ctrl-V` to paste.  If you want to paste multiple lines of code use `ctrl-E` instead (or upload it as a file).  To quit use `ctrl-a` `ctrl-\`.

If end up with no prompt because code is running, hit `ctrl-C` to quit the `while(true)` loop.

### Workflow

We want to be able to write, run, debug, write, run, debug... etc.

You can write your code on your laptop, then push the file to the board using the "Send a file" area.  To then run the code, type `import [filename without the .py part]`.  So if my file is `led.py`, I want to type `import led`.

You're not limited to one file, you can have several on the board at once.  If you want one to be the code that gets run automatically whenever the board boots, name it `main.py` and run `import main`.  

When you want to resend the file after debugging, you will have to delete the module first (sorry).  You'll need to import `sys` for this:

```python
>>> import sys
>>> del sys.modules['led']
```

Now send the debugged file and import again.  (You only need to import `sys` once.)

Now we can write, run, and debug over and over again.

You can also run small snippets of code directly from the python prompt to test things out if you want.

# MQTT

MQTT is a simple, lightweight messaging protocol.  Clients can both publish to and subscribe to topics.  If I publish to a topic called "talk", everyone who is subscribed to that topic will get the message.  Topics can be anything, and they are hierarchical.  So I can have, for instance:

```
house/kitchen/lights/overhead
house/kitchen/lights/sink
house/kitchen/lights/under_counter
house/kitchen/sensors/temp
house/kitchen/sensors/humidity
```

Using this example, I could turn on the overhead light in the kitchen by publishing the message `on` to `house/kitchen/lights/overhead`, and I could subscribe to receive messsages from all the sensors in the kitchen by subscribing to `house/kitchen/sensors/#`.  (The `#` here is a wildcard.)

This is a convenient protocol because of its simplicity.  It has far less overhead than http, it's an open standard so it can be freely used and integrated into projects, and there are libraries for several languages (python, javascript, C/C++).

To use MQTT you need to have one device act as a broker that receives all published messages and sends them out to subscribers.  For an IoT setup you'll probably want this to be a machine that stays on all the time, like a Raspberry Pi.  The most popular broker is Mosquitto.  It's free and open source, and runs on Linux, MacOs, and Windows.

## Installation

For MQTT you'll need a broker to act as the main switchboard for all your messages, and a client running on each of your devices.  For testing purposes it's good to install both a broker and client module on whatever computer you're running the broker on.  You can do this with whatever package manager you use, here are some examples:

Linux/Debian/Ubuntu:
```bash
> sudo apt install mosquitto mosquitto-clients
```

MacOS:
```bash
> sudo port install mosquitto mosquitto-clients
```

or

```bash
> brew install mosquitto mosquitto-clients
```

Here's the Mosquitto website: [https://mosquitto.org/](https://mosquitto.org/), if you want to download it directly or build it from source.

## Commands

To start a broker (in verbose mode):

```bash
> mosquitto -v
```

The basic format for subscribing to a topic, and for publishing a message to that topic:

```bash
> mosquitto_sub -h [host ip] -t [topic]
> mosquitto_pub -h [host ip] -t [topic] -m [message]
```

example:

```bash
> mosquitto_sub -h 129.168.0.23 -t led 
> mosquitto_pub -h 129.168.0.23 -t led -m 255,0,255
```

You can use `#` and `+` as wildcards to susbscribe to more than one topic.  You cannot use wildcards to publish to more than one topic.

**living_room/\#**
	all topics for all devices in your living room (you have to escape the `#` character on the command line)

**living_room/+/bulb**
	all the lightbulbs in your living room

**\#**
	subscribe to all messages

## Configuration

Where to find `mosquitto.conf`:

* MacOS - `/usr/local/etc/mosquitto`
* Linux - `/etc/mosquitto`
* Windows - `c:\mosquitto\`

By default the mosquitto broker runs on port 1883, unless you intentionally start it on another port: `mosquitto -p 1884`, for instance.

MQTT messages are sent in plaintext.  If you want to encrypt them you have to use SSL.  But there are some other things you can do that are fairly simple to provide some security.

You can restrict who can publish and subscribe to messages by setting client ID restrictions on your broker.

# Node Red

![example flow for Node Red](images/nodered-example-flow.png)

If you do a lot of programming, you're probably already thinking of ways to script automations for your devices with MQTT.  But if you don't want to write a lot of code, or want to make it possible for non-programmers in your household or workspace to edit automations, Node Red is a good option.  Most of the interface is boxes (nodes) that you "wire" together to pass messages from one component to another, with some javascript thrown in where necessary to customise the logic of those automations.  Plus you can easily create a web-based dashboard of buttons and switches that folks can access from their laptops and smartphones.

![example dashboard for Node Red](images/nodered-example-dashboard.png)

## Installation

If you don't already have node.js installed, get it here: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)

Next, install Node Red: [https://nodered.org/docs/getting-started/local](https://nodered.org/docs/getting-started/local)

On the website, if you click "Running" in the side bar you'll see detailed information on how to use it once it's installed.

On the command line type `node-red` to start it, and it will provide you with some useful information:

```bash
2 Dec 17:44:35 - [info] Settings file  : /Users/holly/.node-red/settings.js
2 Dec 17:44:35 - [info] Context store  : 'default' [module=memory]
2 Dec 17:44:35 - [info] User directory : /Users/holly/.node-red
2 Dec 17:44:35 - [warn] Projects disabled : editorTheme.projects.enabled=false
2 Dec 17:44:35 - [info] Flows file     : /Users/holly/.node-red/flows_geode.json
2 Dec 17:44:35 - [info] Server now running at http://127.0.0.1:1880/
```

Note that node red runs on port 1880 by default (MQTT runs on port 1883).

## Node Editor

For a basic interaction, find a "slider" node and plug it into a "debug" node.  You might have to install the dashboard module first:

Hamburger menu --> Manage Palette --> install node-red-dashboard

View the dashboard by going to the url of your palette with a `/ui` added to the end (or click the dashboard icon in the node editor).

**In order for changes you made in the node editor to take effect, you have to click "Deploy".**  You will be clicking "Deploy" a lot.

Node Red's basic function is to send messages from one thing to another.  While these messages can enter Node Red in any number of formats (http, mqtt, html, xml, etc.) once inside Node Red they are converted to and passed around as json objects.  Here is the basic structure:

```javascript
{
	"key": "value",
	"key": "value"
}
```

You can modify messages and automate decisions based on messages by using javascript with the "function" node.  When you open it you'll see `return msg;` in the textbox.  You just add your code above that.  The incoming message object is stored in the `msg` variable, so if you do nothing the message will pass through the node unchanged.

But you probably want to alter the message.  Here's what you need to know.  The actual content of the message is stored in the "payload" property of the message object:

```javascript
msg = {
	"payload": "on"
}
```

Which can also be written:

```javascript
msg.payload = "on";
```

Above is a common example where you want to pass the string "on" to a device to, for example, turn on a lightbulb.

The payload can be a string, as above, a number (don't use quotes), a boolean (true or false), an array, or an object.  For instance, here's a message that I use to set the brightness and color temperature of an Ikea smart bulb, where the payload is an object:

```javascript
msg.payload = {
	"brightness": 150,
	"mired": 400
}	
```

Since you can write javascript in the function node, you can add logic.  For instance, the color spectrum Ikea smart bulbs use color names instead of numerical values.  I wanted to be able to use a slider on the dashboard to change the color, and the slider would just return numbers, so I needed to convert those numbers into colors to actually craft a message that the Ikea device would understand.  Here's the code:

```javascript
var colors = [
	"dark peach",
	"warm amber",
	"candlelight",
	"warm",
	"sunrise",
	"normal",
	"lime",
	"yellow",
	"pink",
	"saturated pink",
	"light purple",
	"saturated purple",
	"blue",
	"light blue",
	"cold sky",
	"cool daylight",
	"focus"];
    
index = msg.payload; // incoming msg, which is an int
color_name = colors[index];
msg.payload = {
    "color": color_name
};

return msg;
```

You'll probably want to turn a bunch of lights on or off at once, but MQTT doesn't let you publish to multiple topics at the same time.  In Node Red you can solve this problem by creating an array of messages in a function node:

```javascript
var incoming_payload = msg.payload; // will be "on" or "off"

var messages = [];

var topics = [
	"home/upstairs/bedroom/light/state",
	"home/upstairs/hall/light/state",
	"home/upstairs/beadroom/heater/state"
];
    
for (var topic of topics) {
	messages.push({payload: incoming_payload, topic: topic});
}
return [messages];
```

Sometimes I declare my variables with `var`, sometimes I don't bother.  In both cases it works.  There's probably something to be said here in regards to best practices.. but 🤷🏻

## APIs

If you want to get online data like weather data, you can do that with an http request to the website of your choice.  Here is an example with my favorite online API:

![example nodes](images/api-nodes.png)

Inside the http node (the "get astronaut json" node):

![images/api-get-request.png](images/api-get-request.png)

And here is the code in the function node that extracts the data we want from the json object so we can display it on the dashboard:

```javascript
var people_obj = msg.payload["people"];
var output_str = "";

for (var person of people_obj) {
	if (person == people_obj[0]) {
		output_str = person.name;
	} else if (person == people_obj[people_obj.length - 1]) {
		output_str = output_str + ", and " + person["name"];
	} else {
		output_str = output_str + ", " + person["name"];
	}
}

output_str = output_str + " are all in space right now."

var new_msg = { "payload": output_str}
return new_msg;
```

## Saving your work

**There is no undo in Node Red.**

Your current flow setup is stored in `~/.node-red/flows_[something].json`.  
It's a good idea to make a copy of this file frequently for back
up.  If you put it in version control on github, make sure you
haven't included any secret authentication information in any of
the flows.

Since the structure of the flows is stored as json, you can share your flows, and install other people's flows, by sharing the json description.

# SNoT - Secure Network of Things

In general, securing the system is beyond the scope of this workshop.  The design presented here is not exposed to the internet, so in order to control devices an attacker would have to log onto your home wifi, which provides some basic protection for most threat models (ie., if you are not specifically a target of someone).

Here are some additional protections you can add that are not too much trouble.

## Securing MQTT

In the `mosquitto.conf` file (how to find this is in the main MQTT section) there's a section on access control.  You can set usernames an passwords for your clients, and you can restrict who can subscribe and publish based on topic and/or client ID.

## Securing Node Red

# Troubleshooting

**Can't connect to micropython.org/webrepl**

Try the `http` site and _not_ the `https` site.  If you try to access from the `https` site browsers may refuse to serve the "insecure content" from the websocket.

# To Do

## Document the QOS settings for mqtt

The broker will hold the last message sent, and if you run
`mq.wait_msg()` the board will listen for a message again and get
whatever was sent in the interim (with the current qos configuration,
this can be changed).

# Setting up a Raspberry Pi

## Basic Setup

These instructions are for a headless (no monitor) Raspberry Pi W0.

Raspberry Pi's keep their operating system on an SD card, so the first thing we have to do is flash a card with the appropriate operating system.

First download the "lite" version of the most recent Raspbian version here: [https://www.raspberrypi.org/downloads/raspbian/](https://www.raspberrypi.org/downloads/raspbian/)

We'll use Etcher for flashing the OS onto the Pi, so download and install it: [https://www.balena.io/etcher/](https://www.balena.io/etcher/)

(So, I guess if you're running Catalina find a friend with Linux to flash your SD card because that seems to be broken in Catalina right now?)

Now, we'll need to get the wifi credentials onto the board since we're not connecting it to a monitor.  Instructions for that are here: [https://www.raspberrypi.org/documentation/configuration/wireless/headless.md](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)

Now you need to find the ip address of your Raspberry Pi.  `nmap` is good for this. 

[...some steps skipped...]

Having just set up your pi, it's in a bit of a dangerous state since remote login is enabled and the default username and password are `pi` and `raspberry`.  Log in and create a .ssh directory in pi's home directory:

```
holly@geode:~ > ssh pi@192.168.0.39
pi@raspberrypi:~ $ mkdir .ssh
```

From your local machine, transfer your public ssh key to the pi:

```
holly@geode:~/.ssh >  scp id_rsa.pub pi@192.168.0.39:/home/pi/.ssh/authorized_keys
pi@192.168.0.39's password:
id_rsa.pub                                    100%  399    71.6KB/s   00:00
```

Now, before you turn off password login, make sure you can successfully log into the pi.  So exit, and ssh back in.

```
pi@raspberrypi:~/.ssh $ exit
logout
Connection to 192.168.0.39 closed.
holly@geode:~ >  ssh pi@192.168.0.39
Enter passphrase for key '/Users/holly/.ssh/id_rsa':
Linux raspberrypi 4.19.75+ #1270 Tue Sep 24 18:38:54 BST 2019 armv6l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc//copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Nov 23 15:09:38 2019 from 192.168.0.10

SSH is enabled and the default password for the 'pi' user has not been changed.
This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.

pi@raspberrypi:~ $
```

and turn off password login by editing `/etc/ssh/sshd_config`, searching for the line `#PasswordAuthentication yes` and changing the yes to no and uncomment the line (remove the `#`).

To make the changes take effect, restart `ssh` with:

```
pi@raspberrypi:~ $ sudo /etc/init.d/ssh restart
[ ok ] Restarting ssh (via systemctl): ssh.service.
```

or just reboot the pi.

You'll probably want to change the hostname of your pi.  Edit two files, `/etc/hosts` and `/etc/hostname`, replacing all instance of "raspberrypi" with whatever you want the hostname to be, then reboot the pi (`sudo reboot`).

Now let's get the os up to date:

```
pi@raspberrypi:~ $ sudo apt update
pi@raspberrypi:~ $ sudo apt upgrade
```

# Best Practices

## Circuits

**Unplug** your microcontroller before you change the wiring.

**Black wire** for ground.

**Red wire** for power.

Connect in this order:
	1. ground
	1. power
	1. data

## MQTT

For devices that can be turned on and off, like light bulbs, have two topics:

Have a `my_bulb/state` that only the bulb publishes to.  If other devices, scripts, or dashboard interfaces want to control the bulb, they publish to a `my_bulb/set` topic instead. 


# Resources

## Hardware

Details for ESP board used in this workshop: 
[https://github.com/Heltec-Aaron-Lee/WiFi_Kit_series](https://github.com/Heltec-Aaron-Lee/WiFi_Kit_series)

Adafruit ESP8266 Feather Huzzah pinout and guide:
[https://learn.adafruit.com/adafruit-feather-huzzah-esp8266/pinouts/](https://learn.adafruit.com/adafruit-feather-huzzah-esp8266/pinouts/)

## Software

MQTT
[https://mqtt.org/](https://mqtt.org/)

Node Red, "low code" programming for networked things
[https://nodered.org/](https://nodered.org/)

Snips, private-by-design voice assistant
[https://snips.ai/](https://snips.ai/)

Mozilla's WebThings:
[https://iot.mozilla.org/](https://iot.mozilla.org/)

## Products

Candle, privacy-friendly smarthome
[https://www.candlesmarthome.com/](https://www.candlesmarthome.com/)

## Tutorials and Talks

Cloning a Raspberry Pi
[https://raspberrypi.stackexchange.com/questions/93315/cloning-the-raspberry-pi-sd-card-as-a-balenaetcher-ready-instal-able-image](https://raspberrypi.stackexchange.com/questions/93315/cloning-the-raspberry-pi-sd-card-as-a-balenaetcher-ready-instal-able-image)

Hackaday talk about cloudless IoT
[https://hackaday.com/2019/11/07/found-footage-elliot-williams-talks-nexus-technologies/](https://hackaday.com/2019/11/07/found-footage-elliot-williams-talks-nexus-technologies/)

Adafruit NeoPixel Uberguide
[https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels](https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels)

## Readings

"How Consumer IoT Devices Expose Information"
[https://labs.ripe.net/Members/anna_maria_mandalari_2/how-consumer-iot-devices-expose-information](https://labs.ripe.net/Members/anna_maria_mandalari_2/how-consumer-iot-devices-expose-information)

