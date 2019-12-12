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

( \
	echo "password='$password'" ; \
	echo "essid='$essid'" ; \
	cat config.py ; \
) > /tmp/config.$$.py

warn "Configuring wifi"
ampy --port "$port" run /tmp/config.$$.py \
|| die "config.py failed"
rm /tmp/config.$$.py

