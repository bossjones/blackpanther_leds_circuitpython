from nonblocking_timer import nonblocking_timer
from pixelanimator import PixelAnimator

import board

# from board import *

import neopixel
from digitalio import DigitalInOut, Direction

# from analogio import AnalogIn


class NightLight(nonblocking_timer):
    def __init__(self):
        # FIXME: 10/31/2018 I added this interval value 0.01
        super(NightLight, self).__init__(0.1)
        pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=1, brightness=1.0)
        pixels.fill((0, 0, 0))
        pixels.show()
        self._on = False
        self._animator = PixelAnimator(pixels)

        # self._irSensor = AnalogIn(board.IR_PROXIMITY)

        # self._irInput = DigitalInOut(board.REMOTEIN)
        # self._irInput.direction = Direction.INPUT

        # self._irOutput = DigitalInOut(board.REMOTEOUT)
        # self._irOutput.direction = Direction.OUTPUT

        # self._microphone = DigitalInOut(board.MICROPHONE_DATA)
        # self._irOutput.direction = Direction.INPUT

    def stop(self):
        print("stop")
        # self._irSensor.deinit()
        # self._irInput.deinit()

    def next(self):
        # print("ir: %d mic: %d" % (self._irSensor.value, self._irOutput.value))

        self._animator.next()
