# # code.py should be as small as possible. Other .py files
# # should be transpiled into .mpy format
# import helloworld
# import demorunner


import board
import digitalio
import time
import touchio
import neopixel
import math
from digitalio import DigitalInOut, Direction, Pull

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT


pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0, 0, 0))
pixels.show()

#choose which demos to play
# 1 means play, 0 means don't!
rainbowDemo = False
rainbowCycleDemo = True

# 0 = rgb(255, 0, 0)
#
# NOTE: RED WHEEL ONLY
# def wheel(pos):
#     # print("func = 'wheel' pos='{}'".format(pos))
#     # pos = 255 - pos
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if pos < 85:
#         # 0 = rgb(0,0,0)
#         # 1 = rgb(252,0,0)
#         # 84 = rgb(3, 0, 0)
#         rgb = (int(255 - (pos*3)), 0, 0)
#         # print("Inside: pos < 85 ... pos = '{}' rgb = 'rgb{}'".format(pos, rgb))
#         print("rgb{}".format(rgb))
#         return rgb
#     elif pos < 170:
#         # 85 = rgb(0,0,0)
#         # 170 = rgb(0,0,0)
#         # print("Inside: BEFORE pos -=85 pos < 170 ... pos = '{}'".format(pos))
#         pos -= 85
#         rgb = (0, 0, 0)
#         # print("Inside: AFTER pos -=85 pos < 170 ... pos = '{}' rgb = 'rgb{}'".format(pos, rgb))
#         print("rgb{}".format(rgb))
#         return rgb
#     else:
#         # 171 = rgb(3, 0, 0)
#         # 255 = rgb(255, 0, 0) # NOTE: 255 becomes 85
#         # print("Inside: BEFORE pos -= 170 ... pos > 170 ... pos = '{}'".format(pos))
#         pos -= 170
#         rgb = (int(pos*3), 0, 0)
#         # print("Inside: AFTER pos > 170 ... pos = '{}' rgb = 'rgb{}'".format(pos, rgb))
#         print("rgb{}".format(rgb))
#         return rgb


# 13 = (39, 0, 0)
# high color rgb(208,0,255)

# 1. first find what the high value for red is, what gives us rgb(255, 0, 0)
# 2. Next plug that value in, then determine what our high will be for purple rgb(208,0,255)
# 3. Plug and play w/ values till we can figure out what gets us to the numer we care about

# PURPLE wheel
def wheel(pos):
    # print("func = 'wheel' pos='{}'".format(pos))
    # pos = 255 - pos
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 85:
        # 0 = rgb(0,0,0)
        # 1 = rgb(150, 0, 255)
        # 84 = rgb(3, 0, 0)
        # 79
        # 0 -> 84
        # pos += 15
        # red_offset =
        # blue_offset =
        # pos += 20
        pos += 34
        # offset = 34
        rgb = (int(255 - (pos*3)), 0, int(255 - (pos*3)))
        # print("Inside: pos < 85 ... pos = '{}' rgb = '{}'".format(pos, rgb))
        print("rgb{}".format(rgb))
        return rgb
    elif pos < 170:
        # 84 -> 169
        pos -= 85
        rgb = (0, 0, 0)
        # print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
        print("rgb{}".format(rgb))
        return rgb
    else:
        # 171 -> 255
        # pos -= 170
        # pos -= 155
        # 171 = rgb(3, 0, 0)
        # 255 = rgb(255, 0, 255) # NOTE: 255 becomes 85
        pos -= 170
        rgb = (int(pos*3), 0, int(pos*3))
        # print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
        print("rgb{}".format(rgb))
        return rgb

# purpleish
# rgb(184,38,174)
# rgb(128,0,128)

# NOTE: Adafruit rainbow
# def wheel(pos):
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if (pos < 0) or (pos > 255):
#         return (0, 0, 0)
#     if pos < 85:
#         return (int(pos * 3), int(255 - (pos * 3)), 0)
#     elif pos < 170:
#         pos -= 85
#         return (int(255 - pos * 3), 0, int(pos * 3))

#     pos -= 170
#     return (0, int(pos * 3), int(255 - pos * 3))


# def wheel(pos):
#     # print("func = 'wheel' pos='{}'".format(pos))
#     # pos = 255 - pos
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if pos < 85:
#         rgb = (int(255 - (pos*3)), 0, 0)
#         print("Inside: pos < 85 ... rgb = '{}'".format(rgb))
#         return rgb
#     elif pos < 170:
#         pos -= 85
#         rgb = (0, 0, 0)
#         print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
#         return rgb
#     else:
#         pos -= 170
#         rgb = (int(pos*3), 0, 0)
#         print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
#         return rgb

# def wheel(pos):
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if pos < 85:
#         # rgb = (int(pos*3), int(255 - (pos*3)), 0)
#         # rgb = (int(255 - (pos*3)), 0, int(255 - (pos*3)))
#         rgb = (int((pos*3)), 0, int((pos*3)))
#         print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
#         return rgb
#     elif pos < 170:
#         pos -= 85
#         rgb = (int(255 - (pos*3)), 0, int(255 - (pos*3)))
#         print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
#         return rgb
#     else:
#         pos -= 170
#         # rgb = (0, int(pos*3), 0)
#         rgb = (int((pos*3)), 0, int((pos*3)))
#         print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
#         return rgb

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int((i * 256 / len(pixels)) + j*10)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)


def rainbow(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i+j)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)


while True:
    time.sleep(0.01)
    led.value = True
    time.sleep(0.02)
    led.value = False
    time.sleep(0.1)

    if rainbowDemo:
        print('BlackPanther Purple Rainbow Demo')
        rainbow(.001)

    if rainbowCycleDemo:
        print('BlackPanther Purple Rainbow Cycle Demo')
        rainbow_cycle(.001)
        # rainbow_cycle(1)
