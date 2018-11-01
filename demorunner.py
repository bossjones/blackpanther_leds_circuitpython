import gc
import sys
import board
import time

# import demos
import nightlight

import rainbowdemo

# import blinkdemo
from buttonwatcher import ButtonWatcher

# FIXME: This import is causing 'MemoryError: memory allocation failed, allocating %u bytes'
# import left_chest
import exceptions


index = 0
demos = [
    # left_chest.FlashDemo(),
    nightlight.NightLight(),
    # blinkdemo.FlashDemo(),
    # rainbowdemo.RainbowDemo(),
    # rainbowdemo.RainbowCycleDemo(),
    # blinkdemo.BlinkDemo(),
    # demos.TouchDemo(),
]

currentDemo = demos[index]
demos[index].start()

buttonA = ButtonWatcher(board.BUTTON_A)
buttonB = ButtonWatcher(board.BUTTON_B)

try:
    while True:
        previousIndex = index

        if buttonA.wasPressed():
            index += 1
        if buttonB.wasPressed():
            index -= 1

        index %= len(demos)

        if previousIndex != index:
            for demo in demos:
                demo.stop()
            currentDemo = demos[index]
            currentDemo.start()

        currentDemo.next()
        time.sleep(0.001)
except MemoryError as error:
    # Output unexpected MemoryErrors.
    sys.print_exception(error)
    raise
except RuntimeError as error:
    # Output unexpected RuntimeError.
    sys.print_exception(error)
    raise
except KeyboardInterrupt as exception:
    pass
