import network
from ubinascii import hexlify

# HNI Guest WiFi
# hniconnectme

unique_ID = hexlify(network.WLAN().config('mac'))

config = {
    'mqtt_broker': '10.42.46.155',  # central server for our mqtt network
    'mqtt_client': unique_ID, # this device client ID
}
