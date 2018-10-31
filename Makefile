DEVICENAME := /dev/tty.usbmodem14101
BAUD_RATE := 115200

list-serial-devices:
	ls /dev/tty.*

connect-to-repl:
	screen $(DEVICENAME) $(BAUD_RATE)

repl: connect-to-repl
