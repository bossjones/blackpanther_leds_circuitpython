# DEVICENAME := /dev/tty.usbmodem14101
DEVICENAME := $(shell ls /dev/tty.*| grep "tty.usbmodem" | awk '{print $1}')
BAUD_RATE := 115200

list-serial-devices:
	ls /dev/tty.*

connect-to-repl:
	screen $(DEVICENAME) $(BAUD_RATE)

repl: connect-to-repl

debug:
	@echo "DEVICENAME $(DEVICENAME)"
	@echo "BAUD_RATE $(BAUD_RATE)"

cp-screenrc:
	cp ./contrib/.screenrc ~/.screenrc

cp-to-device:
	rsync --verbose --update nonblocking_timer.py /Volumes/CIRCUITPY/
	rsync --verbose --update left_chest.py /Volumes/CIRCUITPY/
	rsync --verbose --update buttonwatcher.py /Volumes/CIRCUITPY/
	rsync --verbose --update demorunner.py /Volumes/CIRCUITPY/
	rsync --verbose --update helloworld.py /Volumes/CIRCUITPY/
	rsync --verbose --update debugger.py /Volumes/CIRCUITPY/
	rsync --verbose --update nightlight.py /Volumes/CIRCUITPY/
	rsync --verbose --update pixelanimator.py /Volumes/CIRCUITPY/
	rsync --verbose --update rainbowdemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update blinkdemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update simpledemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update animation_utils.py /Volumes/CIRCUITPY/
	rsync --verbose --update code.py /Volumes/CIRCUITPY/
	@df -H /Volumes/CIRCUITPY/

rm-device:
	rm -fv /Volumes/CIRCUITPY/nonblocking_timer.py
	rm -fv /Volumes/CIRCUITPY/left_chest.py
	rm -fv /Volumes/CIRCUITPY/buttonwatcher.py
	rm -fv /Volumes/CIRCUITPY/demorunner.py
	rm -fv /Volumes/CIRCUITPY/helloworld.py
	rm -fv /Volumes/CIRCUITPY/debugger.py
	rm -fv /Volumes/CIRCUITPY/nightlight.py
	rm -fv /Volumes/CIRCUITPY/pixelanimator.py
	rm -fv /Volumes/CIRCUITPY/rainbowdemo.py
	rm -fv /Volumes/CIRCUITPY/blinkdemo.py
	rm -fv /Volumes/CIRCUITPY/animation_utils.py
	rm -fv /Volumes/CIRCUITPY/simpledemo.py

clean: rm-device
