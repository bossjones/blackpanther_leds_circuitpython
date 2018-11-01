import sys
import time
import board
import neopixel
import brightly
from digitalio import DigitalInOut, Direction, Pull

import math

# SOURCE: https://learn.adafruit.com/circuitpython-essentials/circuitpython-analog-in
# ----- analog info ----
from analogio import AnalogIn

analog_in = AnalogIn(board.A1)

DEBUG_MODE = False

MAX_ANALOG_VALUE = 65536


def get_voltage(pin):
    """ Get value from analog sensor and convert it to a 0-3.3V voltage reading """
    return (pin.value * 3.3) / MAX_ANALOG_VALUE


# ------- analog info ---- [end]


# # SOURCE: https://learn.adafruit.com/circuitpython-essentials/circuitpython-digital-in-out
# # -------------------------------------------------------------
# # NOTE: A DigitalInOut is used to digitally control I/O pins.
# Create a new DigitalInOut object associated with the pin.
# Defaults to input with no pull. Use switch_to_input() and switch_to_output() to change the direction.
led = DigitalInOut(board.D13)

led.direction = Direction.OUTPUT

switch = DigitalInOut(board.D7)  # For Circuit Playground Express

switch.direction = Direction.INPUT

switch.pull = Pull.UP
# # -------------------------------------------------------------

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.NEOPIXEL

# The number of NeoPixels
num_pixels = 10

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

BRIGHTNESS_LVL = 0.2

# INFO: First, we create the LED object and attach it to the correct pin or pins. In the case of a NeoPixel, there is only one pin necessary, and we have called it NEOPIXEL for easier use.
# NOTE: auto_write=False so the LEDs only refresh when we say so
pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels,
    brightness=BRIGHTNESS_LVL,
    auto_write=False,
    pixel_order=ORDER,
)

brightly = brightly.Brightly(pixels, num_pixels)

# #8d009b - rgb(141, 0, 155)
# rgb(141, 0, 155) - (0, 141, 155)
# #e542f4
BLACK_PANTHER_PURPLE = (141, 0, 155)
BLACK_PANTHER_NOTHING = (0, 0, 0)

# RED = 0x100000 # (0x10, 0, 0) also works
# "".join('%02x' % i for i in tup)
RED = (255, 0, 0)  # #ff0000
GREEN = (0, 255, 0)  # #00ff00
BLUE = (0, 0, 255)  # #0000ff


RED_HEX = 0x100000
GREEN_HEX = 0x001000
BLUE_HEX = 0x000010

# HEX to RGB tuple
# >>> tuple(bytes.fromhex('100000'))
# (16, 0, 0)
TRUE_RED = (16, 0, 0)
TRUE_GREEN = (0, 16, 0)
TRUE_BLUE = (0, 16, 0)

MAX_TUPLE_POSITIONAL_ARGS = 3
MAX_PIXEL_VALUE = 256

# # SOURCE: http://www.psychocodes.in/rgb-to-hex-conversion-and-hex-to-rgb-conversion-in-python.html
# def rgb2hex(r,g,b):
#     """[convert int values r,g,b to hex string]

#     Arguments:
#         r {int} -- [description]
#         g {int} -- [description]
#         b {int} -- [description]

#     Returns:
#         [type] -- [description]

#     Example:

#         $ rgb2hex(255, 0, 0)
#         '#ff0000'
#     """

#     hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
#     return hex

# # SOURCE: http://www.psychocodes.in/rgb-to-hex-conversion-and-hex-to-rgb-conversion-in-python.html
# def hex2rgb(hexcode):
#     rgb = tuple(map(ord,hexcode[1:].decode('hex')))
#     return rgb

# # SOURCE: https://stackoverflow.com/a/47712512/814221
# def rgba_hex_with_prefix( color, prefix = '0x' ):
#     if len( color ) == 3:
#        color = color + (255,)
#     hexColor = prefix + ''.join( [ '%02x' % x for x in color ] )
#     return hexColor


# def vibranium_effect():
#     # NOTE: These 2 create the pulse effect [---begin----]
#     brightly.smooth_change_to(BLACK_PANTHER_PURPLE)
#     brightly.smooth_change_to(BLACK_PANTHER_NOTHING)
#     # NOTE: These 2 create the pulse effect [---end----]


# SOURCE: [NOT THIS] https://learn.adafruit.com/hacking-ikea-lamps-with-circuit-playground-express/generate-your-colors#wheel-explained
# INFO: The wheel code is a function that uses math to allow a single number to represent the (r, g, b) tuple that usually represents pixel colors. If you wanted to turn your LEDs red, you'd usually use cpx.pixels.fill((255, 0, 0)). However, with wheel, if you include the function at the top of your program, you can use cpx.pixels.fill(wheel(0)).
# EXAMPLE: As you can see, if you provide wheel(112), it returns the (R, G, B) tuple (0, 174, 81)
def wheel(pos):
    # EXAMPLE: When do use wheel?
    # EXAMPLE: A. Now, if all you're doing is using solid colors, it doesn't make much sense to use wheel, because it adds a lot to your code. However, if you want to do a rainbow cycle, wheel is the answer. The typical rainbow cycle uses fancy math code to give wheel a sequence of numbers from 0 to 255, to iterate through all the possible colors from red, to green to blue, and back to red again. The rainbow cycle code is designed to continuously do this. So, even though it's only displaying a single color at any given point in time, when it's viewed altogether, it appears to be a beautiful rainbow!
    # EXAMPLE: B. This is important to know because, in our generator code, we're going to use wheel to create our rainbow cycle mode, but we're also going to use it to create our individual single color modes. Now that we understand how wheel works, the list we use for our color mode sequence generator will make a lot more sense!
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    # SOURCE: https://circuitpython.readthedocs.io/projects/neopixel/en/latest/examples.html
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


# # SOURCE: https://circuitpython.readthedocs.io/projects/neopixel/en/latest/examples.html
# def rainbow_cycle(wait):
#     for j in range(255):
#         for i in range(num_pixels):
#             pixel_index = (i * 256 // num_pixels) + j
#             pixels[i] = wheel(pixel_index & 255)
#         pixels.show()
#         time.sleep(wait)


# # def showStrip():
# #     pixels.show()


# # def setPixel(position, rgb):
# #     pixels[position] = rgb
# #     time.sleep(0.1)


# # def setAll(rgb):
# #     pixels.fill(rgb)
# #     time.sleep(0.1)


# # def setAllGreen():
# #     pixels.fill((0, 255, 0))
# #     time.sleep(0.1)


# # # NOTE: Bossjones custom
# # def enableSensorPlot():
# #     print((get_voltage(analog_in),))
# #     time.sleep(0.1)


# # def setEveryOtherPixel(color=RED):
# #     pixels[::2] = [color] * (len(pixels) // 2)
# #     time.sleep(2)


# ----------------[ARDUINO VERSIONS - DEFAULT WRAPPER FUNCTION ]------------
def _delay(time_in_seconds):
    """[Perform a time sleep in miliseconds.]

    Arguments:
        time_in_seconds {[int]} -- [delay ammount, in seconds. Function automatically converts it to miliseconds]
    """

    to_ms = float(time_in_seconds / 1000)
    time.sleep(to_ms)


def _showStrip():
    """[Arduino version of showStrip, taken from tweaking4all]
    """
    pixels.show()


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

    _rgb = (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)
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


# ----------------[ARDUINO VERSIONS]------------

# SOURCE: https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
def _RGBLoop():
    """[LEDStrip Effect – Fade In and Fade Out: Red, Green and Blue]
    """

    for j in range(0, MAX_TUPLE_POSITIONAL_ARGS):
        # Fade IN
        for k in range(0, MAX_PIXEL_VALUE):
            print("FADE IN. j={},k={}".format(j, k))
            if j == 0:
                _setAll(k, 0, 0)
            elif j == 1:
                _setAll(0, k, 0)
            elif j == 2:
                _setAll(0, 0, k)
        _showStrip()
        _delay(3)

        # Fade OUT
        # NOTE: range([start], stop[, step])
        # start: Starting number of the sequence.
        # stop: Generate numbers up to, but not including this number.
        # step: Difference between each number in the sequence.
        for k in range(MAX_PIXEL_VALUE - 1, 0, -1):
            if DEBUG_MODE:
                print("FADE OUT. j={},k={}".format(j, k))
            if j == 0:
                _setAll(k, 0, 0)
            elif j == 1:
                _setAll(0, k, 0)
            elif j == 2:
                _setAll(0, 0, k)
        _showStrip()
        _delay(3)


# SOURCE: https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
def _FadeInOut(red, green, blue):
    """[LEDStrip Effect – Fade In and Fade Out: Red, Green and Blue]
    """
    k = 0
    while k < 256:
        if DEBUG_MODE:
            print("BEFORE - INSIDE: _FadeInOut FIRST LOOP: k={}".format(k))
            print(
                "BEFORE - INSIDE: _FadeInOut FIRST LOOP: red={}, green={}, blue={}".format(
                    red, green, blue
                )
            )

        r = float((k / 256.0) * red)
        g = float((k / 256.0) * green)
        b = float((k / 256.0) * blue)

        if DEBUG_MODE:
            print(
                "AFTER - INSIDE: _FadeInOut FIRST LOOP: red={}, green={}, blue={}".format(
                    red, green, blue
                )
            )
            print(
                "AFTER - INSIDE: _FadeInOut FIRST LOOP: r={}, g={}, b={}".format(
                    r, g, b
                )
            )

        _setAll(r, g, b)
        _showStrip()
        k = k + 1

    k = 255
    while k >= 0:
        r = float((k / 256.0) * red)
        g = float((k / 256.0) * green)
        b = float((k / 256.0) * blue)
        _setAll(r, g, b)
        _showStrip()

        k = k - 2


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
                    "INSIDE: _RunningLights SECOND LOOP: r={}, g={}, b={}".format(
                        r, g, b
                    )
                )

            _setPixel(j, r, g, b)

            j = j + 1

        _showStrip()
        _delay(WaveDelay)
        i = i + 1


# i = 0

while True:
    _showStrip()
    # ----------------------------Rainbow cycle----------------------------------
    # rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step
    # ----------------------------Rainbow cycle----------------------------------

    # ------------------------------Set all green--------------------------------
    # setAllGreen()
    # ------------------------------Set all green--------------------------------

    # setEveryOtherPixel()
    # _RGBLoop()

    # _FadeInOut(float(0xff), float(0x77), float(0x00))
    # _FadeInOut(255, 119, 0)
    # _FadeInOut(0xff, 0x77, 0x00)

    _RunningLights(0xff, 0xff, 0x00, 50)
