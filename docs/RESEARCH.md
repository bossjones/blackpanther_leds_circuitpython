# TODO: Try making things into classes

https://github.com/mikepschneider/circuitpy_ms/blob/1242a96171f5b436f53807b7a6893315022f292b/CIRCUITPY/demorunner.py

# How to read symbols from micropython.mem_info(1)

Symbol | Meaning
--- | ---
`.` | `free block`
`h` | `head block`
`=` | `tail block`
`m` | `marked head block`
`T` | `tuple`
`L` | `list`
`D` | `dict`
`F` | `float`
`B` | `byte code`
`M` | `module`

```
Each letter represents a single block of memory, a block being 16 bytes. So each line of the heap dump represents 0x400 bytes or 1KiB of RAM.
```

# Neopixel troubleshooting

```
NeoPixels are great when they work, but I’ve managed to create many circuits that didn’t.

They failed in every imaginable way — NeoPixels that wouldn’t turn on, NeoPixels that flickered, NeoPixels stuck on a color (blue seems to be my NeoPixels’ favorite) and — the most baffling of all — NeoPixels that worked when powered from one USB port, but not when powered from a different USB port.

Despite the wide range of symptoms, almost every one of these failures had the same underlying cause: powering NeoPixels with 5V, but connecting their data line to a 3.3V microcontroller.

The root of the problem here is that — according to the NeoPixel data sheets — the NeoPixel data line voltage (in logic-high state) has to be at least 0.7× the NeoPixel power voltage.

In other words, the power voltage has to be at most 1.43× of the data line voltage. Therefore, if the data line is at 3.3V, then the highest voltage you can put on the power line and still have a reliable NeoPixels is 1.43 × 3.3V = 4.71V.

As a result, if your NeoPixel power is close to 4.7V, the NeoPixels will be unreliable in interpreting its data line, resulting in flicker and random color changes.

Similarly, if your NeoPixel power is substantially higher than 4.7V, then the NeoPixels will not see any data on the data line, which will lead to it being stuck on black (for most NeoPixels) or blue (for some older NeoPixels).

Most notably, powering from USB (which provides 5V) does not work if your microcontroller logic is at 3.3V.
```

source: https://blog.adafruit.com/2016/10/28/tips-for-troubleshooting-neopixel-glitches/

source: https://ben.artins.org/electronics/glitchy-neopixels/


# Understanding heap dumps

```
The letters correspond to objects in the heap. The dots are free memory
(IIRC each dot corresponds to 16 bytes. To allocate 582 bytes, you'd need
37 consecutive dots.

The letters correspond to different types of objects in the heap. See:
/py/gc.c@master#L732-L742

Each object consists of one head block and 0-n tail blocks ('t')

On Tue, May 10, 2016 at 6:36 PM, Ryan Shaw notifications@github.com wrote:

What do the letters in the dump refer to?

Task NMEA composite dictionary generator took 116 us, mem free pre gc: 48800 B post gc: 48928 B, freed 128 B
Task NMEA strings parser took 1815 us, mem free pre gc: 47232 B post gc: 47744 B, freed 512 B
Task BaseTask took 138 us, mem free pre gc: 47616 B post gc: 47744 B, freed 128 B
Task File Downloader took 271 us, mem free pre gc: 47552 B post gc: 47744 B, freed 192 B
Task ____ REGISTRATION TASK took 202 us, mem free pre gc: 47616 B post gc: 47744 B, freed 128 B
Task __ MONITOR TASK took 153 us, mem free pre gc: 47616 B post gc: 47744 B, freed 128 B
Task IGNITION TASK took 142 us, mem free pre gc: 47616 B post gc: 47744 B, freed 128 B
Task BATTERY TASK took 148 us, mem free pre gc: 47616 B post gc: 47744 B, freed 128 B
PACKET TERMINATOR CLIPPED BY BUFFER, DROPPING
UNHANDLED EXCEPTION: Network Router Task
WARNING: Descheduling task

Traceback (most recent call last):
File "core/scheduler.py", line 83, in _run_next
File "softmodules/router.py", line 253, in run
File "softmodules/router.py", line 155, in rx_network
File "softmodules/router.py", line 49, in frame_packet
MemoryError: memory allocation failed, allocating 582 bytes
Traceback (most recent call last):
File "main.py", line 52, in
File "core/scheduler.py", line 55, in run
File "core/scheduler.py", line 93, in _run_next
File "core/scheduler.py", line 91, in _run_next
File "core/scheduler.py", line 83, in _run_next
File "softmodules/router.py", line 253, in run
File "softmodules/router.py", line 155, in rx_network
File "softmodules/router.py", line 49, in frame_packet
MemoryError: memory allocation failed, allocating 582 bytes
SYSTEM RESETTING IN LESS THAN 30 SECONDS

stack: 336 out of 15360
GC: total: 166400, used: 145840, free: 20560
No. of 1-blocks: 3433, 2-blocks: 434, max blk sz: 257
GC memory layout; from 20003600:
03600: MDhhhhhtttttttttttttttttttttttttttttttttttttththhhhBLLhhhhTLhhth
03a00: hMDhhhhhMDhtthththttDhhhtttttthhhhThLhhhhhhhhhhhhhhhhhhMDDhDDhhh
03e00: htttttttBhhhhtttttttthhhttttttthhtttttthhtttttTTTTThttttttthhttt
04200: tttthBLBhhhhhhThMDBBTBhhttttttttttttttttttttttttttttttttttthtthh
04600: ttttttthttttttthttttttttthhBtBtBhLFhDhhLhBBhttttttttTDhthDhDDhDh
04a00: tDhtDhththtDTthttttttthttttttttttDhtDhtDhtDhDhtDhDhtttLhtLhtttTD
04e00: hTDhTDhTDhTDhTDhTTTLhTThhhhLhhhhttttttththttttDDhhtttttttttttttt
05200: ttttttThthttttthhhhttTthhhTTTTThThtttttttttttttttthtttthLhhhhTTh
05600: ThhTTtTthttttttttttttttttttttttttttttttttttttttttttttttttttttttt
05a00: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
05e00: ttttttThhThhhttthDTTDDDLhDDhhhththhThTthhDLhhthhhhhhTthThTtTTTTh
06200: hThThhTthLhhhhTthhThThLhhtthhthhttttthtttttBhhBththttthhhthttttt
06600: ttttttttMDMThDBBBBBhBThhhttttttthttthLhtttThhhhthhMDDBBBBBBBBhtt
06a00: thtttthDBBThBhtthttthhtttttthThhtthtthtthtthttthtttthttthtththht
06e00: thTThhhThTtTthThhTtTthhhTtThTthTTThtthThttThhhTTtTtTTthTTthTTThT
07200: ThttttttDhhttttttttttttttttttttttthtthtDBhtttttttDTBBBhtttBBBBBB
07600: htttBhDhttttthttthDTDhhtttthttttttthtttThDhDTDLhhthhhhLhhhhhtttt
07a00: tttThhhDLhhthhtttTtTDhhhTDLhhDhtMDThhLhhhhTthhttttthtDDMDDDTthtD
07e00: BBThhBBhttttTThhttttttthttthhThBhthtttttttDhhhThtttttttttttttttt
08200: ttttthtttttttttttttttttttttttttttttttttttttttthThttthttththtttht
08600: ThhtttThtthtttTthTMhtthttThDLDhTDTthDhhLhhtthhhTthhttttDDhhttDTt
08a00: hhhhhBhthTThhLhhttthhhhhttthtthhhLhttttttthhhhThhhtttttthtDDhttT
08e00: ththhtthhtthhthhthhthhtthhthhthhtthhthhthhthhthhthhtttthhtttthhh
09200: LhhhhtthhhhtttttttttththhhhhhhhhhhTThhLhhhTThhttttthttDThhhttttt
09600: ttDDLDhhtDLhhthhttttttthtttttththtttttttMDhttttthTBBDTTtThtttttt
09a00: thtttTBBBBhthThThThLhhhttttttthhhttThtttttthttthhLhhhThttttttttT
09e00: hthhttttttDhhttDhMDhhtthDThhLhhhhhhhhDBTthLhhhhhhhhhhBhhhttTTBhh
0a200: TtDLhhhtttBBBhhttThttthTDhthttttththtttttLhDhtthttttttttttthtttt
0a600: ttthtthLhThThhttthttttthtthttttthttttttttttthttttttttttttttttttt
0aa00: ttttttthhthtthhttthhtthhhhttttthhhthhthtthhtttttttttttttttttthTt
0ae00: hhhttTthtTtMhhtLhhTLhttttttthtthhhhtttttttMDhhhthttDMhDhttThhttt
0b200: tttthtthTthhhthtthhtttttttttthtthTthDTTtTtBBTTTtTthhDTBBhttttttt
0b600: BThttthBBhDhttttttThttttttthttttttttThtthhhTthtthttttttthhttttth
0ba00: hthhtthtthhttttttthhhthttttthhtttttttthhhhhTtTttBBTTtTtTthtttTtB
0be00: htthhhttthttttTDTtTthtttttttTtTthhhBThhhBhTtTtTthttttttttttthttt
0c200: tttttttttttttttTthhttttthtttTtDBhthThttthhDBhtThhtBhThttThttthtt
0c600: TthttThttttttttttthttTthhthtthtthttthtttthhhttthttttththttthhttt
0ca00: tttttttthhhTthhThttttttthtthhDTThBhhtthttthttttttttThttthDhBThhh
0ce00: tthhhtthttttttthhttttttthtttDTBhThttThttthhttthtthhhhhTthhhtthhh
0d200: httTthhMDhttThDhhhhThhthhtttttttttttttttttttttttttttTthhhttBhTht
0d600: thhTthttTTtTthhhThTthhhhttthttthtthhhTththTtTthhhtthhhhhhhttMDht
0da00: tThhTthDBTthttTthttttttthhtthTthhhhhhhTtBBThtthhhhttBthDhDTBhTBh
0de00: hthtthttththttthDTBhththtttDBBBhhBhThDBhhhhtthhhhtthhhtthhhTthhh
0e200: tthhhTthtthhhttTthhthhhtttthhtttttthhhthttttttthhhthhhtthhtttttt
0e600: thhtttttttttttttttttttthtthhhhthhhhhhhhhhhhthhtthttttttttttttttt
0ea00: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
0ee00: ththhhThthtTthttttttthttthttthtttTBhtthhhhhthhhhhhhhhtthhhhttTth
0f200: hBTthhhttttttttttttBThhhhttthttthhhDThhTBTThhhBhhtttDThtttttttth
0f600: tthtttThttthDTBhBTtttBBBBTththhhtthhhhtthhBhBhTDhttttttttTBhTThh
0fa00: tttttttththhtthtttThhhttttttttttthttttttthtthhhttTttthhThhtthTth
0fe00: hhhDTtThhhTthttttttthtthhttttttttttthhhtthhhhhtthhhTthTthhhhtthh
10200: TTthhhhhhhthtthhhhthBhhthttthhDTBhThDTTBBhhttBhTthttttttthtttThD
10600: TTthttttttthhttttttthhhhhttthttthtthhhhhhhhhTttthhhhhhhttttttthh
10a00: hhhhhhhBhThttThttthDTBhTBThhhttthttttthttttDhTBhTBhBBBBBBTLhhttt
10e00: hhthhhhhhhtttDhThhTTthhhhhhBBBBBBBhBhTThhttthttthhhhhttttttthhht
11200: tttttttttttttthhhhhhhhhhhhhhhtttttttttttttthttttttttttthtttttttt
11600: tttttthhhDhhhhhhhhhhhhhhhhhthhhhhhhhhhhhtthhhhTthhhttttttthhhhhh
11a00: hhhhthhhhhttttttthhFhttttttthhhhhhhhTthttthMDhhhhhhhhhhhhhthhhhh
11e00: hhhhhTthhhtttDhThhhhhhhhTthhhDBhttttttthtBhhBtBhhhBBBBBBBBBBhhhh
12200: hhhhhhhhhhhhhhhtthhhhhhthhhhhhhhhhhhhhBhThttthttttthDhDhhhDhtttt
12600: htttttttttttttttttthhhhhhhhhhhhhhttttthttttttttttttttthhhhhhhthh
12a00: hhhhhhhhhhhTthhhhhtttthhhthhhhhhthhhhhhhhhhhhhhhhhhhhhthhhhhhthh
12e00: hhhhTthhhhhhhhhhhhthhhhthhhhthhthhthhththhthhttttttttttttttthhht
13200: httttthhttttttttttttthhttttttttttttttttttttttttttttttttttththhtt
13600: thhttthhtthhhhtthhthttttttttttttttttttttthhhhhhttttttthhhthttttt
13a00: tthhhthttttttthhhtthttttttttttttthhhhhthttttttttttttttttthhhhhth
13e00: ttttttttttthhttttthhhhhhhhttttthttttthhhhhhhhhhhDDhhhttttttthttt
14200: ttttttttttttthhthhhhhhhhhhhhhhhhhhhhthttttttttttthhTthhhhhhhhhhh
14600: hhhhhtthtttttttthhhttttttttttttttttttttttttttttttttttttttttttttt
14a00: ttttttttttttttttttthhhhhttttttthttttttttttthhhhhhttttttthhhhhhhh
14e00: hhhhhhhhDhhhhhhhhhhhhhtttLhhhhthhhhhhhLhhhhhhhhhhhhhhhhttttttFDL
15200: hhthhhtthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhDDDhhhttthtDDhhhhDLhhthhth
15600: hhhhtTthhttttttthhhhhhhhhhhhhhhhttttthhhhhhhttthtDDhhhhhhhLhhhhh
15a00: hDLhhthhhhLhhhhhhhhtttttthDLhhthhhhDLhhthhDLhhthhtDDLhhthDDLhThh
15e00: thhtttLhhtDhDLhhthhhhhhhttttthhtDLhttttttthhthhhhLhhhhhLhDLhhhhh
16200: thhhhhhLhhhTthhhhhhhDLhhthhDLhhhhhththhDLhhhhhhhhhhhhtDDhLhhthtt
16600: htttttDhhhhDLhhthhhDLhhhhhhhhhhhhhhhhhhttttttttttttttttttttttttt
16a00: ttttttttttttttttththhhhhLhhhhhhhhhhhhDhhLhhthhhhhhhhhhLhhhhhhhth
16e00: DhhhDLhhthDDLhhthhhhhhhhhthttttththhttthtDDhhhhhhhLhhhhhhhhhhthh
17200: hhhhhttththhttththDhhhhhDLhhthttthtDhDhhhthhhhhhtthhhttththhhhhh
17600: hhhhhhhhhhhhhhhhhhhthththhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhthhhhhh
17a00: hhhhhhhhhhhhhhtTthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
17e00: hhhhhhhhthhhhhhhhhhhhhhTthhhhthhhhhhhhhhhhhhTthhhhhhhhhhhhhhhhht
18200: thhhhhhhhhhhhhhhhhhhhthhhhhhthhthhtthhthhhhthhthhtththhhhhthhhth
18600: htttttthhttttthhttttttthhttttttttthtttthhthhthhthhthhtthhhhtthht
18a00: hhthhhhthhtthhhhtthhhhtthhhttttttttttththhhhhhthhthhthttttttthtt
18e00: thhhhhhthhthhthhhhhhhhthhhhthhhthhthhtthhtthhttttttttttthtttttth
19200: htthhhhhhthhhhhhhhthhhhthhhhhhthhhhthhhhhhthhhhthhhhhhthhhhthttt
19600: ttttthhhhhtttttttttttthttttttthhhthttttttthhttttttttttttttthhhth
19a00: hhhhtthhtttttttttththhhhhhhhhttttttththhtthhthhhhthhthhtthtthhtt
19e00: tttttthhhthhthtttttthhttttthhhthhthtttttttthhthhtttttttththhhhhh
1a200: hhhhhttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
1a600: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
1aa00: ttttttttttttttttttttttttttttttttttttthhhhhhhhhhhTthhhhhhhhhhhhhh
1ae00: hhhhhhhhhhhhhhhhhhhhhhThttttttthhhhhhhhhhhhhhhhhhthhhhhttttttthh
1b200: hhhhhhhhTthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhthhhhttttttthhh
1b600: hhhhhhhhhhhhhTthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
1ba00: hhhhhhhhthhhhhhhhhhhhhhTthhhhhtttttttttttttttttttttttttttttttttt
1be00: tttttttttttttttttttttttttttttttttttthttttttttttttttttttttttttttt
1c200: tttttttthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhthhhthhhhhhhhhhhhhhTtTthh
1c600: hhhhhhhhhhhhhhhhhhhtttthtttttttttttttttttthtthtthttttttttttttttt
1ca00: tttttththttttttttttttthttttthtthtttttthhhhtthhhttttttthtttthhtth
1ce00: hhtthhhhhhhhhhttttttthtttttthhhhhhhhhhhhhhhthhhhhhhhhhhhthhhhhhh
1d200: hhhhhhhTthhhttttttttttttttttthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
1d600: hhhhhhhhhthhhhhhhhhhhhhhTthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
1da00: hhhhhhhhthhhhhhhthhthhhhhhthhhhhhhthhhhhhhhhhhTthhhhhthhhhhhhhhh
1de00: hhhhhthhhhthhthhhhhttttthhttttttthhhhhhhhttttttttttttttttttttttt
1e200: ttththhhhhhthhthttttthhttttttttttttttttthhhhhhttttttttttttttttth
1e600: tthhhhthhthhthhhhhhthhthhthttttttttttttttttttthhhthhthhthtttthht
1ea00: ttthhhthhhtttttttttttttttttttttttthhhthhthttttttthhhthhthttthhtt
1ee00: hhtthhtttthhtttttttttttthtthhttttthhthtttthhttthhttthhttttthhhth
1f200: hthtttthhhthhthtttttttttthhhthhthttttttthhtttttttttttttthhhththh
1f600: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
1fa00: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
1fe00: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
20200: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
20600: httttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
20a00: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
20e00: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
21200: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
21600: thhhhhhhhhhTthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhthhhhhhhhhhhhhh
21a00: Tthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhthhhhhh
21e00: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
22200: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
22600: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
22a00: ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttth
22e00: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
23200: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
23600: tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
23a00: ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttth
23e00: hhhhhhhhTthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
24200: hthhhhhhhhhhhhtttttthhhTthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
24600: hhhhhhhhhhhhhhhhthhhhhhhhhhhhhhTthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
24a00: hhhhhhhhhhhhhhhhhhhhhhhhhthhhhhhhhhhhhhhTthhhhhhhhhhhhhhhhhhhhhh
24e00: Ththhhhhhhhhhhhhhhhh...........hht..............Tt..............
25200: ..............hh.........hh............hht..............Tt......
25600: ......................hh.........hh............hht..............
25a00: Tt............................hh.........hh............hht......
25e00: ........Tt...................................hh.........hh......
26200: ......hht..............Tt.........hh.........hh............hht..
26600: ............Tthttttttttttttttttttttttttttttttttttt....hh........
26a00: .hh............hht..............Tt..................hT..........
26e00: .....hh.........hh............hht..............Tt...............
27200: ......hh.........hh............hht..............Tthttttttttttttt
27600: tttttttttttttttttttttt..........................hh.........hh...
27a00: .........hht..............Tthttttttttttttttttttttttttttttttttttt
27e00: httttttttttttttttttttttttttttttttttt............................
28200: hh.........hh............hht..............Tt....................
28600: ........hh.........hh............hht..............Tt............
28a00: ................hhhh.......hh..hh.h......hht.hh.........htTthht.
28e00: ..........Tt........Tt.hh.........hh............hht.............
29200: .Tt.............................hh.........hh............hht....
29600: ..........Tt................hh.........hh............hht........
29a00: ......Tthttttttttttttttttttttttttttttttttttttttt..hh.........hh.
29e00: ...........hht.....hT.......Tt............................hh....
2a200: .....hh............h.hhht.............Tthttttttttttttttttttttttt
2a600: tttttttttttthttttttttttttttttttttttttttttttttttttttttttttttttttt
2aa00: ttttttttttt.hh.........hh............hht..............Tt........
2ae00: ....................hh.........hh............hht..............Tt
2b200: hh.........hh............hht..hh.....h....hTt.....h............h
2b600: ht..............Tt............................hh.........hh.....
2ba00: .......hht..............Tt............................hh........
2be00: .hh............hht.........hh..h

—
You are receiving this because you are subscribed to this thread.
Reply to this email directly or view it on GitHub
#2057 (comment)

Dave Hylands
Shuswap, BC, Canada
http://www.davehylands.com
```

SOURCE: https://github.com/micropython/micropython/issues/2057


# Performance Tips
- [PythonSpeed - PerformanceTips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [Variables and scope](https://python-textbok.readthedocs.io/en/1.0/Variables_and_Scope.html)
- [Understand How Much Memory Your Python Objects Use](https://code.tutsplus.com/tutorials/understand-how-much-memory-your-python-objects-use--cms-25609)
- [Python Memory Management](http://deeplearning.net/software/theano_versions/0.8.X/tutorial/python-memory-management.html)
- [Maximising MicroPython Speed](https://docs.micropython.org/en/latest/reference/speed_python.html)


# Hardware/Circuits
- [Avoiding NeoPixel glitches](https://ben.artins.org/electronics/glitchy-neopixels/)
