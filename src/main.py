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
#from random import Random
import json
import micropython
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
  client.connect()
  client.subscribe(TOPIC)
  
  print('Connected to %s MQTT broker, subscribed to topic "%s"' % (server, str(TOPIC)))
  
  return client

def restart():
  print('Reconnecting...')

  machine.reset()


try:
  client = connect_and_subscribe()

  while True:
    # Schedule the update as to prevent blocking the REPL
    # The function requires that an argument is passed, hence the need of a lambda
    try:
      micropython.schedule(lambda _: client.check_msg(), None)
      time.sleep(0.3)
    except RuntimeError:
      pass
except Exception as e:
  print("An unhandled exception occurred")
  print("Exception: " + e)
  time.sleep(10)
finally:
  restart()
