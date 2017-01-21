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

myPath = __file__.replace('RedTwiBot.py','')

def OAuthHelp(site):
	if site == "Reddit":
		link = "https://www.reddit.com/prefs/apps"
	else:
		link = "https://www.twitch.tv/settings/connections"
	print("First, go to "+site+" and sign in to the bot's account, then go to the following link:\n"+link)
	input("Press enter to continue...")
	previously = input("Have you previously created an app for this script?\n(y/n): ")
	if previously.lower() == 'n':
		if site == "Reddit":
			print("Press the 'create app' button.\n"
				  "Fill out the form as follows:\n"
				  "	Name: Sidebar-Streamers (or another name if you so wish)\n"
				  "	App type: script\n"
				  "	description: (leave blank or whatever you may like)\n"
				  "	about url: https://github.com/WolfgangAxel/RedTwiBot\n"
				  "	redirect url: http://127.0.0.1:65010/authorize_callback\n"
				  "Finally, press the 'create app' button.")
			input("Press enter to continue...")
			print("Underneath the name of the app, there should be a string of letters and numbers.\n"
				  "That is your client-id.\n"
				  "The secret is displayed in the table.")
		else:
			print("Scroll to the bottom of the page and press the 'Register your application' button\n"
				  "Fill out the form as follows:\n"
				  "	Name: Sidebar-Streamers"
				  "	Redirect URI: http://127.0.0.1:65010/authorize_callback\n"
				  "	Application Category: Application Integration\n"
				  "Finally, press the 'Register' button.")
			input("Press enter to continue...")
			print("Your client-id should now be displayed in a box on the page.")
	elif previously.lower() == 'y':
		if site == "Reddit":
			print("Scroll to the 'Developed Applications' section.\n"
				  "Underneath the name of the app, there should be a string of letters and numbers.\n"
				  "That is your client-id.\n"
				  "To get your secret, press 'edit' in the bottom-left of the app's box.\n"
				  "The secret should then be displayed.")
		else:
			print("Scroll to the 'Other Connections' section at the bottom of the page and press 'Edit' underneath the application name.\n"
				  "Your client-id should now be displayed in a box on the page.")

def walkThroughCredentials():
	while True:
		REDDIT_BOT_USERNAME=input("Please enter the Reddit bot's username: ").replace("/u/","")
		if REDDIT_BOT_USERNAME:
			confirm = input("You have entered /u/"+REDDIT_BOT_USERNAME+". Is this correct?\n(y/n): ")
			if confirm.lower() == "y":
				break
		else:
			print("No username entered. Try again.")
	while True:
		REDDIT_BOT_PASSWORD=input("Please enter the Reddit bot's password: ")
		if REDDIT_BOT_PASSWORD:
			confirm = input("You have entered '"+REDDIT_BOT_PASSWORD+"'. Is this correct?\n(y/n): ")
			if confirm.lower() == "y":
				break
		else:
			print("No password entered. Try again.")
	while True:
		OAuthWalkthrough = input("Do you know the Reddit bot's secret and client-id?\n(y/n):")
		if OAuthWalkthrough.lower() == 'n':
			OAuthHelp("Reddit")
		REDDIT_BOT_CLIENT_ID=input("Please enter the Reddit bot's client-id: ")
		if REDDIT_BOT_CLIENT_ID:
			confirm = input("You have entered '"+REDDIT_BOT_CLIENT_ID+"'. Is this correct?\n(y/n): ")
			if confirm.lower() == "y":
				break
		else:
			print("No client-id entered. Try again.")
	while True:
		REDDIT_BOT_SECRET=input("Please enter the Reddit bot's secret: ")
		if REDDIT_BOT_SECRET:
			confirm = input("You have entered '"+REDDIT_BOT_SECRET+"'. Is this correct?\n(y/n): ")
			if confirm.lower() == "y":
				break
		else:
			print("No secret entered. Try again.")
	while True:
		twitchAuthKnown=input("Do you know your Twitch bot client-id?\n(y/n): ")
		if twitchAuthKnown.lower() == 'n':
			OAuthHelp("Twitch")
		TWITCH_CLIENT_ID=input("Please enter the Twitch bot's client-id: ")
		if TWITCH_CLIENT_ID:
			confirm = input("You have entered '"+TWITCH_CLIENT_ID+"'. Is this correct?\n(y/n): ")
			if confirm.lower() == "y":
				break
	while True:
		MY_SUBREDDIT=input("Please enter the subreddit you want the bot to access: ").replace("/r/","")
		if MY_SUBREDDIT:
			confirm = input("You have entered /r/"+MY_SUBREDDIT+". Is this correct?\n(y/n): ")
			if confirm.lower() == "y":
				break
		else:
			print("No subreddit entered. Try again.")
	while True:
		MY_PERSONAL_REDDIT_ACCOUNT=input("Please enter your own personal reddit account: ").replace("/u/","")
		if MY_PERSONAL_REDDIT_ACCOUNT:
			confirm = input("You have entered /u/"+MY_PERSONAL_REDDIT_ACCOUNT+". Is this correct?\n(y/n): ")
			if confirm.lower() == "y":
				break
		else:
			print("No username entered. Try again.")
	ACCEPTABLE_GAMES = []
	print("This script will only add streamers to the sidebar if they are playing a game that is relevent to your subreddit. "
		  "This script will refer to these as 'acceptable games'.\n"
		  "Please add as many acceptable game titles as you would like.")
	while True:
		print("The current list of acceptable games is:")
		for aGame in ACCEPTABLE_GAMES:
			print("    "+aGame)
		print()
		game=input("Type in the name of one acceptable game: ")
		if game:
			confirm=input("Add '"+game+"' as an acceptable game?\n(y/n): ")
			if confirm.lower() == 'y':
				ACCEPTABLE_GAMES.append(game)
				print("Added "+game)
			again=input("Add another?\n(y/n): ")
			if again.lower() == 'n':
				break
		else:
			print("No game name entered. Try again.")
	while True:
		REFRESH_INTERVAL_IN_SECONDS=input("Enter the duration in minutes to wait between requesting Twitch streamer status:\n(Note: 3-5 minutes is a reasonable duration): ")
		confirm=input("Wait "+REFRESH_INTERVAL_IN_SECONDS+" minutes between refreshing?\n(y/n)")
		if REFRESH_INTERVAL_IN_SECONDS:
			if confirm.lower() == 'y':
				break
		else:
			print("No duration entered. Try again.")
	REFRESH_INTERVAL_IN_SECONDS=eval(REFRESH_INTERVAL_IN_SECONDS)*60
	with open(myPath+"credentials.txt",'w') as f:
		theFile =("REDDIT_BOT_USERNAME="+REDDIT_BOT_USERNAME+"\n"+
				  "REDDIT_BOT_PASSWORD="+REDDIT_BOT_PASSWORD+"\n"+
				  "REDDIT_BOT_CLIENT_ID="+REDDIT_BOT_CLIENT_ID+"\n"+
				  "REDDIT_BOT_SECRET="+REDDIT_BOT_SECRET+"\n"+
				  "TWITCH_CLIENT_ID="+TWITCH_CLIENT_ID+"\n"+
				  "MY_SUBREDDIT="+MY_SUBREDDIT+"\n"+
				  "MY_PERSONAL_REDDIT_ACCOUNT="+MY_PERSONAL_REDDIT_ACCOUNT+"\n"+
				  "ACCEPTABLE_GAMES="+str(ACCEPTABLE_GAMES)+"\n"+
				  "REFRESH_INTERVAL_IN_SECONDS="+str(REFRESH_INTERVAL_IN_SECONDS)+"\n")
		f.write(theFile)

while True:
	try:
		with open(myPath+"credentials.txt",'r') as f:
			creds = f.read().splitlines()
			REDDIT_BOT_USERNAME=creds[0].replace("REDDIT_BOT_USERNAME=",'')
			REDDIT_BOT_PASSWORD=creds[1].replace("REDDIT_BOT_PASSWORD=",'')
			REDDIT_BOT_CLIENT_ID=creds[2].replace("REDDIT_BOT_CLIENT_ID=",'')
			REDDIT_BOT_SECRET=creds[3].replace("REDDIT_BOT_SECRET=",'')
			TWITCH_CLIENT_ID=creds[4].replace("TWITCH_CLIENT_ID=",'')
			MY_SUBREDDIT=creds[5].replace("MY_SUBREDDIT=",'')
			MY_PERSONAL_REDDIT_ACCOUNT=creds[6].replace("MY_PERSONAL_REDDIT_ACCOUNT=",'')
			ACCEPTABLE_GAMES=eval(creds[7].replace("ACCEPTABLE_GAMES=",''))
			REFRESH_INTERVAL_IN_SECONDS=eval(creds[8].replace("REFRESH_INTERVAL_IN_SECONDS=",''))
			break
	except:
		print("There was an error reading "+myPath+"credentials.txt.\nThe script will now aid you in creating a new one.")
		walkThroughCredentials()

if not (REDDIT_BOT_USERNAME and REDDIT_BOT_PASSWORD and REDDIT_BOT_CLIENT_ID and REDDIT_BOT_SECRET and TWITCH_CLIENT_ID and MY_PERSONAL_REDDIT_ACCOUNT and MY_SUBREDDIT):
	exit("Something strange happened. Please delete "+myPath+"credentials.txt and restart this script.\nIf the problem persists, please fill out a bug report on GitHub here:\nhttps://github.com/WolfgangAxel/RedTwiBot/issues/new")

while True:
	try:
		test = open(myPath+"sidebar.md",'r').read()
		if test == "Paste your subreddit's sidebar markdown here.\n\n Add 2 lines like below where you want the streamer statuses to be displayed.\n\n====\n\n====":
			print("Sidebar was not edited. Please edit the file and try again.")
			raise Exception
		break
	except:
		with open(myPath+"sidebar.md",'w') as f:
			f.write("Paste your subreddit's sidebar markdown here.\n\n Add 2 lines like below where you want the streamer statuses to be displayed.\n\n====\n\n====")
		print(myPath+"sidebar.md was not found. One has automatically been generated. Please open that file in a text editor and follow the instructions in the file.")
		input("Press enter to continue...")

while True:	
	try:
		test = open(myPath+"streamers.txt",'r').readlines()
		if test == ['example1','EXAMPLE_2','Example-3']:
			print("Streamer file was not edited. Please edit the file and try again.")
			raise Exception
		break
	except:
		with open(myPath+"streamers.txt",'w') as f:
			f.write("example1\nEXAMPLE_2\nExample-3")
		print(myPath+"streamers.txt was not found. One has automatically been generated. Please open that file in a text editor and follow the instructions in the file.")
		input("Press enter to continue...")

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
	print("Checking streamers...")
	streamers = open(myPath+"streamers.txt",'r').readlines()
	# Reopens this file every time the bot refreshes, so new additions 
	# will be included on the next update
	streamerBox="\n\n****\n\n**Streaming now:**\n\n"
	for streamer in streamers:
		streamer = streamer.replace('\n','')
		status = get("https://api.twitch.tv/kraken/streams/"+streamer,headers={'Accept':'application/vnd.twitchtv.v3+json','Client-ID':TWITCH_CLIENT_ID})
		# Get their Twitch status
		status = loads(str(status.content,'utf-8'))
		# Parse it
		if status['stream']:
			print(streamer+" is playing "+status['stream']['game'])
			# Check if they're streaming at all
			if status['stream']['game'].lower().replace(' ','') in [ name.lower().replace(' ','') for name in ACCEPTABLE_GAMES]:
				# Check if they're streaming the right game
				streamerBox += "[" + streamer + "](" + status['stream']['channel']['url'] + ")\n\n"
				# Makes a link to the stream with the streamer's username as the link title
	if streamerBox == "\n\n**Streaming now:**\n\n":
		streamerBox += "None :(\n\n"
		# Make a sad face if no-one is streaming
	sidebar = open(myPath+"sidebar.md",'r').read()
	# Read the sidebar (on file)
	oldStreamerBox = search("====(.*)====",sidebar,flags=multiline)
	# Find the replacement portion
	if streamerBox != oldStreamerBox.group(1):
		print("Stream statuses changed. Updating sidebar...")
		# If it's the same as it was last update, we skip all of this
		newSidebar = sidebar.replace(oldStreamerBox.group(0),streamerBox)
		# Replace everything between the ===='s, ===='s included
		praw.models.reddit.subreddit.SubredditModeration(reddit.subreddit(MY_SUBREDDIT)).update(description=newSidebar)
		# Update the sidebar
		with open(myPath+"sidebar.md",'w') as New:
			New.write(sidebar.replace(oldStreamerBox.group(0),"===="+streamerBox+"\n===="))
			# Save the new sidebar for the next update
	print("Done. Sleeping")
	sleep(REFRESH_INTERVAL_IN_SECONDS)
