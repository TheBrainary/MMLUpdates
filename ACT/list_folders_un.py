#!/usr/bin/python

import os
import json
from os.path import join, getsize
# initialise ROS node

def list_folders():
    data = {}
    data = []
    i=-1
    for root, dirs, files in os.walk('/home/miro/ACT/packaged_apps/'):
        if i>=0:
            data.append({
                'id': i,
                'name': root.replace('/home/miro/ACT/packaged_apps/', ' '),
                'path': root
            })
        i=i+1
    return json.dumps(data)
