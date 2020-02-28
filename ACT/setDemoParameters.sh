#!/bin/bash

TARGET_KEY="demo_flags"
CONFIG_FILE="/home/miro/.miro2/config/platform_parameters"
REPLACEMENT_VALUE="$1"
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE
