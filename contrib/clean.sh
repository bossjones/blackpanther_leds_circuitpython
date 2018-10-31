set -v
rm *.mpy
find /Volumes/CIRCUITPY/ -name *.py | xargs rm
find /Volumes/CIRCUITPY/ -name *.mpy | xargs rm
