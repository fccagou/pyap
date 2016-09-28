#!/bin/sh

BLINK_PYTHON=$(dirname $0)/blink1

[ ! -d ${BLINK_PYTHON} ] && mkdir -p ${BLINK_PYTHON}

for f in blink1.py blink1_pyusb.py
do
	curl -q -o ${BLINK_PYTHON}/$f https://raw.githubusercontent.com/todbot/blink1/master/python/alternative_libraries/$f
done


chmod +x ${BLINK_PYTHON}/blink1.py

curl -q -o data/51-blink1.rules https://github.com/todbot/blink1/blob/master/linux/51-blink1.rules

