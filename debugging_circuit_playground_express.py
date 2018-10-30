
import sys
import os

import board
import neopixel

import time

import board
import math

import digitalio
from digitalio import DigitalInOut, Direction, Pull


DEBUG_MODE = False
MAX_NUMBER_OF_ANIMATION_STATES = 2

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


def shortkeypress(color_palette):
    color_palette += 1

    if color_palette > MAX_NUMBER_OF_ANIMATION_STATES:
        color_palette = 1

    return color_palette


def _RunningLights(red, green, blue, WaveDelay):
    """[summary]

    Arguments:
        red {int} -- [hex representation of color red]
        green {int} -- [hex representation of color green]
        blue {int} -- [hex representation of color blue]
        WaveDelay {int} -- [time to delay animation, in seconds (will be converted to miliseconds)]
    """

    position = 0

    i = 0
    DOUBLE_NUM_PIXELS = num_pixels * 2

    while i < DOUBLE_NUM_PIXELS:
        if DEBUG_MODE:
            print("INSIDE: _RunningLights FIRST LOOP: i={}".format(i))
        position = position + 1  # = 0; #Position + Rate;

        j = 0
        while j < num_pixels:
            # NOTE: From orig
            # sine wave, 3 offset waves make a rainbow!
            # float level = sin(i+Position) * 127 + 128
            # setPixel(i, level, 0, 0)
            # float level = sin(i+Position) * 127 + 128

            r = ((math.sin(j + position) * 127 + 128) / 255) * red
            g = ((math.sin(j + position) * 127 + 128) / 255) * green
            b = ((math.sin(j + position) * 127 + 128) / 255) * blue

            if DEBUG_MODE:
                print(
                    "INSIDE: _RunningLights SECOND LOOP: r={}, g={}, b={}".format(r, g, b))

            _setPixel(
                j,
                r,
                g,
                b,
            )

            j = j + 1

        _showStrip()
        _delay(WaveDelay)
        i = i + 1


# BUTTON REGISTER
button = DigitalInOut(board.BUTTON_A)
button.direction = Direction.INPUT
button.pull = Pull.DOWN
# BUTTON STATES
prevkeystate = False
ledmode = 0  # button press counter, switch color palettes


# dump(board)

# dump(left_rib_pixels)

# dump(button)

# Mainloop
try:
    while True:

        _showStrip()

        # check for button press
        currkeystate = button.value

        # button press, move to next pattern
        if (prevkeystate is not True) and currkeystate:
            ledmode = shortkeypress(ledmode)

        # save button press state
        prevkeystate = currkeystate

        # black panther solid colors on
        if ledmode == 1:
            _setAll(141, 0, 155)
        # OFF
        elif ledmode == 2:
            _setAll(0, 0, 0)

        time.sleep(0.01)

except KeyboardInterrupt:
    pass
