import sys
import signal
import logging
import os
import time
import math

# --------------------------[DEBUGGER]----------------------------------
# --------------------------[DEBUGGER]----------------------------------
# --------------------------[DEBUGGER]----------------------------------
# --------------------------[DEBUGGER]----------------------------------
# --------------------------[DEBUGGER]----------------------------------
logger = logging.getLogger(__name__)

DEBUG_MODE = True
num_pixels = 10


def init_debugger():
    import sys

    from IPython.core.debugger import Tracer  # noqa
    from IPython.core import ultratb

    sys.excepthook = ultratb.FormattedTB(
        mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
    )


# source: http://blender.stackexchange.com/questions/1879/is-it-possible-to-dump-an-objects-properties-and-methods
def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


# NOTE: What is a lexer - A lexer is a software program that performs lexical analysis. Lexical analysis is the process of separating a stream of characters into different words, which in computer science we call 'tokens' . When you read my answer you are performing the lexical operation of breaking the string of text at the space characters into multiple words.
def dump_color(obj):
    # source: https://gist.github.com/EdwardBetts/0814484fdf7bbf808f6f
    from pygments import highlight

    # Module name actually exists, but pygments loads things in a strange manner
    from pygments.lexers import Python3Lexer  # pylint: disable=no-name-in-module
    from pygments.formatters.terminal256 import (
        Terminal256Formatter
    )  # pylint: disable=no-name-in-module

    for attr in dir(obj):
        if hasattr(obj, attr):
            obj_data = "obj.%s = %s" % (attr, getattr(obj, attr))
            print(highlight(obj_data, Python3Lexer(), Terminal256Formatter()))


# SOURCE: https://github.com/j0nnib0y/gtao_python_wrapper/blob/9cdae5ce40f9a41775e29754b51325652584cf25/debug.py
def dump_magic(obj, magic=False):
    """Dumps every attribute of an object to the console.
    Args:
        obj (any object): object you want to dump
        magic (bool, optional): True if you want to output "magic" attributes (like __init__, ...)
    """
    for attr in dir(obj):
        if magic is True:
            print("obj.%s = %s" % (attr, getattr(obj, attr)))
        else:
            if not attr.startswith("__"):
                print("obj.%s = %s" % (attr, getattr(obj, attr)))


def get_pprint():
    import pprint

    # global pretty print for debugging
    pp = pprint.PrettyPrinter(indent=4)
    return pp


def pprint_color(obj):
    # source: https://gist.github.com/EdwardBetts/0814484fdf7bbf808f6f
    from pygments import highlight

    # Module name actually exists, but pygments loads things in a strange manner
    from pygments.lexers import PythonLexer  # pylint: disable=no-name-in-module
    from pygments.formatters.terminal256 import (
        Terminal256Formatter
    )  # pylint: disable=no-name-in-module
    from pprint import pformat

    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))


# --------------------------[DEBUGGER]----------------------------------
# --------------------------[DEBUGGER]----------------------------------
# --------------------------[DEBUGGER]----------------------------------
# --------------------------[DEBUGGER]----------------------------------
# --------------------------[DEBUGGER]----------------------------------

MAX_TUPLE_POSITIONAL_ARGS = 3
MAX_PIXEL_VALUE = 256

BLACK_PANTHER_PURPLE = (141, 0, 155)
BLACK_PANTHER_NOTHING = (0, 0, 0)

# RED = 0x100000 # (0x10, 0, 0) also works

RED = (255, 0, 0)  # ff0000
GREEN = (0, 255, 0)  # 00ff00
BLUE = (0, 0, 255)  # 0000ff

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


def _delay(time_in_seconds):
    """[Perform a time sleep in miliseconds.]

    Arguments:
        time_in_seconds {[int]} -- [delay ammount, in seconds. Function automatically converts it to miliseconds]
    """

    to_ms = float(time_in_seconds / 1000)
    print("Converting from '{}s' to '{}ms'".format(time_in_seconds, to_ms))
    time.sleep(to_ms)


def _showStrip():
    """[Arduino version of showStrip, taken from tweaking4all]
    """
    # print("Making pixel color changes active w/ 'pixels.show()'")
    # pixels.show()
    pass


def _setPixel(position, r, g, b):
    """[Arduino version of setPixel(), taken from tweaking4all]

    Arguments:
        position {int} -- [description]
        r {int} -- [description]
        g {int} -- [description]
        b {int} -- [description]
    """
    print("INSIDE: BEFORE (int) cast _setPixel: r={}, g={}, b={}".format(r, g, b))

    if type(r) == float:
        r = int(r)

    if type(b) == float:
        b = int(b)

    if type(g) == float:
        g = int(g)

    print("INSIDE: AFTER (int) cast _setPixel: r={}, g={}, b={}".format(r, g, b))

    # _rgb = (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)
    # pixels[position] = _rgb
    # # time.sleep(0.1)
    pass


def _setAll(r, g, b):
    """[Arduino version of setAll(), taken from tweaking4all]

    Arguments:
        r {[type]} -- [description]
        g {[type]} -- [description]
        b {[type]} -- [description]
    """

    # FIXME: Temporarily disabled
    # for i in range(num_pixels):
    #     _setPixel(i, r, g, b)
    # _showStrip()

    pass


def _FadeInOut(red, green, blue):
    """[LEDStrip Effect – Fade In and Fade Out: Red, Green and Blue]
    """

    # _r = float(r)
    # _g = float(g)
    # _b = float(b)
    # In Python 3, relevant quotients are converted from integers to floats when doing division though they are not in Python 2. That is, when you divide 5 by 2, in Python 3 you will get a float for an answer (2.5)
    k = 0
    while k < 256:
        # for k in range(0, MAX_PIXEL_VALUE):
        print("BEFORE - INSIDE: _FadeInOut FIRST LOOP: k={}".format(k))
        print(
            "BEFORE - INSIDE: _FadeInOut FIRST LOOP: red={}, green={}, blue={}".format(
                red, green, blue
            )
        )

        r = float((k / 256.0) * red)
        g = float((k / 256.0) * green)
        b = float((k / 256.0) * blue)
        print(
            "AFTER - INSIDE: _FadeInOut FIRST LOOP: red={}, green={}, blue={}".format(
                red, green, blue
            )
        )
        print("AFTER - INSIDE: _FadeInOut FIRST LOOP: r={}, g={}, b={}".format(r, g, b))
        _setAll(r, g, b)
        _showStrip()
        k = k + 1

    k = 255
    while k >= 0:
        # for k in range(MAX_PIXEL_VALUE-1,0,-2):

        r = float((k / 256.0) * red)
        g = float((k / 256.0) * green)
        b = float((k / 256.0) * blue)
        print("INSIDE: _FadeInOut SECOND LOOP: r={}, g={}, b={}".format(r, g, b))
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

            print(
                "INSIDE: _RunningLights SECOND LOOP: r={}, g={}, b={}".format(r, g, b)
            )

            _setPixel(j, r, g, b)

            j = j + 1

        _showStrip()
        _delay(WaveDelay)
        i = i + 1


if __name__ == "__main__":
    _RunningLights(0xff, 0xff, 0x00, 5)
