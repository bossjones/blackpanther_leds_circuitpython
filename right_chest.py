import gc
import micropython  # pylint: disable=E0401
gc.collect()
import board
gc.collect()
from nonblocking_timer import nonblocking_timer
gc.collect()
import neopixel
gc.collect()
# import math
# gc.collect()
import pixelanimator
gc.collect()

# import digitalio
# gc.collect()

PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)
OFF = BLACK

def memorySnapshot(location=None):
    print("\n------memorySnapshot-----")
    if location:
        print("Location: {}\n".format(location))

    # pylint: disable=E1101
    print("Free memory: {} bytes".format(
        gc.mem_free()))  # pylint: disable=E1101
    print("Allocated memory: {} bytes".format(
        gc.mem_alloc()))  # pylint: disable=E1101
    print("Stack Use: {}".format(micropython.stack_use()))  # pylint: disable=E1101
    print("Memory Info:")  # pylint: disable=E1101
    print("-----------------------------")
    micropython.mem_info(1)
    print("-----------------------------")
    print("\n")


# def dump(obj):
#     for attr in dir(obj):
#         if hasattr(obj, attr):
#             print("obj.{} = {}".format(attr, getattr(obj, attr)))


class RightUnit(nonblocking_timer):
    # NOTE: The interval here controls the speed at which the whole animation moves at
    # Interval suggestions:
    #   default: 0.25
    #   slow: 1
    def __init__(self, interval=0.09):
        super(RightUnit, self).__init__(interval)

        self._right_chest_pixels = neopixel.NeoPixel(
            board.NEOPIXEL, 10, auto_write=False, pixel_order=neopixel.GRB
        )
        self._right_chest_pixels.fill((0, 0, 0))
        self._right_chest_pixels.show()
        self._right_chest_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._right_chest_animator = pixelanimator.PixelAnimatorNG(self._right_chest_pixels)
        # self._right_chest_animator.start()

        # # ------- Right rib unit ------------------
        self._right_rib_pixels = neopixel.NeoPixel(
            board.A7,
            8,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._right_rib_pixels.fill((0, 0, 0))
        self._right_rib_pixels.show()
        self._right_rib_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._right_rib_animator = pixelanimator.PixelAnimatorNG(
            self._right_rib_pixels)
        # self._right_rib_animator.start()

        # # ------- Right abs unit ------------------
        self._right_abs_pixels = neopixel.NeoPixel(
            # board.A2,
            board.A5,
            7,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._right_abs_pixels.fill((0, 0, 0))
        self._right_abs_pixels.show()
        self._right_abs_pixels_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._right_abs_animator = pixelanimator.PixelAnimatorNG(self._right_abs_pixels)

        #########################################################################
        # New units that might cause a memory issue
        #########################################################################

        # # ------- Right upper_arm unit ------------------
        self._right_upper_arm_pixels = neopixel.NeoPixel(
            board.A6,
            8,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._right_upper_arm_pixels.fill((0, 0, 0))
        self._right_upper_arm_pixels.show()
        self._right_upper_arm_pixels_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._right_upper_arm_animator = pixelanimator.PixelAnimatorNG(
            self._right_upper_arm_pixels)

        # # ------- Right elbow unit ------------------
        self._right_elbow_pixels = neopixel.NeoPixel(
            board.A1,
            8,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._right_elbow_pixels.fill((0, 0, 0))
        self._right_elbow_pixels.show()
        self._right_elbow_pixels_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._right_elbow_animator = pixelanimator.PixelAnimatorNG(
            self._right_elbow_pixels)

        # # ------- Right thigh unit ------------------
        self._right_thigh_pixels = neopixel.NeoPixel(
            board.A3,
            11,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._right_thigh_pixels.fill((0, 0, 0))
        self._right_thigh_pixels.show()
        self._right_thigh_pixels_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._right_thigh_animator = pixelanimator.PixelAnimatorNG(
            self._right_thigh_pixels)

    def next(self):
        if super(RightUnit, self).next():
            self._right_chest_animator.next()
            self._right_rib_animator.next()
            self._right_abs_animator.next()

            #########################################################################
            # New units that might cause a memory issue
            #########################################################################
            self._right_upper_arm_animator.next()
            self._right_elbow_animator.next()
            self._right_thigh_animator.next()

    def stop(self):
        self._right_chest_pixels.fill(BLACK)
        self._right_chest_pixels.show()

        self._right_rib_pixels.fill(BLACK)
        self._right_rib_pixels.show()

        self._right_abs_pixels.fill(BLACK)
        self._right_abs_pixels.show()

        #########################################################################
        # New units that might cause a memory issue
        #########################################################################
        self._right_upper_arm_pixels.fill(BLACK)
        self._right_upper_arm_pixels.show()

        self._right_elbow_pixels.fill(BLACK)
        self._right_elbow_pixels.show()

        self._right_thigh_pixels.fill(BLACK)
        self._right_thigh_pixels.show()
