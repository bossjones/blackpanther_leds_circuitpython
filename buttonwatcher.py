import board
import digitalio
import time

# import touchio
import neopixel
import math
from digitalio import DigitalInOut, Direction, Pull


class ButtonWatcher:
    def __init__(self, pin):
        self._button = DigitalInOut(pin)
        self._button.direction = Direction.INPUT
        self._button.pull = Pull.DOWN
        self._value = False

        # Turn off power light
        self.green_light = DigitalInOut(board.D13)
        self.green_light.value = False

    def wasPressed(self):
        previousValue = self._value
        self._value = self._button.value
        if self._value and not (previousValue):
            return True
        return False
