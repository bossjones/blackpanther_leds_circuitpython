# Note, this version ONLY works with the lift rib version
import sys
import os

import random
import board
import neopixel

import time

import board
import math

import digitalio
from digitalio import DigitalInOut, Direction, Pull

leds = {
    "left_rib": {
        # On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
        # Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
        "data_pin": board.A7,
        # number of pixels on device to use
        "num_pixels": 8,
        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        "order": neopixel.GRB,
        "brightness_lvl": 0.2,
        # This is where the initialized neopixel object will go
        "led_object": None,
    },
    # "left_chest": {
    #     "data_pin": board.NEOPIXEL,
    #     "num_pixels": 10,
    #     "order": neopixel.GRB,
    #     "brightness_lvl": 0.2,
    #     "led_object": None,
    # },
    # "left_abs": {
    #     "data_pin": board.A2,
    #     "num_pixels": 8,
    #     "order": neopixel.GRB,
    #     "brightness_lvl": 0.2,
    #     "led_object": None,
    # },
    # "left_middle": {},

    # "right_rib": {},
    # "right_chest": {},
    # "right_abs": {},
    # "right_middle": {},
}


DEBUG_MODE = False
MAX_NUMBER_OF_ANIMATION_STATES = 5

# NOTE: Use this guy to initialize neopixel objects and add them to our dictonary lookup
def create_neopixel_objects(device=None):
    # if device object exists
    if device in leds:
        _neopixel_obj = neopixel.NeoPixel(
            leds[device]["data_pin"],
            leds[device]["num_pixels"],
            brightness=leds[device]["brightness_lvl"],
            auto_write=False,
            pixel_order=leds[device]["order"],
        )

        # Add neopixel object to dict
        leds[device]["led_object"] = _neopixel_obj

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

def _showStrip(device=None):
    """[Arduino version of showStrip, taken from tweaking4all]

    Arguments:
        component {ANY} -- [EG. NeoPixel object, like 'left_rib_pixel_strip']
    """
    # Get device object (Usually of type NeoPixel)
    device = leds[device]["led_object"]
    device.show()

def _setPixel(position, r, g, b, device=None):
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

    _rgb = (r, g, b) if leds[device]["order"] == neopixel.RGB or leds[device]["order"] == neopixel.GRB else (
        r, g, b, 0)

    pixels = leds[device]["led_object"]
    pixels[position] = _rgb
    # time.sleep(0.1)

def _setAll(r, g, b, device=None):
    """[Arduino version of setAll(), taken from tweaking4all]

    Arguments:
        r {[type]} -- [description]
        g {[type]} -- [description]
        b {[type]} -- [description]
    """

    num_pixels = leds[device]["num_pixels"]

    for i in range(num_pixels):
        _setPixel(i, r, g, b, device=device)
    _showStrip(device=device)

def shortkeypress(color_palette):
    color_palette += 1

    if color_palette > MAX_NUMBER_OF_ANIMATION_STATES:
        color_palette = 1

    return color_palette

def _RunningLights(red, green, blue, WaveDelay, device=None):
    """[summary]

    Arguments:
        red {int} -- [hex representation of color red]
        green {int} -- [hex representation of color green]
        blue {int} -- [hex representation of color blue]
        WaveDelay {int} -- [time to delay animation, in seconds (will be converted to miliseconds)]
    """
    num_pixels = leds[device]["num_pixels"]

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
                device=device,
            )

            j = j + 1

        _showStrip(device=device)
        _delay(WaveDelay)
        i = i + 1


def _colorWipe(red, green, blue, WaveDelay, device=None):
    """[ColorWipe animation from tweaking4all]
    """
    num_pixels = leds[device]["num_pixels"]

    k = 0
    while k < num_pixels:
        if DEBUG_MODE:
            print("BEFORE - INSIDE: _colorWipe FIRST LOOP: k={}".format(k))
            print(
                "BEFORE - INSIDE: _colorWipe FIRST LOOP: red={}, green={}, blue={}".format(
                    red, green, blue
                )
            )

        _setPixel(
            k,
            red,
            green,
            blue,
            device=device,
        )

        _showStrip(device=device)
        _delay(WaveDelay)

        k = k + 1

# meteorRain - Color (red, green, blue), meteor size, trail decay, random trail decay (true/false), speed delay
def _meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, speedDelay, device=None):
    num_pixels = leds[device]["num_pixels"]

    _setAll(0, 0, 0, device=device)

    DOUBLE_NUM_LEDS = num_pixels+num_pixels

    i = 0
    while i < DOUBLE_NUM_LEDS:

        # fade brightness all LEDs one step
        j = 0
        while j < num_pixels:
            if (not meteorRandomDecay) or (random.randint(0, 10) > 5):
                _fadeToBlack(j, meteorTrailDecay)
            j = j + 1

        # draw meteor
        j = 0
        while j < meteorSize:
            if (i-j < num_pixels) and (i-j >= 0):
                _setPixel(i-j, red, green, blue, device=device)
            j = j + 1

        _showStrip(device=device)
        _delay(speedDelay)
        i = i + 1

def _fadeToBlack(ledNo, fadeValue, device=None):
    pixels = leds[device]["led_object"]

    oldColor = pixels[ledNo]

    # What do 0LL or 0x0UL mean?
    # SOURCE: https://stackoverflow.com/questions/7036056/what-do-0ll-or-0x0ul-mean
    r = float(oldColor[0])
    g = float(oldColor[1])
    b = float(oldColor[2])

    if DEBUG_MODE:
        print(
            "INSIDE: _fadeToBlack r,g,b as floats: r={}, g={}, b={}".format(r, g, b))

    r = (r <= 10) and 0 or int(r-(r*fadeValue/256))
    g = (g <= 10) and 0 or int(g-(g*fadeValue/256))
    b = (b <= 10) and 0 or int(b-(b*fadeValue/256))

    if DEBUG_MODE:
        print(
            "INSIDE: _fadeToBlack r,g,b after conversion: r={}, g={}, b={}".format(r, g, b))

    _setPixel(
        ledNo,
        r,
        g,
        b,
        device=device,
    )

# BUTTON REGISTER
button = DigitalInOut(board.BUTTON_A)
button.direction = Direction.INPUT
button.pull = Pull.DOWN
# BUTTON STATES
prevkeystate = False
ledmode = 0  # button press counter, switch color palettes

# dump(board)

# dump(left_rib_data_pin)

# dump(button)


# TODO: Add the other devices
# SETUP
create_neopixel_objects(device="left_rib")
# create_neopixel_objects(device="left_chest")
# create_neopixel_objects(device="left_abs")
# create_neopixel_objects(device="left_middle")
# create_neopixel_objects(device="right_rib")
# create_neopixel_objects(device="right_chest")
# create_neopixel_objects(device="right_abs")
# create_neopixel_objects(device="right_middle")

# Mainloop
try:
    while True:
        for l in leds:
            _showStrip(device=l)

        # check for button press
        currkeystate = button.value

        # button press, move to next pattern
        if (prevkeystate is not True) and currkeystate:
            ledmode = shortkeypress(ledmode)

        # save button press state
        prevkeystate = currkeystate

        # STATE: black panther solid colors on
        if ledmode == 1:
            _setAll(141, 0, 155, device="left_rib")

        # STATE: BP Running purple lights
        elif ledmode == 2:
            _RunningLights(141, 0, 155, 50, device="left_rib")

        # STATE: ColorWipe Purple
        elif ledmode == 3:
            _colorWipe(141, 0, 155, 50, device="left_rib")
            _colorWipe(0, 0, 0, 50, device="left_rib")

        # STATE: MeteorRain
        # meteorRain - Color (red, green, blue), meteor size, trail decay, random trail decay (true/false), speed delay
        elif ledmode == 4:
            _meteorRain(141, 0, 155, 10, 64, True, 30, device="left_rib")

        # STATE: OFF
        elif ledmode == 5:
            _setAll(0, 0, 0, device="left_rib")

        time.sleep(0.01)

except KeyboardInterrupt:
    pass
