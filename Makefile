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
