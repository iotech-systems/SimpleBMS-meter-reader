#!/bin/bash

RAMDSK_SIZE="16M"
RAMDSK_PATH="/opt/iotech/ramdsk"

if [ ! -d $RAMDSK_PATH ]; then
  echo "Creating RAMDSK: $RAMDSK_PATH"
  mkdir $RAMDSK_PATH
fi

mount -t tmpfs -o rw,size=$RAMDSK_SIZE tmpfs $RAMDSK_PATH
echo "ERROR_CODE: $?"
