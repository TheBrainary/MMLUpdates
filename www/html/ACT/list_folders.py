
#!/usr/bin/python

import os
import json
from os.path import join, getsize
# initialise ROS node
data = {}
data['Applications'] = []
for root, dirs, files in os.walk('/home/miro/ACT/packaged_apps/'):
    data["Applications"].append({
        'name': root.replace('/home/miro/ACT/packaged_apps/', ' '),
        'path': root
    })
   
print json.dumps(data)
