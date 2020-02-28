#!/bin/bash
cd /tmp
rm MMLVersion -r
git clone git@github.com:TheBrainary/MMLVersion.git -q
cd MMLVersion
version=`cat VERSION`
cversion=`cat ~/ACT/VERSION`
#echo "$cversion;$version;Update Available"
#echo "Update Version: $version"
if (( `expr $version` > `expr $cversion`))
then
	echo "$cversion;$version;Update Available"
else
	echo "$cversion;$version;Up to date"
fi
