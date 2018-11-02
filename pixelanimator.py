from nonblocking_timer import nonblocking_timer

PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)
OFF = BLACK
BLACK_PANTHER_PURPLE = (198, 0, 224)  # rgb(198, 0, 224)

# FIXME: Move this into the pixelanimator.py when verified
class PixelAnimatorNG(nonblocking_timer):

    LINEAR = 0
    RUNNINGLIGHTS = 1
    COLORWIPE = 2

    def __init__(self, pixels):
        super(PixelAnimatorNG, self).__init__()
        self.pixels = pixels
        self.animator = self._getAnimator(PixelAnimatorNG.COLORWIPE)
        # self.animator = self._getAnimator(PixelAnimatorNG.LINEAR)
        self.animator.start()
        print("PixelAnimatorNG Demo: pixel count = %s" % len(self.pixels))

    def next(self):
        self.animator.next()

    #
    #   def fill(self, color, interval, steps):
    #     self._color = color
    #     self.pixels.fill(color)

    #   def _setPixel(self, position, r, g, b):
    #     """[Arduino version of setPixel(), taken from tweaking4all]

    #     Arguments:
    #         position {int} -- [description]
    #         r {int} -- [description]
    #         g {int} -- [description]
    #         b {int} -- [description]
    #     """
    #     self.pixels[position] = tuple(
    #         map(lambda x: int(x) if isinstance(x, float) else x, [r, g, b]))

    #   def _setAll(self, r, g, b):
    #     """[Arduino version of setAll(), taken from tweaking4all]

    #     Arguments:
    #         r {[type]} -- [description]
    #         g {[type]} -- [description]
    #         b {[type]} -- [description]
    #     """

    #     for i in range(len(self.pixels)):
    #         self._setPixel(i, r, g, b)
    #     self.pixels.show()

    def _getAnimator(self, animation_type):
        if animation_type == PixelAnimatorNG.LINEAR:
            #   return _RunningLightsAnimator(self.pixels, interval=1, steps=50)
            # return _LinearAnimator(self.pixels, interval=1, steps=50)
            raise Exception(
                "Not implemented animator: {}".format(animation_type))
        # elif animation_type == PixelAnimatorNG.RUNNINGLIGHTS:
        #     return _RunningLightsAnimator(self.pixels, interval=1)
        elif animation_type == PixelAnimatorNG.COLORWIPE:
            return _ColorWipeAnimator(self.pixels, interval=1)
        raise Exception("Unknown animator: {}".format(animation_type))


# class _RunningLightsAnimator(nonblocking_timer):

#     RESET_POSITION = 0
#     INCREMENT_POSITION = 1
#     STAY_AT_POSITION = 2

#     def __init__(self, pixels, interval=0):
#         # super(_RunningLightsAnimator, self).__init__(interval / float(steps))
#         super(_RunningLightsAnimator, self).__init__(interval / float(50))

#         print(
#             "Class = '{}' func = '__init__' interval = '{}'\n".format(
#                 self.__qualname__, interval
#             )
#         )

#         if interval <= 0:
#             raise Exception("Interval must be > 0")
#         # if steps <= 0:
#         #     raise Exception("Steps must be > 0")
#         self._pixels = pixels

#         self._num_pixels = len(self._pixels)
#         self._current_pixel = 0  # think j = 0 in runningLights
#         self._position_state = _RunningLightsAnimator.STAY_AT_POSITION
#         self._position = 0  # think position
#         self._double_num_pixels = len(self._pixels) * 2

#         # self._steps = len(self._pixels)
#         # self._color = OFF
#         # self._increasing = True
#         # self._currentColor = OFF
#         # self._currentStep = 0  # same as position
#         # self._deltaColor = tuple(map(lambda x: x / float(steps), ORANGE))

#     def performSinMath(self, color_tuple):
#         red, green, blue = color_tuple

#         r = ((math.sin(self._current_pixel + self._position) * 127 + 128) / 255) * red
#         g = ((math.sin(self._current_pixel + self._position) * 127 + 128) / 255) * green
#         b = ((math.sin(self._current_pixel + self._position) * 127 + 128) / 255) * blue

#         print(
#             "Class = '{}' func = 'performSinMath' r = '{}' g = '{}' b = '{}'\n".format(
#                 self.__qualname__, r, g, b
#             )
#         )

#         # basically the same as this _setPixel(j, r, g, b, device=device)
#         return tuple(map(lambda x: int(x) if isinstance(x, float) else x, [r, g, b]))

#     def next(self):
#         print(
#             "Class = '{}' func = 'next' self._position_state = '{}' self._position = '{}' self._current_pixel = '{}'\n".format(
#                 self.__qualname__,
#                 self._position_state,
#                 self._position,
#                 self._current_pixel,
#             )
#         )

#         # Step 1: Check if we move to position++ or do we stay where we are at
#         if self._position_state == _RunningLightsAnimator.STAY_AT_POSITION:
#             # print("step1: check if we move to position++ or do we stay where we are at")

#             # step2: Check if position value (self._position < self._double_num_pixels) or (0 < DOUBLE_NUM_PIXELS)
#             if self._position < self._double_num_pixels:
#                 # print(
#                 #     "step2: Check if position value (self._position < self._double_num_pixels) or (0 < DOUBLE_NUM_PIXELS)"
#                 # )

#                 # step3: check if (_current_pixel < num_pixels) AKA (j < num_pixels)
#                 if self._current_pixel < len(self._pixels):
#                     # print(
#                     #     "step3: check if (_current_pixel < num_pixels) AKA (j < num_pixels)"
#                     # )

#                     self._pixels[self._current_pixel] = self.performSinMath(PURPLE)

#                     self._pixels.show()

#                     print(
#                         "Class = '{}' func = 'next' self._current_pixel = '{}' self._pixels[self._current_pixel] = '{}'\n".format(
#                             self.__qualname__,
#                             self._current_pixel,
#                             self._pixels[self._current_pixel],
#                         )
#                     )

#                     # print("-------------------------")
#                     # dump(self)
#                     # print("-------------------------")

#                     # print("color: %s step: %s", self._color, self._currentStep)
#                     # j = j + 1
#                     self._current_pixel = self._current_pixel + 1
#                 else:
#                     # print(
#                     #     "step4: since we've hit 'len(self._pixels)' RUN: self._position = self._position + 1"
#                     # )
#                     self._position_state = _RunningLightsAnimator.INCREMENT_POSITION
#                     self._position = self._position + 1
#                     self._position_state = _RunningLightsAnimator.STAY_AT_POSITION

#             # If we've done more than double the number of pixels worth of animation, reset back to 0
#             else:
#                 # print(
#                 #     "If we've done more than double the number of pixels worth of animation, reset back to 0"
#                 # )
#                 self._position_state = _RunningLightsAnimator.RESET_POSITION
#                 self._position = 0
#                 self._position_state = _RunningLightsAnimator.STAY_AT_POSITION
#                 self._current_pixel = 0


#         # if super(_RunningLightsAnimator, self).next():
#         #     if self._increasing:
#         #         self._color = tuple(
#         #             map(lambda x, y: min(x + y, 255),
#         #                 self._color, self._deltaColor)
#         #         )
#         #     else:
#         #         self._color = tuple(
#         #             map(lambda x, y: max(x - y, 0),
#         #                 self._color, self._deltaColor)
#         #         )

#         #     self._pixels.fill(tuple(map(lambda x: int(round(x)), self._color)))
#         #     print("color: %s step: %s", self._color, self._currentStep)
#         #     self._currentStep += 1
#         #     if self._currentStep > self._steps:
#         #         self._currentStep = 0
#         #         self._increasing = not self._increasing

class _ColorWipeAnimator(nonblocking_timer):
    def __init__(self, pixels, interval=0):
        super(_ColorWipeAnimator, self).__init__(interval)

        print(
            "Class = '{}' func = '__init__' interval = '{}'\n".format(
                self.__qualname__, interval
            )
        )

        if interval <= 0:
            raise Exception("Interval must be > 0")

        self._pixels = pixels
        self._num_pixels = len(self._pixels)
        self._current_pixel = 0
        self._color = PURPLE
        self._color_choices = [PURPLE, BLACK]
        self._color_state = 0  # purple by default(low), black when(high)

    def next(self):
        print(
            "Class = '{}' func = 'next' self._current_pixel = '{}' self._color = '{}' self._color_state = '{}'\n".format(
                self.__qualname__,
                self._current_pixel,
                self._color,
                self._color_state,
            )
        )

        # Iterate through each position on the neopixel strip or Circuit Playground Express, and set a color
        if self._current_pixel < self._num_pixels:

            # Set current pixel value to self._color. Options [PURPLE, BlACK]
            self._pixels[self._current_pixel] = tuple(
                map(lambda x: int(x) if isinstance(x, float) else x, [self._color[0], self._color[1], self._color[2]]))
            self._pixels.show()

            self._current_pixel += 1

        # Colorwipe back to black
        else:
            self._color_state = (self._color_state + 1) % 2
            self._color = self._color_choices[self._color_state]
            self._current_pixel = 0

    def stop(self):
        self._pixels.fill((0, 0, 0))
        self._pixels.show()


# class _LinearAnimator(nonblocking_timer):
#   def __init__(self, pixels, interval=0, steps=0):
#     super(_LinearAnimator, self).__init__(interval / float(steps))
#     # if interval <= 0:
#     #     raise Exception('Interval must be > 0')
#     # if steps <= 0:
#     #     raise Exception('Steps must be > 0')
#     self._steps = steps
#     self._pixels = pixels
#     self._color = OFF
#     self._increasing = True
#     self._currentColor = OFF
#     self._currentStep = 0
#     self._deltaColor = tuple(map(lambda x: x / float(steps), BLACK_PANTHER_PURPLE))

#   def next(self):
#     if (super(_LinearAnimator, self).next()):
#       if self._increasing:
#         self._color = tuple(
#             map(lambda x, y: min(x + y, 255),
#                 self._color, self._deltaColor))
#       else:
#         self._color = tuple(
#             map(lambda x, y: max(x - y, 0),
#                 self._color, self._deltaColor))

#       self._pixels.fill(tuple(
#           map(lambda x: int(round(x)), self._color)))
#       self._pixels.show()
#       print("color: %s step: %s", self._color, self._currentStep)
#       self._currentStep += 1
#       if (self._currentStep > self._steps):
#         self._currentStep = 0
#         self._increasing = not self._increasing
