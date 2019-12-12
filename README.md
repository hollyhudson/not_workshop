<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [STEP ONE](#step-one)
- [Things on ESP boards](#things-on-esp-boards)
  - [Using webrepl](#using-webrepl)
    - [Setup](#setup)
    - [Workflow](#workflow)
- [MQTT](#mqtt)
  - [Configuration](#configuration)
- [Node Red](#node-red)
  - [Installation](#installation)
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
  - [Using the OLED screen](#using-the-oled-screen)
- [Resources](#resources)
  - [Hardware](#hardware)
  - [Software](#software)
  - [Products](#products)
  - [Tutorials and Talks](#tutorials-and-talks)
  - [Readings](#readings)
- [What shall we call this?](#what-shall-we-call-this)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# STEP ONE

Install mosquitto (the most popular implementation of MQTT).

**Linux**
 	It's probably already there.  Run `which mosquitto` to check.

**Mac**
	Use your favorite package manager to install to install `mosquitto` and `mosquitto-clients`.  If those words didn't mean anything to you, congratulations, you will now gain a favorite package manager.  Homebrew is the most popular these days: [https://brew.sh/](https://brew.sh/), but I prefer MacPorts: [https://www.macports.org/](https://www.macports.org/).  Install one and type `brew install mosquitto mosquitto-clients` or `port install mosquitto mosquitto-clients`.  If it fails, take off the `mosquitto-clients` part and try again.

**Windows**
	The website has a download option: [https://mosquitto.org/download/](https://mosquitto.org/download/).


# Things on ESP boards

You can find detailed information about the board we are using here:
[https://github.com/Heltec-Aaron-Lee/WiFi_Kit_series](https://github.com/Heltec-Aaron-Lee/WiFi_Kit_series)

Today the boards have been set up for you.  When you plug them in they will already be on the wifi.  At home you can run `boot/setup.sh` to put your board on your home wifi.  If you buy a different type of ESP board, you can use the instructions in the `webreple-from-scratch.md` file.

## Using webrepl

### Setup

To view webrepl in your browser go to the IP address displayed on your ESP board.  

To get a prompt, click in the screen and press enter.  The password is set to `abcd` by default (this and other boot settings can be changed by editing `boot/boot.py`).

Useful commands:

**ctrl-C**
	stop the current program

**ctrl-A ctrl-V**
	paste one line

**ctrl-E**
	paste several lines of code

**ctrl-A ctrl-\**
	quit
	
**up arrow**
	cycle through previous commands

If things stop working, reload the page and/or reset the board.

### Workflow

Load code onto the board by using the "Send a file" area.

Run the code with by importing the file name, minus the `.py` part:

```python
import led
```

If you want to load a revised version to the board (after fixing a bug), you have to un-import the module and then import it again.  So, after fetching the code with the "Send a file" area, do:

```python
>>> unimport("led")
>>> import led
```

_The `unimport()` function is a custom tool written for this workshop.  If it's not available, you can `import sys` then run `del sys.modules['led']` instead._

You can always test things by running small snippets of code directly from the python prompt in the webrepl if you want.

For instance, blinking an LED:

```python
>>> from machine import Pin                                                
>>> p = Pin(0,Pin.OUT)                                                      
>>> p.on()                                                                     
>>> p.off()                                                                    
```

# MQTT

MQTT is a simple, lightweight messaging protocol.  To create an MQTT network, designate one machine as your "broker" (server), and start the broker there:

```bash
> mosquitto -v
```

The `-v` flag puts it in verbose mode.

You can then publish (tell) and subscribe (listen), from any device running the client software, with these commands:

```bash
> mosquitto_sub -h [IP address of broker] -t [topic]
> mosquitto_pub -h [IP address of broker] -t [topic] -m [message]
```

For example:

```bash
> mosquitto_pub -h 192.168.0.10 -t sensors/temp -m 23
> mosquitto_sub -h 192.168.0.10 -t sensors/temp
```

Any device can create a topic just by publishing to that topic, and other devics can subscribe to topics that interest them.

You can use `#` and `*` as wildcards for subscribing to mulitple topics.  For example, all the devices in the kitchen:

```
house/kitchen/#
```

The lights in every room in the house:

```
house/*/light
```

_Note: You can only use wildcards for subscribing.  You can not publish to more than one topic at a time._

This is a convenient protocol because of its simplicity.  It has less overhead than http and it's an open standard so it can be freely used and integrated into projects.  There are libraries for several languages (python, javascript, C/C++), so you can script interactions within your network with whatever tools you're most comfortable with.

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

You'll probably want one central hub for all of your device information and automation logic to reside so that there is one central place to go when you want to add a feature or if something breaks.  

You could script things together with your favorite programming language, but Node Red provides a convenient unified interface for both your DIY things and your consumer IoT devices.  It's a low-code environment, so it will be easier for members of your household who do not code to understand and tweak.  In addition it provides a browser-based dashboard that you can access from laptops and phones.

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

## Using the OLED screen

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

# What shall we call this?

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


