# Making an LED blink

![wiring diagram](esp-wiring-led.PNG)

![schematic](led-schematic.png)

```python
import time
from machine import Pin

my_led = Pin(14, Pin.OUT) # which pin your LED is connected to

my_led.on() 	# turn it on
my_led.off() 	# turn it off

# to make it blink (put this in a loop)
my_led.on() 		# turn it on
time.sleep_ms(500)	# wait 1/2 a sec
my_led.off() 		# turn it off
time.sleep_ms(500)	# wait 1/2 a sec

```

```python
# example responding to an mqtt message
def set_state(msg):
    if msg == b'on':
        my_led.on() 
    elif msg == b'off':
        my_led.off()
```

If you want to dim the LED you can use pwm:

```python
from machine import Pin,PWM

my_led = Pin(14, Pin.OUT) 
my_led_pwm = PWM(my_led)

# possible values are 0-1023
my_led_pwm.duty(0)		# off
my_led_pwm.duty(10) 	# dim	
my_led_pwm.duty(512) 	# 50% brightness
my_led_pwm.duty(1023) 	# full brightness
```
