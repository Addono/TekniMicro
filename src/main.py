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
try:
  from umqtt.simple import MQTTClient
except:
  print("MQTT library not available, try installing it using upip")
  try:
    import upip

    upip.install("micropython-umqtt.simple")
  except:
    print("Failed installing umqtt")
  finally:
    from umqtt.simple import MQTTClient

from config import load_config

CONFIG = load_config()

TOPIC = b"tek/staging/light/1/#"

# This holds the desired state according to received MQTT messages
brightness = None
rgb = None
transition = None

def update_state_from_mqtt_message(topic: bytes, msg: bytes):
  global brightness, rgb, transition
  
  print("Topic: ", topic, "Message: ", msg)

  if topic.endswith("/brightness"):
    payload = json.loads(msg)

    brightness = payload["brightness"]
  elif topic.endswith("/state"):
    payload = json.loads(msg)

    rgb = (payload["params"]["red"], payload["params"]["green"], payload["params"]["blue"])
    transition = payload["transition"]
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

  print('Connecting to', server)

  client.set_callback(update_state_from_mqtt_message)

  client.connect(clean_session=True)

  print('Connected to %s MQTT broker' % server)
  
  client.subscribe(TOPIC)
  
  print('Subscribed to topic "%s"' % str(TOPIC))
  
  return client

while True:
  try:
    client = connect_and_subscribe()

    count = 0
    while True:
      # Check for new messages to arrive
      client.check_msg()

      # Regularly ping the server
      count = (count + 1) % 250
      if count == 0:
        client.ping()

      # Update the LEDs when there is data
      if rgb is not None and brightness is not None and transition is not None:
        if transition == "sudden":
          alpha = 1
        else:
          alpha = 0.025

        write_color(rgb, brightness, alpha=alpha)
  finally:
    print("Restarting...")
