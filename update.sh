#!/bin/bash
cd /tmp
rm MMLUpdates -r
git clone git@github.com:TheBrainary/MMLUpdates.git -q
cd MMLUpdates
version=`cat VERSION`
cversion=`cat ~/ACT/VERSION`
echo "Current Version: $cversion"
echo "Update Version: $version"
if (( `expr $version` > `expr $cversion` ))
then
	echo "Installing update, This may take a few minutes."
	sh ./install.sh
else
	echo "No Update needed, software is up to date"
fi
