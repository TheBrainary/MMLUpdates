#!/bin/bash
for (( ; ; ))
do
	x=$(rosnode list)
	if  [[ $x == *"client_web"* ]]; then
		echo "Client_web Running"
	else
		if  [ -f "/tmp/running.state" ]; then
			sleep 5
			x=$(rosnode list)
			if  [[ $x != *"client_web"* ]]; then
				rm "/tmp/running.state"
				echo "Removing /tmp/running.state"
			fi
		fi
	fi
done
