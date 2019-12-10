#!/bin/sh
# Usage:
# setup.sh /dev/ttyUSB0 'essid' 'password'

die() { echo >&2 "$@" ; exit 1 ; }
warn() { echo >&2 "$@" ; }

port=$1
essid=$2
password=$3
micropython=$4

if [ -z "$micropython" ]; then
	micropython=esp8266-20190529-v1.11.bin
fi
if [ ! -r "$micropython" ]; then
	warn "$micropython: trying to fetch"
	wget "http://micropython.org/resources/firmware/$micropython" \
	|| die "$micropython: wget failed"
fi


#
# Check for micropython running on the board
#

warn "$port: Checking for micropython"
if ! timeout 1 ampy --port "$port" ls > /dev/null 2>/dev/null ; then
	warn "------- micropython not installed -----"
	sleep 2
	esptool.py \
		--port "$port" \
		erase_flash \
	|| die "$port: erase flash failed"

	esptool.py \
		--port "$port" \
		--baud 460800 \
		write_flash 0 \
		"$micropython" \
	|| die "$port: write flash failed"

	sleep 1
fi

( \
	echo "password='$password'" ; \
	echo "essid='$essid'" ; \
	cat config.py ; \
) > /tmp/config.$$.py

ampy --port "$port" run /tmp/config.$$.py \
|| die "config.py failed"

ampy --port "$port" put boot.py \
|| die "boot.py failed"

# Perform a hard reset by reading the MAC address
esptool.py --port "$port" read_mac \
|| die "reset failed"
