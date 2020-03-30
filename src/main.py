import neopixel
import machine

PIXEL_COUNT = 280
GPIO_PIN = 5

pin = machine.Pin(GPIO_PIN)
strip = neopixel.NeoPixel(pin, PIXEL_COUNT)

current = (0.0, 0.0, 0.0)
def write_color(target_rgb: tuple, brightness: float, alpha: float = 1.0):
  global current

  # Mix the target value with the current value based on alpha
  current = tuple(alpha * t * brightness + (1 - alpha) * c for t, c in zip(target_rgb, current))

  # Scale the colors to [0, 255]
  rgb = tuple(int(round(v * 255)) for v in current)
  
  # Set all leds in the strip to the new RGB value
  for i in range(PIXEL_COUNT):
    strip[i] = rgb
  
  # Write the new strip state
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
rgb = None

def callback(topic: bytes, msg: bytes):
  global brightness, rgb
  
  print((topic, msg))

  if topic.endswith("/brightness"):
    payload = json.loads(msg)

    brightness = payload["brightness"]
  elif topic.endswith("/state"):
    payload = json.loads(msg)

    params = payload["params"]
    rgb = (params["red"], params["green"], params["blue"])
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

  client.connect(clean_session=True)

  print('Connected to %s MQTT broker' % server)
  
  client.subscribe(TOPIC)
  
  print('Subscribed to topic "%s"' % str(TOPIC))
  
  return client

  
try:
  client = connect_and_subscribe()

  while True:
    client.check_msg()

    if rgb is not None and brightness is not None:
      write_color(rgb, brightness, alpha=0.025)

finally:
  machine.reset()