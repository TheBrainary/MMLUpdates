#!/bin/bash
TARGET_KEY="ssid"
CONFIG_FILE="/etc/wpa_supplicant/wpa_supplicant.conf"
REPLACEMENT_VALUE="\"$1\""
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE
TARGET_KEY="psk"
REPLACEMENT_VALUE="\"$2\""
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE
