import sys
import time
import board
import neopixel
import brightly
from digitalio import (
    DigitalInOut,
    Direction,
    Pull
)

# -----------------------------------------------------------------------------
# INFO: Why are hexadecimal numbers prefixed with 0x?
# SOURCE: https://stackoverflow.com/questions/2670639/why-are-hexadecimal-numbers-prefixed-with-0x
# Short story: The 0 tells the parser it's dealing with a constant (and not an identifier/reserved word). Something is still needed to specify the number base: the x is an arbitrary choice.
# Long story: In the 60's, the prevalent programming number systems were decimal and octal — mainframes had 12, 24 or 36 bits per byte, which is nicely divisible by 3 = log2(8).
# -----------------------------------------------------------------------------

# NOTE: circuit express is little endian!!!

# SOURCE: https://learn.adafruit.com/circuitpython-essentials/circuitpython-analog-in
# ----- analog info ----
from analogio import AnalogIn

analog_in = AnalogIn(board.A1)

MAX_ANALOG_VALUE = 65536

def get_voltage(pin):
    """ Get value from analog sensor and convert it to a 0-3.3V voltage reading """
    return (pin.value * 3.3) / MAX_ANALOG_VALUE
# ------- analog info ---- [end]

# # SOURCE: https://learn.adafruit.com/circuitpython-essentials/circuitpython-digital-in-out
# # -------------------------------------------------------------
# # NOTE: A DigitalInOut is used to digitally control I/O pins.
led = DigitalInOut(board.D13)  # Create a new DigitalInOut object associated with the pin. Defaults to input with no pull. Use switch_to_input() and switch_to_output() to change the direction.

led.direction = Direction.OUTPUT

# # For Gemma M0, Trinket M0, Metro M0 Express, ItsyBitsy M0 Express, Itsy M4 Express
# # switch = DigitalInOut(board.D2)
# # switch = DigitalInOut(board.D5)  # For Feather M0 Express, Feather M4 Express

switch = DigitalInOut(board.D7)  # For Circuit Playground Express

switch.direction = Direction.INPUT

# EXAMPLE: So why pull-ups and not pull-downs? There are likely several reasons for it, but when wiring buttons or switches or anything "normally open", you only have to tie them to ground, you don't need to run +5V out to them. Since most boards are going to be designed with large ground pours for shielding reasons anyway, tying to ground is practically reasons.
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
pixels = neopixel.NeoPixel(pixel_pin,
                           num_pixels,
                           brightness=BRIGHTNESS_LVL,
                           auto_write=False,
                           pixel_order=ORDER)

brightly = brightly.Brightly(pixels, num_pixels)

# #8d009b - rgb(141, 0, 155)
# rgb(141, 0, 155) - (0, 141, 155)
# #e542f4
BLACK_PANTHER_PURPLE = (141, 0, 155)
BLACK_PANTHER_NOTHING = (0, 0, 0)

# RED = 0x100000 # (0x10, 0, 0) also works

RED = (255, 0, 0)  #ff0000
GREEN = (0, 255, 0) #00ff00
BLUE = (0, 0, 255)  #0000ff

# "".join('%02x' % i for i in tup)

RED_HEX = 0x100000
GREEN_HEX = 0x001000
BLUE_HEX = 0x000010

# HEX to RGB tuple
# >>> tuple(bytes.fromhex('100000'))
# (16, 0, 0)
TRUE_RED = (16, 0, 0)
TRUE_GREEN = (0, 16, 0)
TRUE_BLUE = (0, 16, 0)

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

def vibranium_effect():
    # NOTE: These 2 create the pulse effect [---begin----]
    brightly.smooth_change_to(BLACK_PANTHER_PURPLE)
    brightly.smooth_change_to(BLACK_PANTHER_NOTHING)
    # NOTE: These 2 create the pulse effect [---end----]

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
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


# SOURCE: https://circuitpython.readthedocs.io/projects/neopixel/en/latest/examples.html
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def showStrip():
    # print("Making pixel color changes active w/ 'pixels.show()'")
    pixels.show()

def setPixel(position, rgb):
    pixels[position] = rgb
    time.sleep(0.1)

def setAll(rgb):
    pixels.fill(rgb)
    time.sleep(0.1)

def setAllGreen():
    pixels.fill((0, 255, 0))
    time.sleep(0.1)

# NOTE: Bossjones cutom
def enableSensorPlot():
    print((get_voltage(analog_in),))
    time.sleep(0.1)

def setEveryOtherPixel(color=RED):
    pixels[::2] = [color] * (len(pixels) // 2)
    time.sleep(2)

# ----------------[ARDUINO VERSIONS - DEFAULT WRAPPER FUNCTION ]------------
def _delay(time_in_seconds):
    """[Perform a time sleep in miliseconds.]

    Arguments:
        time_in_seconds {[int]} -- [delay ammount, in seconds. Function automatically converts it to miliseconds]
    """

    to_ms = float(time_in_seconds/1000)
    # print("Converting from '{}s' to '{}ms'".format(time_in_seconds, to_ms))
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
    print("INSIDE: _setPixel: r={}, g={}, b={}".format(r,g,b))

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

    # FIXME: Temporarily disabled
    for i in range(num_pixels):
        _setPixel(i, r, g, b)
    _showStrip()

    # pass

# ----------------[ARDUINO VERSIONS]------------

MAX_TUPLE_POSITIONAL_ARGS = 3
MAX_PIXEL_VALUE = 256

# SOURCE: https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
def _RGBLoop():
    """[LEDStrip Effect – Fade In and Fade Out: Red, Green and Blue]
    """

    for j in range(0, MAX_TUPLE_POSITIONAL_ARGS):
        # Fade IN
        for k in range(0, MAX_PIXEL_VALUE):
            print("FADE IN. j={},k={}".format(j,k))
            if j == 0:
                _setAll(k,0,0)
            elif j == 1:
                _setAll(0,k,0)
            elif j == 2:
                _setAll(0,0,k)
        _showStrip()
        _delay(3)

        # Fade OUT
        # NOTE: range([start], stop[, step])
        # start: Starting number of the sequence.
        # stop: Generate numbers up to, but not including this number.
        # step: Difference between each number in the sequence.
        for k in range(MAX_PIXEL_VALUE-1, 0, -1):
            print("FADE OUT. j={},k={}".format(j,k))
            if j == 0:
                _setAll(k,0,0)
            elif j == 1:
                _setAll(0,k,0)
            elif j == 2:
                _setAll(0,0,k)
        _showStrip()
        _delay(3)


# SOURCE: https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
def _FadeInOut(red, green, blue):
    """[LEDStrip Effect – Fade In and Fade Out: Red, Green and Blue]
    """

    # In Python 3, relevant quotients are converted from integers to floats when doing division though they are not in Python 2. That is, when you divide 5 by 2, in Python 3 you will get a float for an answer (2.5)
    k = 0
    while k < 256:
        # for k in range(0, MAX_PIXEL_VALUE):
        # print("BEFORE - INSIDE: _FadeInOut FIRST LOOP: k={}".format(k))
        print(
            "BEFORE - INSIDE: _FadeInOut FIRST LOOP: red={}, green={}, blue={}".format(red, green, blue)
        )

        r = float((k / 256.0) * red)
        g = float((k / 256.0) * green)
        b = float((k / 256.0) * blue)
        # print(
        #     "AFTER - INSIDE: _FadeInOut FIRST LOOP: red={}, green={}, blue={}".format(red, green, blue)
        # )
        # print("AFTER - INSIDE: _FadeInOut FIRST LOOP: r={}, g={}, b={}".format(r, g, b))
        _setAll(r, g, b)
        _showStrip()
        k = k + 1

    k = 255
    while k >= 0:
        # for k in range(MAX_PIXEL_VALUE-1,0,-2):

        r = float((k / 256.0) * red)
        g = float((k / 256.0) * green)
        b = float((k / 256.0) * blue)
        # print("INSIDE: _FadeInOut SECOND LOOP: r={}, g={}, b={}".format(r, g, b))
        _setAll(r, g, b)
        _showStrip()

        k = k - 2

i = 0

while True:
    _showStrip()
    # INFO: theater_chase(self, col, wait, duration)
    # brightly.theater_chase(BLACK_PANTHER_PURPLE, 0.05, 5)
    # brightly.theater_chase((255, 0, 0), 0.05, 5)
    # brightly.theater_chase((127, 0, 0), 0.05, 5)

    # NOTE: Black Panther colors [---begin----]
    # Fade in fade out effect
    # INFO: wipe(self, wait, dir, cols):
    # brightly.wipe(0.05, 1, BLACK_PANTHER_PURPLE)
    # time.sleep(1)
    # brightly.wipe(0.05, 1, BLACK_PANTHER_NOTHING)
    # time.sleep(1)
    # Fade in fade out effect [---end----]

    # NOTE: These 2 create the pulse effect [---begin----]
    # brightly.smooth_change_to(BLACK_PANTHER_PURPLE)
    # brightly.smooth_change_to(BLACK_PANTHER_NOTHING)
    # NOTE: These 2 create the pulse effect [---end----]

    # def wipe(self, wait, dir, cols):
    # theater_chase(self, col, wait, duration):
    # brightly.wipe(0.05, 1, (148, 0, 211))
    # brightly.wipe(0.5, 1, (0, 0, 0))
    # brightly.wipe(0.05, 1, (255, 0, 0))
    # brightly.wipe(0.05, -1, (0,0,255))
    # brightly.twinkle(8, [(255,0,0),(0,255,0),(0,0,255)], 5)
    # brightly.scroll_morse("hi there", (255,0,0))
    # brightly.smooth_change_to((0,255,0))
    # brightly.smooth_change_to([(255,0,0),(201,54,0),(147,108,0),(90,165,0),(36,219,0),(0,237,18),(0,183,72),(0,126,129),(0,75,180),(0,18,237),(33,0,222),(90,0,165),(144,0,111),(198,0,57)])
    # for i in range(16):
    #     brightly.smooth_rotate_pix(1)
    # for i in range(16):
    #     brightly.set_pixels([(255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255, 0, 0), (0,0,0)])
    #     time.sleep(0.4)
    #     brightly.smooth_change_to([(0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255, 0, 0), (0,0,0), (255, 0, 0)])

    # ---------------------------SWITCH ON/OFF----------------------------------
    # We could also do "led.value = not switch.value"!
    # if switch.value:  # switch is on
    #     led.value = False
    # else:  # switch is off
    #     led.value = True

    # time.sleep(0.01)  # debounce delay
    # ---------------------------SWITCH ON/OFF----------------------------------

    # -------------------- Analog sensor data + plot ----------------------------
    # print((get_voltage(analog_in),))
    # time.sleep(0.1)
    # enableSensorPlot()
    # -------------------- Analog sensor data + plot ----------------------------

    # i = (i + 1) % 256  # run from 0 to 255
    # # print(i)
    # time.sleep(0.1)
    # w = wheel(i)
    # print("wheel: {}".format(w))
    # pixels.fill(w)
    # pixels.show()
    # time.sleep(0.1)

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
    _FadeInOut(0xff, 0x77, 0x00)

