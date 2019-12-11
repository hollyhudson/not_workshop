#!/bin/sh
# Usage:
# setup.sh /dev/ttyUSB0 'essid' 'password'

dir=`dirname $0`
cd "$dir"

die() { echo >&2 "$@" ; exit 1 ; }
warn() { echo >&2 "$@" ; }

if [ $# -lt 3 ] ; then
	die "Usage: $0 /dev/tty... wifi-network wifi-password"
fi

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

warn "Configuring wifi"
ampy --port "$port" run /tmp/config.$$.py \
|| die "config.py failed"
rm /tmp/config.$$.py

warn "Configuring boot"
ampy --port "$port" put boot.py \
|| die "boot.py failed"

# Install the local webserver
warn "Setting up webserver"
ampy --port "$port" mkdir html 2>/dev/null
for file in index.html term.js FileSaver.js; do
	warn "$file: installing"
	gzip < html/$file > /tmp/$file.$$.gz

	ampy --port "$port" put /tmp/$file.$$.gz html/$file.gz \
	|| die "$file: Unable to install"

	rm /tmp/$file.$$.gz
done

warn "webserver.py: installing"
ampy --port "$port" put webserver.py

# Perform a hard reset by reading the MAC address
esptool.py --port "$port" read_mac \
|| die "reset failed"
