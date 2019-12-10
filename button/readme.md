# Using a button or switch for input

![wiring diagram](esp-wiring-button.PNG)

![schematic](button-schematic.png)

If you want to know how the pins in the diagram correspond to the pins on your actual button you can use a multimeter.

Buttons are a type of tactile switch called a "momentary tactile switch" because the circuit is closed only while you are pressing them.

![Momentary tactile switches from Adafruit](../docs/media/buttons_sm.jpg)

Source: [https://www.adafruit.com/product/1119](https://www.adafruit.com/product/1119)

Another type of switch is a slide switch, where the center pin is connected to either the left or right pin, depending on the position of the switch. 

![SPDT slider switch from Adafruit](../docs/media/switch_slide_spdt.jpg)

Source: [https://www.adafruit.com/product/805](https://www.adafruit.com/product/805)

We want to read from the pin that the button is connected to, but there's a problem in that stray voltages around the board can cause random readings.  We need to hardwire the pin to something to provide a default value when the button is not pressed.  We do this with code: `PULL_UP` will connect the pin, internally, to a resistor between the pin and power, so that when the button is not pressed it will be providing a `1`.  When you press the button and close the circuit, the pin is connected to ground and the value becomes (effectively) `0`.

It's different for a slider switch.  A slider switch would be declared with only `Pin(14, Pin.IN)` (no PULL_UP) because it gets wired with 3 wires and is always connected to either ground or power.

Here is the basic code for a button:

```python
from machine import Pin

button = Pin(14, Pin.IN, Pin.PULL_UP) # which pin your LED is connected to

while True:
	if not button.value():
		print("not pressed")
	else:
		print("pressed!!!!!")
	
	time.sleep(0.1)
```
