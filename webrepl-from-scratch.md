This procedure is not necessary if you're using the boot.py and setup.sh files.  But here it is just in case.

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

## Using webrepl

### Setup

To view webrepl in your browser go to .....  **Note:** make sure your browser doesn't correct it to be `https`.  You'll want to use the `http` site or it won't work.  If you run the HTTPS Everywhere extension, disable it for this page.

Replace the IP address in the text box with the one for your ESP board, and hit `Connect`.  If you forgot the IP address, you can run screen again in a terminal, then:

```python
>>> import network
>>> wlan = network.WLAN(network.STA_IF)
>>> wlan.ifconfig()
```


