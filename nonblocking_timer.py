# The MIT License (MIT)
#
# Copyright (c) 2017 Michael Schneider
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`nonblocking_timer`
====================================================

.. This class allows easier usage of time.monotonic() in CircuitPython to keep
   track of timers without using making a blocking call to time.sleep().

   Example:


class BlinkDemo(nonblocking_timer):
  def __init__(self):
    super(BlinkDemo, self).__init__(0.1)
    self.led = digitalio.DigitalInOut(board.D13)
    self.led.direction = digitalio.Direction.OUTPUT
    self.value = True

  def stop(self):
    self.led.value = False

  def next(self):
    if (super(BlinkDemo, self).next()):
      self.led.value = not (self.led.value)

blinkdemo.BlinkDemo()

while True:
  blinkDemo.next()
  # This is the only place you should use time.sleep: to set the overall
  # "sampling rate" of your program.
  time.sleep(0.001)

* Author(s): Michael Schneider
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/mikepschneider/CircuitPython_nonblocking_timer.git"


import time


class nonblocking_timer(object):
    """ Non blocking timer class for use with CircuitPython """

    _STOPPED = "STOPPED"
    _RUNNING = "RUNNING"

    def __init__(self, interval=-1):
        """
        Create a new timer with optional interval.
        Initial state is _STOPPED.
        Call start() to set status to _RUNNING.
        """
        print(
            "Class = '{}' func = '__init__' __init__.interval = '{}'\n".format(
                self.__qualname__, interval
            )
        )
        self._interval = interval
        self._status = nonblocking_timer._STOPPED
        self._start_time = 0

    @property
    def status(self):
        return self._status

    def next(self):
        """ Returns true or false according to the following algorithm:

      if interval <= 0 raise RuntimeError
      if status != _RUNNING raise RuntimeError
      if time.monotonic() - start_time > interval
        return True and set start_time = time.monotonic()
      else return False
    """

        if self._interval <= 0:
            print(
                "Class = '{}' func = 'next' __init__.interval = '{}'\n".format(
                    self.__qualname__, self._interval
                )
            )
            raise RuntimeError("Interval must be > 0")

        if self._status != nonblocking_timer._RUNNING:
            # print("Class = '{}' func = 'next' self._status = '{}' nonblocking_timer._RUNNING = '{}' message = 'Timer must be in state _RUNNING before calling next()'\n".format(
            #     self.__qualname__, self._status, nonblocking_timer._RUNNING))
            # raise RuntimeError("Timer must be in state _RUNNING before calling next()")
            raise RuntimeError(
                "Class = '{}' func = 'next' self._status = '{}' nonblocking_timer._RUNNING = '{}' message = 'Timer must be in state _RUNNING before calling next()'\n".format(
                    self.__qualname__, self._status, nonblocking_timer._RUNNING
                )
            )

        current_time = time.monotonic()
        elapsed = current_time - self._start_time

        if elapsed >= self._interval:
            # The timer has been "triggered"
            self._start_time = current_time
            return True

        return False

    def stop(self):
        """Sets status to _STOPPED. Do any cleanup here such as releasing pins,
       etc. Call start() to restart. Does not reset current time."""
        self._status = nonblocking_timer._STOPPED

    def start(self):
        """Sets status to _RUNNING. Sets start_time to time.monotonic(). Call
       next() repeatedly to determine if the timer has been triggered.
       If interval <= 0 raise a RuntimeError """
        if self._interval <= 0:
            print(
                "Class = '{}' func = 'start' self._interval = '{}'\n".format(
                    self.__qualname__, self._interval
                )
            )
            raise RuntimeError("Interval must be > 0")

        self._start_time = time.monotonic()
        self._status = nonblocking_timer._RUNNING

    def set_interval(self, seconds):
        """ Set the trigger interval time in seconds (float). If interval <= 0
        raise a RuntimeError """
        if seconds <= 0:
            print(
                "Class = '{}' func = 'set_interval' seconds = '{}'\n".format(
                    self.__qualname__, seconds
                )
            )
            raise RuntimeError(
                "Debug: func = 'set_interval' msg = 'Seconds interval must be > 0'"
            )
        self._interval = seconds

    def get_interval(self):
        return self._interval
