
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  SidebarStreamers.py
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

########################################################################
#                                                                      #
#    Definitions                                                       #
#                                                                      #
########################################################################

#### Startup

def loadConfig(myPath):
    """
    loads the config file, if anything is empty, cause panic
    """
    print("Loading configuration from file...")
    conf = configparser.RawConfigParser()
    conf.optionxform = lambda option: option
    conf.read(myPath+"configuration.ini")
    print("Configuration file read. Checking for usable values.")
    if not conf.sections():
        print("No sections found in configuration file. Aborting!")
        raise Exception
    if sorted(conf.sections()) != sorted(configSections):
        print("Not all sections found. Aborting!")
        raise Exception
    print("Found sections. Checking for values...")
    for item in conf.sections():
        if not [thing[1] for thing in conf[item].items()]:
            print("No values found for section "+item+"."
                  "Proceeding without certain values might "
                  "cause errors down the road. If this is "
                  "incorrect, kill this script now and adjust "
                  "the values in "+myPath+"configuration.ini "
                  "or regenerate "+myPath+"configuration.ini.")
            time.sleep(3)
            print("Ignoring empty section")
        print("Found values for section "+item)
    print("Configuration seems usable. Using "+myPath+"configuration.ini")
    return conf

def saveConfig():
    with open(myPath+"configuration.ini","w") as cfg:
        conf.write(cfg)
    print("Config file written successfully")

def makeCreds(myPath):
    print("Either this is the first time this script is being run, or there "
          "was an error reading the config file. You will now be walked "
          "through obtaining all the credentials this bot needs in order "
          "to function.")
    global conf
    conf = configparser.ConfigParser()
    conf.optionxform = lambda option: option
    ############################################################# Reddit
    print("We will first get the bot's Reddit information.")
    input("Press enter to continue... ")
    print(" 1) Go to https://www.reddit.com/prefs/apps and sign in with your "
          "bot account.\n"
          " 2) Press the 'create app' button, then enter the following :\n\n"
          "    Name: SidebarStreamers (or another name if you so wish)\n"
          "    App type: script\n"
          "    description: (leave this blank or enter whatever you wish)\n"
          "    about url: https://github.com/WolfgangAxel/SidebarStreamers\n"
          "    redirect url: http://127.0.0.1:65010/authorize_callback\n\n"
          " 3) Finally, press the 'create app' button.")
    input("Press enter to continue... ")
    print("Underneath the name of the app, there should be a string of letters and numbers.\n"
          "That is the bot's client-id.\n"
          "The bot's secret is displayed in the table.")
    redCreds = {}
    for short,thing in [["u","username"],["p","password"],["c","client-id"],["s","secret"]]:
        while True:
            value = input("Please enter the bot's "+thing+":\n==> ")
            confirm = input("Is '"+value+"' correct? (y/n)\n==> ")
            if confirm.lower() == "y":
                redCreds[short] = value
                break
            print("Confirmation failed. Restarting entry")
    ############################################################### Twitch
    print("Next, we will get the bot's Twitch information.")
    input("Press enter to continue... ")
    print(" 1) Go to https://www.twitch.tv/settings/connections and sign in with "
          "your bot account.\n"
          " 2) Scroll to the bottom of the page and press the 'Register your application' "
          "button.\n"
          " 3) Fill out the form as follows:\n"
          "  Name: Sidebar-Streamers"
          "  Redirect URI: http://127.0.0.1:65010/authorize_callback\n"
          "  Application Category: Application Integration\n"
          " 4) Finally, press the 'Register' button.")
    input("Press enter to continue... ")
    twiCreds={}
    while True:
        value = input("Please enter the bot's client-id:\n==> ")
        confirm = input("Is '"+value+"' correct? (y/n)\n==> ")
        if confirm.lower() == "y":
            twiCreds["c"] = value
            break
        print("Confirmation failed. Restarting entry")
    ############################################################### YouTube
    print("Next, we will get the bot's YouTube information.")
    input("Press enter to continue... ")
    print(" 1) Go to https://console.developers.google.com/apis and sign in with "
          "your or your bot's Google account.\n"
          " 2) Click on the 'credentials' tab on the right\n"
          " 3) Create a new project if you do not have one available to use. "
          "Name it whatever you wish.\n"
          " 4) Press the 'Create credentials' button, then 'API key' from the menu.\n"
          " 5) You may use the key now, however it is advised to click the 'Restrict key' "
          "button and restrict the key to 'IP address'. You may also rename the key "
          "if you so wish.")
    input("Press enter to continue... ")
    gytCreds = {}
    while True:
        value = input("Please enter the bot's API key:\n==> ")
        confirm = input("Is '"+value+"' correct? (y/n)\n==> ")
        if confirm.lower() == "y":
            gytCreds["k"] = value
            break
        print("Confirmation failed. Restarting entry")
    ############################################################### Misc
    print("Almost done! Just a few more items to define.")
    input("Press enter to continue... ")
    mscCreds = {}
    for variable,question in [ ["mySub","Enter the name of your subreddit."],
                               ["botMaster","Enter your personal Reddit username. (This is used for Reddit's user-agent, nothing more)"],
                               ["sleepTime","How many seconds to wait between refreshing? (Use whole numbers like 300 or expressions like 5 * 60)"]
                             ]:
        while True:
            value = input(question+"\n==>")
            confirm = input("Is '"+value+"' correct? (y/n)\n==> ")
            if confirm.lower() == "y":
                mscCreds[variable] = value
                break
            print("Confirmation failed. Restarting entry.")
    
    ################################################ Games and Streamers
    gameList = {}
    print("We will now build the list of acceptable games")
    input("Press enter to continue... ")
    while True:
        print("The current list of acceptable games is:")
        for thing in gameList:
            print("    "+thing)
        print()
        again=input("Add another?\n(y/n): ")
        if again.lower() == 'n':
            break
        thing=input("Type in the name of one acceptable game: ")
        if thing:
            confirm=input("Add '"+thing+"' as an acceptable game?\n(y/n): ")
            if confirm.lower() == 'y':
                gameList[thing] = "Good"
                print("Added "+thing)
        else:
            print("No game entered. Nothing to add.")
    twstList = {}
    print("We will now build the list of acceptable Twitch streamers.\n"
          "Note: this will use the client ID you provided previously.")
    input("Press enter to continue... ")
    while True:
        print("The current list of acceptable Twitch streamers is:")
        for thing in twstList:
            print("    "+thing+" - "+twstList[thing])
        print()
        again=input("Add another?\n(y/n): ")
        if again.lower() == 'n':
            break
        thing=input("Type in the name of one acceptable Twitch streamer: ")
        if thing:
            confirm=input("Add '"+thing+"' as an acceptable Twitch streamer?\n(y/n): ")
            if confirm.lower() == 'y':
                print("Making request to obtain user ID for",thing)
                try:
                    status = requests.get("https://api.twitch.tv/kraken/users?login="+thing,
                                headers={'Accept':'application/vnd.twitchtv.v5+json','Client-ID':twiCreds["c"]})
                    status = json.loads(str(status.content,"utf-8"))
                    twstList[status['users'][0]['_id']] = thing
                    print("Added "+thing)
                except Exception as e:
                    print("Error when adding streamer. Error details:\n   ",e)
        else:
            print("No game entered. Nothing to add.")
    ytstList = {}
    print("We will now build the list of acceptable YouTube streamers. "
          "\n***NOTICE***\n\nYouTube channel IDs are NOT the channel names!!!\n"
          "Find the channel ID by visiting their channel and copying "
          "the string of characters between '/channel/' and the first '?'. For example, "
          "the channel ID for "
          "https://www.youtube.com/channel/UC4YaOt1yT-ZeyB0OmxHgolA?&ab_channel=A.I.Channel "
          "would be UC4YaOt1yT-ZeyB0OmxHgolA")
    input("Press enter to continue... ")
    while True:
        print("The current list of acceptable YouTube streamers is:")
        for thing in ytstList:
            print("    "+thing+" - "+ytstList[thing])
        print()
        again=input("Add another?\n(y/n): ")
        if again.lower() == 'n':
            break
        thing=input("Type in the CHANNEL ID of one acceptable YouTube streamer: ")
        human=input("Type in the human-readable channel name for "+thing+": ")
        if thing:
            confirm=input("Add '"+human+"' ("+thing+") as an acceptable YouTube streamer?\n(y/n): ")
            if confirm.lower() == 'y':
                ytstList[thing] = human
                print("Added "+thing)
        else:
            print("No YouTube streamer entered. Nothing to add.")
    
    conf["R"] = {key:redCreds[key] for key in sorted(redCreds)}
    conf["T"] = {key:twiCreds[key] for key in sorted(twiCreds)}
    conf["Y"] = {key:gytCreds[key] for key in sorted(gytCreds)}
    conf["M"] = {key:mscCreds[key] for key in sorted(mscCreds)}
    conf["G"] = {key:gameList[key] for key in sorted(gameList)}
    conf["TS"] = {key:twstList[key] for key in sorted(twstList)}
    conf["YS"] = {key:ytstList[key] for key in sorted(ytstList)}
    saveConfig()
    return conf

#### Utility

def addThing(thing,kind):
    """
    Add a thing to the list and save the file.
    """
    if kind == "YS":
        ID = re.search("(.+?) ",thing).group(1)
        human = re.search(".+ (.+)").group(1)
        conf[kind][ID] = human
    elif kind == "TS":
        status = requests.get("https://api.twitch.tv/kraken/users?login="+thing,
                    headers={'Accept':'application/vnd.twitchtv.v5+json','Client-ID':conf["T"]["c"]})
        status = json.loads(str(status.content,"utf-8"))
        if 'error' in status:
            raise Exception("Error in response: "+status['message'])
        conf[kind][status['users'][0]['_id']] = thing
    else:
        conf[kind][thing.lower().replace(":","").replace("=","")] = "Good"
    saveConfig()

def delThing(thing,kind):
    """
    Remove a thing from the list and save the file.
    """
    if kind not in ["TS","YS"]:
        _ = conf[kind].pop(thing.lower())
    else:
        _ = conf[kind].pop( [s for s in conf[kind] if conf[kind][s] == thing][0] )
    saveConfig()

def updateSidebar():
    statusSection = "\n\n****\n\n**Streaming now:**\n\n"
    ############################################################ Twitch
    if len(conf["TS"]) <= 100:
        streamerGroups = [",".join(conf["TS"])]
    else:
        index = 0
        streamerGroups = []
        while True:
            streamerGroups.append( ",".join(conf["TS"][index*100:100*(index+1)]) )
    paginated = []
    for streamers in streamerGroups:
        fails = 0
        while fails < 3:
            try:
                # Be nice to Twitch servers
                time.sleep(0.5)
                # Get the status
                status = requests.get("https://api.twitch.tv/kraken/streams/?channel="+streamers+"&?limit=100&?stream_type=live",
                                      headers={'Accept':'application/vnd.twitchtv.v5+json',
                                               'Client-ID':conf["T"]["c"]})
                # Parse it and add to paginated queue
                status = json.loads(str(status.content,'utf-8'))
                paginated.append(status)
                # If there were no errors, then keep going
                # If there were errors, try again
                # If there were 3 consecutive errors, skip it (handled later).
                if not "error" in status:
                    break
                fails += 1
                print("Error with request for Twitch streams. Attempts remaining: "+str(3-fails)+"/3")
            except Exception as e:
                fails += 1
                print("Error with request for Twitch streams. Attempts remaining: "+str(3-fails)+"/3")
                print("Error was more than an invalid response. Details:\n",e)
    streams = []
    for status in paginated:
        for stream in status['streams']:
            streams.append(stream)
    for stream in streams:
        print(stream['channel']['name']+" is playing "+stream['game'])
        # Check if they're streaming the right game
        if stream['game'].lower().replace(' ','').replace(":","").replace("=","") in [ name.lower().replace(' ','') for name in conf["G"] ]:
            # Make a link to the stream with the streamer's username as the link title
            statusSection += "* [" + stream['channel']['name'] + " - " + stream['game'] + "](" + stream['channel']['url'] + ")\n\n"
    ########################################################### Youtube
    for streamer in conf["YS"]:
        fails = 0
        while fails < 3:
            try:
                # Be nice to Google servers
                time.sleep(0.5)
                # Get the status
                status = requests.get("https://www.youtube.com/channel/"+streamer+"/videos?view=2&amp;flow=grid")
                # Parse it
                status = bs4.BeautifulSoup(str(status.content,"utf-8"),"html.parser")
                break
            except Exception as e:
                fails += 1
                print("Error with request for "+conf["YS"][streamer]+"'s stream. Attempts remaining: "+str(3-fails)+"/3")
                print("Details:\n",e)
        if fails > 2:
            print("Maximum failed attempts hit. Skipping.")
            continue
        # Get links for any livestreams found
        for stream in status.find_all(attrs={"class":"yt-lockup-title "}):
            streamInfo = stream.parent.find_all(attrs={"class":"yt-lockup-badges"})
            if not streamInfo:
                # Not actually live, just a live stream recording
                continue
            if streamInfo[0].ul.li.span.string != "Live now":
                # False positive. Not quite sure how this happens but it does
                continue
            title = stream.a.string
            if len(title) > 70:
                title = title[:67]+"..."
            print(status.title.string[2:-11],"is streaming",title)
            for name in conf["G"]:
                if name.lower().replace(' ','') in stream.a.string.lower().replace(' ','').replace(":","").replace("=",""):
                    # Make a link to the stream with the streamer's username as the link title
                    statusSection += "* [" + status.title.string[2:-11] + " - " + title + "](" + "https://www.youtube.com" + stream.a['href'] + ")\n\n"
                    break
            if status.title.string[2:-11] in statusSection:
                continue
            print("Acceptable game not found in title. Making additional request to search tags")
            fails = 0
            while fails < 3:
                try:
                    # Be nice to Google servers
                    time.sleep(0.5)
                    # Get full description
                    expand = requests.get("https://www.googleapis.com/youtube/v3/videos?part=snippet&id="+stream.a['href'].replace("/watch?v=","")+"&key="+conf["Y"]["k"])
                    # Parse it
                    expand = json.loads(str(expand.content,'utf-8'))
                    # If there were no errors, then keep going
                    # If there were errors, try again
                    # If there were 3 consecutive errors, skip it (handled later).
                    if not "error" in expand:
                        break
                    fails += 1
                    print("Error with request for "+conf["YS"][streamer]+"'s stream. Attempts remaining: "+str(3-fails)+"/3")
                except Exception as e:
                    fails += 1
                    print("Error with request for "+conf["YS"][streamer]+"'s stream. Attempts remaining: "+str(3-fails)+"/3")
                    print("Error was more than an invalid response. Details:\n",e)
            # If they haven't tagged their stream, this will fail anyway
            if 'tags' not in expand['items'][0]['snippet']:
                print("Streamer has not tagged their stream. Giving up.")
                continue 
            # Check if they're streaming the right game
            for name in conf["G"]:
                if (name.lower().replace(' ','') in [ game.lower().replace(' ','').replace(":","").replace("=","") for game in expand['items'][0]['snippet']['tags'] ]
                and status.title.string[2:-11] not in statusSection):
                    # Make a link to the stream with the streamer's username as the link title
                    statusSection += "* [" + status.title.string[2:-11] + " - " + title + "](" + "https://www.youtube.com" + stream.a['href'] + ")\n\n"
    if statusSection == "\n\n****\n\n**Streaming now:**\n\n":
        # If no one is streaming
        statusSection += "* No active streams\n\n"
    print("All streamer statuses retrieved. Checking if sidebar should update...")
    # This ensures the sidebar is redownloaded on every check instead of using the cached one
    sub = R.subreddit(conf["M"]["mySub"])
    # Get sidebar
    sidebar = sub.description
    # Figure out where to put the streamer statuses
    try:
        preFeed = re.search("(.*)\n\n[*]*\n\n[*]*Streaming now:[*]*.*",sidebar,flags=re.DOTALL).group(1)
    except:
        print("preFeed failure. Assuming bottom attachment.")
        preFeed = sidebar
    try:
        postFeed = "****"+re.search(".*\n\n[*]*\n\n[*]*Streaming now:[*]*.*[*]{4}(.*)",sidebar,flags=re.DOTALL).group(1)
    except:
        print("postFeed failure")
        postFeed = "****"
    if sidebar != preFeed+statusSection+postFeed:
        sub.mod.update(description=preFeed+statusSection+postFeed)
        print(time.strftime("%D, %H:%M-\n    ")+"Sidebar was updated")

def checkInbox():
    # Get current moderator list
    mods = [ mod.name for mod in R.subreddit(conf["M"]["mySub"]).moderator() ]
    for message in R.inbox.unread():
        if not message.author.name in mods or message.subject in ["username mention","comment reply"]:
            # If it's not from the moderators or a direct PM,
            # we don't care
            continue
        print("Message from moderator!")
        fails = 0
        for parser in ["Add YouTube streamer","Add Twitch streamer","Add game","Remove YouTube streamer","Remove Twitch streamer","Remove game"]:
            try:
                thing = re.search(parser+": (.*)",message.body).group(1)
                figurer = parser.split(" ")
                if figurer[0] == "Add":
                    try:
                        addThing(thing,figurer[1][0]+figurer[2][0].upper())
                    except Exception as e:
                        message.reply("Error when adding "+thing+"\n\nDetails:"+str(e))
                        message.mark_read()
                        continue
                else:
                    try:
                        delThing(thing,figurer[1][0]+figurer[2][0].upper())
                    except:
                        message.reply(thing+" not found, so not removed.")
                        message.mark_read()
                        continue
                if figurer[0][-1] == "d":
                    figurer[0] += "e"
                figurer[0] += "d"
                message.reply("Successfully "+figurer[0].lower()+" "+figurer[2])
                message.mark_read()
                print("Successfully handled")
                continue
            except:
                fails += 1
        if fails == 6:
            message.reply("Error with request. Please use one of the following:\n\n"
                          "* `Add YouTube streamer: CHANNEL-ID HUMAN-READABLE-NAME`\n\n"
                          "* `Add Twitch streamer: NAME`\n\n"
                          "* `Add game: NAME`\n\n"
                          "* `Remove Twitch streamer: NAME`\n\n"
                          "* `Remove YouTube streamer: HUMAN-READABLE-NAME`\n\n"
                          "* `Remove game: NAME`")
            message.mark_read()
            print("Error handling message")

########################################################################
#                                                                      #
#    Script Startup                                                    #
#                                                                      #
########################################################################

try:
    mods = ["praw",
            "re",
            "configparser",
            "time",
            "requests",
            "json",
            "bs4"]
    for mod in mods:
        print("Importing "+mod)
        exec("import "+mod)
except:
    exit(mod+" was not found. Install "+mod+" with pip to continue.")

# Flip the filepath backwards, look for the first non-alphanumeric character,
# grab the rest, then flip it forwards again. This theoretically gets the
# folder the script is in without using the os module.
myPath = re.search(r"[a-zA-Z0-9. ]*(.*)",__file__[::-1]).group(1)[::-1]

try:
    configSections = ["R","T","Y","M","G","TS","YS"]
    conf = loadConfig(myPath)
except Exception as e:
    print("Error details:\n"+str(e.args))
    conf = makeCreds(myPath)

# Normalize credentials
conf["R"]["u"] = conf["R"]["u"].replace("/u/","").replace("u/","")
conf["M"]["mySub"] = conf["M"]["mySub"].replace("/r/","").replace("r/","")
conf["M"]["botMaster"] = conf["M"]["botMaster"].replace("/u/","").replace("u/","")

## Reddit authentication
R = praw.Reddit(client_id = conf["R"]["c"],
                client_secret = conf["R"]["s"],
                password = conf["R"]["p"],
                user_agent = "BasicBotTemplate, a bot for /r/"+conf["M"]["mySub"]+"; hosted by /u/"+conf["M"]["botMaster"],
                username = conf["R"]["u"])

print("Bot successfully loaded. Entering main loop.")

########################################################################
#                                                                      #
#    Script Actions                                                    #
#                                                                      #
########################################################################
while True:
    try:
        startTime = time.time()
        checkInbox()
        updateSidebar()
        endTime = time.time()
        # Sleep if we completed the job in under the refresh rate,
        # otherwise restart the loop immediately
        if eval(conf["M"]["sleepTime"]) - endTime + startTime > 0:
            time.sleep(eval(conf["M"]["sleepTime"]) - endTime + startTime)
    except Exception as e:
        i=1
        e=e
        while True:
            lastError = eval("e.__traceback__"+".tb_next"*i)
            if lastError == None:
                lineNumber = eval("e.__traceback__"+".tb_next"*(i-1)+".tb_lineno")
                break
            i += 1
        print("Error!\n\n  Line "+str(lineNumber)+" -> "+e.__str__())
        endTime = time.time()
        if eval(conf["M"]["sleepTime"]) - endTime + startTime > 0:
            time.sleep(eval(conf["M"]["sleepTime"]) - endTime + startTime)
