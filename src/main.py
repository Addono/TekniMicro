import neopixel
import machine

PIXEL_COUNT = 280
GPIO_PIN = 5

pin = machine.Pin(GPIO_PIN)
strip = neopixel.NeoPixel(pin, PIXEL_COUNT)

def write_color(red, green, blue, brightness):
  rgb = tuple(int(round(c * 255 * brightness)) for c in (red, green, blue))

  for i, _ in enumerate(strip):
    strip[i] = rgb
  
  strip.write()
  

import ubinascii
import machine
import json
import time
from umqtt.robust import MQTTClient
from config import load_config

CONFIG = load_config()

TOPIC = b"tek/staging/light/1/#"


brightness = None
red = None
green = None
blue = None

def callback(topic: bytes, msg: bytes):
  global red, green, blue, brightness
  
  print((topic, msg))

  if topic.endswith("/brightness"):
    payload = json.loads(msg)

    brightness = payload["brightness"]

    if red is not None and green is not None and blue is not None:
      write_color(red, green, blue, brightness)

  elif topic.endswith("/state"):
    payload = json.loads(msg)

    params = payload["params"]
    red = params["red"]
    green = params["green"]
    blue = params["blue"]

    if brightness is not None:
      write_color(red, green, blue, brightness)
  else:
    print("Unknown topic encountered")

def connect_and_subscribe():
  server = CONFIG['MQTT_HOSTNAME']
  client = MQTTClient(
    client_id=CONFIG['MQTT_CLIENT_ID'],
    server=server,
    user=CONFIG['MQTT_USERNAME'], 
    password=CONFIG['MQTT_PASSWORD'],
  )

  client.set_callback(callback)

  if not client.connect(clean_session=False):
    client.subscribe(TOPIC)
  
  print('Connected to %s MQTT broker, subscribed to topic "%s"' % (server, str(TOPIC)))
  
  return client

  
try:
  client = connect_and_subscribe()

  while True:
    client.wait_msg()

except:
  machine.reset()