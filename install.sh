#!/bin/bash
#Remove Old ACT Folder and replace with one from MML
sudo rm /home/miro/ACT -r
sudo cp ACT /home/miro/ACT -r

sudo rm /var/www/ -r
#sudo rm /var/www/html/dist -r
sudo cp assets /var/www/html/assets -r
sudo cp www /var/ -r

sudo rm /usr/local/lib/python3.5/dist-packages/pocketsphinx/model/testdict.dict
sudo cp testdict.dict usr/local/lib/python3.5/dist-packages/pocketsphinx/model/testdict.dict
sudo cp checkupdate.sh /home/miro/checkupdate.sh
sudo cp update.sh /home/miro/update.sh
echo "Source Files Installed"