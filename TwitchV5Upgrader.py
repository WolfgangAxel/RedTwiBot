#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  TwitchV5Upgrader.py
#  
#  Copyright 2017 Keaton Brown <linux.keaton@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

"""

NOTICE: THIS IS ONLY REQUIRED IF YOU ARE UPGRADING THE BOT FROM
A VERSION BEFORE 5/19/17 TO THE CURRENT VERSION.

Don't run this otherwise- you're just going to be wasting your time.
********************************************************************

After you run this script, configuration.V5.ini will be written.
This file will need to be renamed to configuration.ini in order for 
the bot to properly be updated. It is done this way so your 
configuration is not overwritten with information missing. Double-
check that the configuration file has everything you want in it 
before deleting the old one.

"""



import requests
import configparser
import time
import re
import json

myPath = re.search(r"[a-zA-Z0-9. ]*(.*)",__file__[::-1]).group(1)[::-1]
conf = configparser.RawConfigParser()
conf.optionxform = lambda option: option
conf.read(myPath+"configuration.ini")

# Can't change the size of the dict while iterating, so get our iterator now
streamers = [streamer for streamer in conf['TS']]

for streamer in streamers:
    # Make the channel request
    status = requests.get("https://api.twitch.tv/kraken/channels/"+streamer,
                  headers={'Accept':'application/vnd.twitchtv.v3+json',
                           'Client-ID':conf["T"]["c"]})
    # Parse it
    status = json.loads(str(status.content,'utf-8'))
    # If an error occurred, print error and halt until the user acknowledges
    if 'error' in status:
        print("Skipping "+streamer+". Error:\n    "+status['message'])
        _ = conf['TS'].pop(streamer)
        input("Press enter to continue...")
        continue
    conf['TS'][str(status['_id'])] = streamer
    _ = conf['TS'].pop(streamer)
    print(streamer+" updated!")
    time.sleep(0.5)

# Sort the configuration file's keys
for section in conf:
    conf[section] = {key:conf[section][key] for key in sorted(conf[section])}

with open(myPath+"configuration.V5.ini","w") as cfg:
    conf.write(cfg)
