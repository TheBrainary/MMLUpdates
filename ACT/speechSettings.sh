#!/bin/bash
TARGET_KEY="lang"
CONFIG_FILE="/home/miro/ACT/speech.cfg"
REPLACEMENT_VALUE="\"$1\""
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE
TARGET_KEY="pitch"
REPLACEMENT_VALUE="\"$2\""
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE
TARGET_KEY="tempo"
REPLACEMENT_VALUE="\"$3\""
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE
TARGET_KEY="voice_reco"
REPLACEMENT_VALUE="\"$4\""
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE
