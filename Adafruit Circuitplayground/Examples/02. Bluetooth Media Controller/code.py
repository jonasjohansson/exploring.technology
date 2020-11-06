"""
A CircuitPython 'multimedia' dial demo
Uses a Circuit Playground Bluefruit + Rotary Encoder -> BLE out
Knob controls volume, push encoder for mute, CPB button A for Play/Pause
Once paired, bonding will auto re-connect devices


Adaptation by Mickey van Olst
- Made generic code CircuitPlayground specific
- Replaced rotary encoder with capacitive touch
"""

import time
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_circuitplayground import cp
ble = adafruit_ble.BLERadio()
ble.name = "Bluefruit-Volume-Control"
# Using default HID Descriptor.
hid = HIDService()
device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(hid)
cc = ConsumerControl(hid.devices)

cp.pixels.auto_write = False

FILL_COLOR = (0, 10, 10)
UNMUTED_COLOR = (128, 128, 0)
MUTED_COLOR = (128, 0, 0)
DISCONNECTED_COLOR = (40, 40, 0)

# NeoPixel LED ring
cp.pixels.fill(DISCONNECTED_COLOR)
cp.pixels.show()
dot_location = 0  # what dot is currently lit

button_a_pressed = False  # for debounce state
button_b_pressed = False  # for debounce state

#last_pos = encoder.position
last_pos = 0
muted = False
command = None
# Disconnect if already connected, so that we pair properly.
if ble.connected:
    for connection in ble.connections:
        connection.disconnect()


def draw():
    if not muted:
        cp.pixels.fill(FILL_COLOR)
        cp.pixels[dot_location] = UNMUTED_COLOR
    else:
        cp.pixels.fill(MUTED_COLOR)
    cp.pixels.show()


advertising = False
connection_made = False
print("let's go!")
while True:
    if not ble.connected:
        cp.pixels.fill(DISCONNECTED_COLOR)
        cp.pixels.show()
        connection_made = False
        if not advertising:
            ble.start_advertising(advertisement)
            advertising = True
        continue
    else:
        if connection_made:
            pass
        else:
            cp.pixels.fill(FILL_COLOR)
            cp.pixels.show()
            connection_made = True

    advertising = False

    # pos = encoder.position
    pos = last_pos
    if cp.touch_A2:
        pos += 1
        time.sleep(.1)

    if cp.touch_A3:
        pos -= 1
        time.sleep(.1)

    delta = pos - last_pos
    last_pos = pos
    direction = 0

    if delta > 0:
        command = ConsumerControlCode.VOLUME_INCREMENT
        direction = -1
    elif delta < 0:
        command = ConsumerControlCode.VOLUME_DECREMENT
        direction = 1

    if direction:
        muted = False
        for _ in range(abs(delta)):
            cc.send(command)
            # spin neopixel LED around in the correct direction!
            dot_location = (dot_location + direction) % len(cp.pixels)
            draw()


    if cp.button_b and not button_b_pressed:
        if not muted:
            print("Muting")
            cc.send(ConsumerControlCode.MUTE)
            muted = True
        else:
            print("Unmuting")
            cc.send(ConsumerControlCode.MUTE)
            muted = False
        draw()
        # while not button_B.value:  # debounce
        #    time.sleep(0.1)

    if cp.button_a and not button_a_pressed:  # button is pushed
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        print("Play/Pause")
        button_a_pressed = True  # state for debouncing
        time.sleep(0.05)

    if not cp.button_a and button_a_pressed:
        button_a_pressed = False
        time.sleep(0.05)