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
simpleCircleDemo = False
flashDemo = False
rainbowDemo = False
rainbowCycleDemo = True
touchDemo = False

# NOTE: This works as well, other one below has more debugging info
# def wheel(pos):
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if pos < 85:
#         return (int(pos*3), int(255 - (pos*3)), 0)
#     elif pos < 170:
#         pos -= 85
#         return (int(255 - (pos*3)), 0, int(pos*3))
#     else:
#         pos -= 170
#         return (0, int(pos*3), int(255 - pos*3))

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    # ORIG
    # if pos < 85:
    #     rgb = (int(pos*3), int(255 - (pos*3)), 0)
    #     print("Inside: pos < 85 ... rgb = '{}'".format(rgb))
    #     return rgb
    # elif pos < 170:
    #     pos -= 85
    #     rgb = (int(255 - (pos*3)), 0, int(pos*3))
    #     print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
    #     return rgb
    # else:
    #     pos -= 170
    #     rgb = (0, int(pos*3), int(255 - pos*3))
    #     print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
    #     return rgb
    if pos < 85:
        rgb = (int(255 - (pos*3)), 0, int(255 - (pos*3)))
        print("Inside: pos < 85 ... rgb = '{}'".format(rgb))
        return rgb
    elif pos < 170:
        pos -= 85
        rgb = (0, 0, 0)
        print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
        return rgb
    else:
        pos -= 170
        rgb = (int(pos*3), 0, int(pos*3))
        print("Inside: pos < 170 ... pos = '{}' rgb = '{}'".format(pos, rgb))
        return rgb

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


# while True:
#     time.sleep(0.01)
#     led.value = True
#     time.sleep(0.02)
#     led.value = False
#     time.sleep(0.1)

#     if rainbowDemo:
#         print('BlackPanther Purple Rainbow Demo')
#         rainbow(.001)

#     if rainbowCycleDemo:
#         print('BlackPanther Purple Rainbow Cycle Demo')
#         rainbow_cycle(.001)
