#!/bin/bash

# params
FILE_WEB_SCRIPT_USER="$MIRO_DIR_STATE/web_script_user.py"
FILE_WEB_SCRIPT_TAG="web_script_exec"
FILE_WEB_SCRIPT_EXEC="/tmp/$FILE_WEB_SCRIPT_TAG.py"

# handle
if [[ "$1" == "start" ]];
then

	# stop any running script first
	./control_web_script.sh stop

	# if it exists
	if [[ -f "$FILE_WEB_SCRIPT_USER" ]];
	then
		cp web_script_prepend.py $FILE_WEB_SCRIPT_EXEC
		cat $FILE_WEB_SCRIPT_USER >> $FILE_WEB_SCRIPT_EXEC
		$FILE_WEB_SCRIPT_EXEC &
	fi

fi

# handle
if [[ "$1" == "stop" ]];
then

	# find its pid
	pid=`pgrep -f $FILE_WEB_SCRIPT_TAG`

	# if present
	if [[ "$pid" != "" ]];
	then
		echo -e "killing $pid..."
		kill -9 $pid
		sleep 1

		pid=`pgrep -f $FILE_WEB_SCRIPT_TAG`
		if [[ "$pid" == "" ]];
		then
			echo "OK, killed"
		else
			echo "failed to kill"
		fi
	else
		echo "(not running)"
	fi

fi




