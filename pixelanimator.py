from nonblocking_timer import nonblocking_timer

# from simpleio import map_range
import board
import neopixel as NeoPixel

# import pixelanimator as PixelAnimator
import time


ORANGE = (255, 40, 0)
OFF = ORANGE


class PixelAnimator(nonblocking_timer):

    LINEAR = 0

    def __init__(self, pixels):
        # FIXME: 10/31/2018 I added this interval value 0.01
        super(PixelAnimator, self).__init__()
        self.pixels = pixels
        self.animator = self._getAnimator(PixelAnimator.LINEAR)
        print("PixelAnimator Demo: pixel count = %s" % len(self.pixels))

    def next(self):
        self.animator.next()

    def fill(self, color, interval, steps):
        self._color = color
        self.pixels.fill(color)

    def _getAnimator(self, animation_type):
        if animation_type == PixelAnimator.LINEAR:
            return _LinearAnimator(self.pixels, interval=1, steps=50)
        raise Exception("Unknown animator: %s" % animation_type)


class _LinearAnimator(nonblocking_timer):
    def __init__(self, pixels, interval=0, steps=0):
        super(_LinearAnimator, self).__init__(interval / float(steps))

        print("Class = '{}' func = '__init__' interval = '{}'\n".format(
            self.__qualname__, interval))

        if interval <= 0:
            raise Exception("Interval must be > 0")
        if steps <= 0:
            raise Exception("Steps must be > 0")
        self._steps = steps
        self._pixels = pixels
        self._color = OFF
        self._increasing = True
        self._currentColor = OFF
        self._currentStep = 0
        self._deltaColor = tuple(map(lambda x: x / float(steps), ORANGE))

    def next(self):
        if super(_LinearAnimator, self).next():
            if self._increasing:
                self._color = tuple(
                    map(lambda x, y: min(x + y, 255), self._color, self._deltaColor)
                )
            else:
                self._color = tuple(
                    map(lambda x, y: max(x - y, 0), self._color, self._deltaColor)
                )

            self._pixels.fill(tuple(map(lambda x: int(round(x)), self._color)))
            print("color: %s step: %s", self._color, self._currentStep)
            self._currentStep += 1
            if self._currentStep > self._steps:
                self._currentStep = 0
                self._increasing = not self._increasing
