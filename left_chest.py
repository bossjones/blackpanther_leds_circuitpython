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


class LeftUnit(nonblocking_timer):
    # NOTE: The interval here controls the speed at which the whole animation moves at
    # Interval suggestions:
    #   default: 0.25
    #   slow: 1
    def __init__(self, interval=0.09):
        super(LeftUnit, self).__init__(interval)
        self._left_chest_pixels = neopixel.NeoPixel(
            board.NEOPIXEL, 10, auto_write=False, pixel_order=neopixel.GRB
        )
        self._left_chest_pixels.fill((0, 0, 0))
        self._left_chest_pixels.show()
        self._left_chest_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._left_chest_animator = pixelanimator.PixelAnimatorNG(self._left_chest_pixels)
        # self._left_chest_animator.start()

        # # ------- Left rib unit ------------------
        self._left_rib_pixels = neopixel.NeoPixel(
            board.A7,
            8,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._left_rib_pixels.fill((0, 0, 0))
        self._left_rib_pixels.show()
        self._left_rib_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._left_rib_animator = pixelanimator.PixelAnimatorNG(
            self._left_rib_pixels)
        # self._left_rib_animator.start()

        # # ------- Left abs unit ------------------
        self._left_abs_pixels = neopixel.NeoPixel(
            # board.A2,
            board.A5,
            8,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._left_abs_pixels.fill((0, 0, 0))
        self._left_abs_pixels.show()
        self._left_abs_pixels_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._left_abs_animator = pixelanimator.PixelAnimatorNG(self._left_abs_pixels)

        #########################################################################
        # New units that might cause a memory issue
        #########################################################################

        # # ------- Left upper_arm unit ------------------
        self._left_upper_arm_pixels = neopixel.NeoPixel(
            board.A6,
            8,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._left_upper_arm_pixels.fill((0, 0, 0))
        self._left_upper_arm_pixels.show()
        self._left_upper_arm_pixels_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._left_upper_arm_animator = pixelanimator.PixelAnimatorNG(
            self._left_upper_arm_pixels)

        # # ------- Left elbow unit ------------------
        self._left_elbow_pixels = neopixel.NeoPixel(
            board.A1,
            8,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._left_elbow_pixels.fill((0, 0, 0))
        self._left_elbow_pixels.show()
        self._left_elbow_pixels_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._left_elbow_animator = pixelanimator.PixelAnimatorNG(
            self._left_elbow_pixels)

        # # ------- Left center unit ------------------
        self._left_center_pixels = neopixel.NeoPixel(
            board.A4,
            16,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._left_center_pixels.fill((0, 0, 0))
        self._left_center_pixels.show()
        self._left_center_pixels_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._left_center_animator = pixelanimator.PixelAnimatorNG(
            self._left_center_pixels)

        # # ------- Left thigh unit ------------------
        self._left_thigh_pixels = neopixel.NeoPixel(
            board.A3,
            11,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self._left_thigh_pixels.fill((0, 0, 0))
        self._left_thigh_pixels.show()
        self._left_thigh_pixels_index = 0
        # FIXME: NOTE, we might need to make these local variables only, based on NightLight example
        self._left_thigh_animator = pixelanimator.PixelAnimatorNG(
            self._left_thigh_pixels)

    def next(self):
        if super(LeftUnit, self).next():
            self._left_chest_animator.next()
            self._left_rib_animator.next()
            self._left_abs_animator.next()

            #########################################################################
            # New units that might cause a memory issue
            #########################################################################
            self._left_upper_arm_animator.next()
            self._left_elbow_animator.next()
            self._left_center_animator.next()
            self._left_thigh_animator.next()

    def stop(self):
        self._left_chest_pixels.fill(BLACK)
        self._left_chest_pixels.show()

        self._left_rib_pixels.fill(BLACK)
        self._left_rib_pixels.show()

        self._left_abs_pixels.fill(BLACK)
        self._left_abs_pixels.show()

        #########################################################################
        # New units that might cause a memory issue
        #########################################################################
        self._left_upper_arm_pixels.fill(BLACK)
        self._left_upper_arm_pixels.show()

        self._left_elbow_pixels.fill(BLACK)
        self._left_elbow_pixels.show()

        self._left_center_pixels.fill(BLACK)
        self._left_center_pixels.show()

        self._left_thigh_pixels.fill(BLACK)
        self._left_thigh_pixels.show()
