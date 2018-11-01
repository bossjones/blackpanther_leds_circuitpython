import gc

import time
# gc.collect()
import board
gc.collect()
import sys
gc.collect()
# import demos
# import nightlight
# gc.collect()
# import rainbowdemo
# gc.collect()

import left_chest
gc.collect()

# import blinkdemo
from buttonwatcher import ButtonWatcher
gc.collect()

index = 0
demos = [
    left_chest.LeftUnit(),
    # nightlight.NightLight(),
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
    sys.print_exception(error)  # pylint: disable=E1101
    raise
except RuntimeError as error:
    # Output unexpected RuntimeError.
    sys.print_exception(error)  # pylint: disable=E1101
    raise
except KeyboardInterrupt as exception:
    pass
