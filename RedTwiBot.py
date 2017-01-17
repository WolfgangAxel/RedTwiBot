#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  RedTwiBot.py
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

REDDIT_BOT_USERNAME=""
REDDIT_BOT_PASSWORD=""
REDDIT_BOT_CLIENT_ID=""
REDDIT_BOT_SECRET=""

TWITCH_CLIENT=""

MY_SUBREDDIT=""
# Leave out the /r/
# i.e. "nocturnemains" not "/r/nocturnemains"

MY_PERSONAL_REDDIT_ACCOUNT=""
# Leave out the /u/
# i.e. 

GAME_ALIASES = [ 'example1', 'Example2' ]
# Possible names the stream may use for your game.
# These need to be wrapped in either single quotes (')
# or double quotes (") and separated by a comma.

REFRESH_INTERVAL_IN_SECONDS=180


if not (REDDIT_BOT_USERNAME and REDDIT_BOT_PASSWORD and REDDIT_BOT_CLIENT_ID and REDDIT_BOT_SECRET and TWITCH_CLIENT and MY_PERSONAL_REDDIT_ACCOUNT and MY_SUBREDDIT):
	exit("I can't run without knowing who I am. Please open this file and enter my credentials at the top under the comment block.")

myPath = __file__.strip('RedTwiBot.py')
try:
	test = open(myPath+"sidebar.md",'r').read()
	test = open(myPath+"streamers.txt",'r').readlines()
except:
	exit("Please supply a 'sidebar.md' and 'streamers.txt' file in the same directory as this script.")

try:
	mod = "praw"
	import praw
	mod = "requests"
	from requests import get
except:
	exit("Please install "+mod+". Easiest way is to run 'pip3 install "+mod+"'")

try:
	reddit = praw.Reddit(client_id=REDDIT_BOT_CLIENT_ID,
						client_secret=REDDIT_BOT_SECRET,
						password=REDDIT_BOT_PASSWORD,
						user_agent="Updating the sidebar of /r/"+MY_SUBREDDIT+", hosted by /u/"+MY_PERSONAL_REDDIT_ACCOUNT,
						username=REDDIT_BOT_USERNAME)
except Exception as e:
	exit("Reddit authentication failed. Check for correct credentials and internet connection\n\nMore details: "+str(e.args()))

from time import sleep
from json import loads
from re import search
from re import DOTALL as multiline
while True:
	streamers = open(myPath+"streamers.txt",'r').readlines()
	# Reopens this file every time the bot refreshes, so new additions 
	# will be included on the next update
	streamerBox="\n\n****\n\n**Streaming now:**\n\n"
	for streamer in streamers:
		status = get("https://api.twitch.tv/kraken/streams/"+streamer,headers={'Accept':'application/vnd.twitchtv.v3+json','Client-ID':TWITCH_CLIENT})
		# Get their Twitch status
		status = loads(status.content)
		# Parse it
		if status['stream']:
			# Check if they're streaming at all
			if status['stream']['game'].lower().strip(' ') in [ name.lower().strip(' ') for name in GAME_ALIASES]:
				# Check if they're streaming the right game
				streamerBox += "[" + streamer + "](" + status['stream']['channel']['_links']['stream_key'] + ")\n\n"
				# Makes a link to the stream with the streamer's username as the link title
	if streamerBox == "\n\n**Streaming now:**\n\n":
		streamerBox += "None :(\n\n"
		# Make a sad face if no-one is streaming
	sidebar = open(myPath+"sidebar.md",'r').read()
	# Read the sidebar (on file)
	oldStreamerBox = search("====(.*)====",sidebar,flags=multiline)
	# Find the replacement portion
	if streamerBox != oldStreamerBox.group(1):
		# If it's the same as it was last update, we skip all of this
		newSidebar = sidebar.replace(oldStreamerBox.group(0),streamerBox)
		# Replace everything between the ===='s, ===='s included
		praw.models.reddit.subreddit.SubredditModeration(reddit.subreddit(MY_SUBREDDIT)).update(description=newSidebar)
		# Update the sidebar
		with open(myPath+"sidebar.md",'w') as New:
			New.write(sidebar.replace(oldStreamerBox.group(1),streamerBox)
			# Save the new sidebar for the next update
	sleep(REFRESH_INTERVAL_IN_SECONDS)
