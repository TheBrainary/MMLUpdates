#!/bin/bash
#Remove Old ACT Folder and replace with one from MML
sudo rm /home/miro/ACT -r
sudo cp ACT /home/miro/ACT -r

sudo rm /var/www/html/assets -r
sudo rm /var/www/html/dist -r
sudo cp assets /var/www/html/assets -r
sudo cp dist /var/www/html/dist -r

# sudo rm /home/miro/mdk/bin/onboard/on_system_ready.sh
# sudo cp on_system_ready.sh /home/miro/mdk/bin/onboard/on_system_ready.sh
echo "Source Files Installed"