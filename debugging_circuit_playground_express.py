
import sys
import os

import board
import neopixel

import time

import board

import digitalio
from digitalio import DigitalInOut, Direction, Pull

DEBUG_MODE = True

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
left_rib_pixels = board.A7

# The number of NeoPixels
left_rib_num_pixels = 8

# Disable this when not running on indiviual test strip
num_pixels = left_rib_num_pixels

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
BRIGHTNESS_LVL = 0.2

# Initialize NeoPixel object for left rib
left_rib_pixel_strip = neopixel.NeoPixel(
    left_rib_pixels,
    left_rib_num_pixels,
    brightness=BRIGHTNESS_LVL,
    auto_write=False,
    pixel_order=ORDER,
)

# TESTING ONLY:
pixels = left_rib_pixel_strip

# source: http://blender.stackexchange.com/questions/1879/is-it-possible-to-dump-an-objects-properties-and-methods


def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


def _delay(time_in_seconds):
    """[Perform a time sleep in miliseconds.]

    Arguments:
        time_in_seconds {[int]} -- [delay ammount, in seconds. Function automatically converts it to miliseconds]
    """

    to_ms = float(time_in_seconds / 1000)
    time.sleep(to_ms)


def _showStrip():
    """[Arduino version of showStrip, taken from tweaking4all]

    Arguments:
        component {ANY} -- [EG. NeoPixel object, like 'left_rib_pixel_strip']
    """
    left_rib_pixel_strip.show()


def _setPixel(position, r, g, b):
    """[Arduino version of setPixel(), taken from tweaking4all]

    Arguments:
        position {int} -- [description]
        r {int} -- [description]
        g {int} -- [description]
        b {int} -- [description]
    """
    if DEBUG_MODE:
        print("INSIDE: _setPixel: r={}, g={}, b={}".format(r, g, b))

    if type(r) == float:
        r = int(r)

    if type(b) == float:
        b = int(b)

    if type(g) == float:
        g = int(g)

    _rgb = (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (
        r, g, b, 0)
    pixels[position] = _rgb
    # time.sleep(0.1)


def _setAll(r, g, b):
    """[Arduino version of setAll(), taken from tweaking4all]

    Arguments:
        r {[type]} -- [description]
        g {[type]} -- [description]
        b {[type]} -- [description]
    """

    for i in range(num_pixels):
        _setPixel(i, r, g, b)
    _showStrip()


# BUTTON REGISTER
button = DigitalInOut(board.BUTTON_A)
button.direction = Direction.INPUT
button.pull = Pull.DOWN

# dump(board)

# dump(left_rib_pixels)

# dump(button)

# Mainloop
try:
    while True:

        _showStrip()

        if button.value:  # button is pushed
            _setAll(141, 0, 155)
        else:
            # led.value = False
            _setAll(0, 0, 0)

        time.sleep(0.01)

except KeyboardInterrupt:
    pass