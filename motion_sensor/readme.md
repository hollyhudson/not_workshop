# PIR Sensor

Passive Infrared Sensor

Details at: [https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/connecting-to-a-pir](https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/connecting-to-a-pir)

```python
from machine import Pin

pir = Pin(14, Pin.IN)

while True:
	if pir.value():
		print("omg motion!!!")

	time.sleep(0.1)
```
