import board
import digitalio
from nonblocking_timer import nonblocking_timer
from digitalio import DigitalInOut, Direction, Pull
import neopixel
import touchio

RED = 0x100000  # (0x10, 0, 0) also works
YELLOW = (0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
AQUA = (0, 0x10, 0x10)
BLUE = (0, 0, 0x10)
PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)

COLORS = [RED, YELLOW, GREEN, AQUA, BLUE, PURPLE, BLACK]


class RainbowCycleDemo(nonblocking_timer):
    def __init__(self):
        super(RainbowCycleDemo, self).__init__(1)
        self._on = True
        self._pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
        self._ring = neopixel.NeoPixel(board.A1, 32, brightness=.5)
        self._pixels.fill(PURPLE)
        self._ring.fill(RED)
        self._count = 0

    def next(self):
        if super(RainbowCycleDemo, self).next():
            self._on = not self._on
            if self._on:
                self._pixels.fill(AQUA)
                self._ring.fill(AQUA)
            else:
                self._pixels.fill(YELLOW)
                self._ring.fill(PURPLE)
