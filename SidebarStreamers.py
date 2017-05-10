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
    print("Next, we will get the bot's Twitch information.")
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
    strmList = {}
    for things,dic in [["games",gameList],["twitch streamers",strmList]]:
        print("We will now build the list of acceptable "+things)
            input("Press enter to continue... ")
        while True:
            print("The current list of acceptable "+things+" is:")
            for thing in dic:
                print("    "+thing)
            print()
            again=input("Add another?\n(y/n): ")
            if again.lower() == 'n':
                break
            thing=input("Type in the name of one acceptable "+things[:-1]+": ")
            if thing:
                confirm=input("Add '"+thing+"' as an acceptable "+things[:-1]+"?\n(y/n): ")
                if confirm.lower() == 'y':
                    dic[thing] = "Good"
                    print("Added "+thing)
            else:
                print("No "+things[:-1]+" entered. Nothing to add.")
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
                    dic[thing] = human
                    print("Added "+thing)
            else:
                print("No YouTube streamer entered. Nothing to add.")
    
    conf["R"] = redCreds
    conf["T"] = twiCreds
    conf["Y"] = gytCreds
    conf["M"] = mscCreds
    conf["G"] = gameList
    conf["TS"] = strmList
    conf["YS"] = ytstList
    saveConfig()
    return conf

#### Utility

def addThing(thing,kind):
    """
    Add a thing to the list and save the file.
    """
    if thing != "YS":
        conf[kind][thing.lower().replace(":","").replace("=","")] = "Good"
    else:
        ID = re.search("(.+?) ",thing)
        human = re.search(".+ (.+)")
        conf[kind][ID] = human
    saveConfig()

def delThing(thing,kind):
    """
    Remove a thing from the list and save the file.
    """
    if thing != "YS":
        _ = conf[kind].pop(thing.lower())
    else:
        _ = conf[kind].pop( [s for s in conf[kind] if conf[kind][s] == thing][0] )
    saveConfig()

def updateSidebar():
    statusSection = "\n\n****\n\n**Streaming now:**\n\n"
    ############################################################ Twitch
    for streamer in conf["TS"]:
        fails = 0
        while True:
            # Get the status
            status = requests.get("https://api.twitch.tv/kraken/streams/"+streamer,
                                  headers={'Accept':'application/vnd.twitchtv.v3+json',
                                           'Client-ID':conf["T"]["c"]})
            # Be nice to Twitch servers
            time.sleep(0.5)
            # Parse it
            status = json.loads(str(status.content,'utf-8'))
            # If there were no errors, then keep going
            # If there were errors, try again
            # If there were 10 consecutive errors, skip it (handled later).
            if not "error" in status or fails > 8:
                break
            fails += 1
            print("Error with request for "+streamer+"'s stream. Attempts remaining: "+str(10-fails)+"/10")
        # Check if they're streaming at all
        try:
            if status['stream']:
                print(streamer+" is playing "+status['stream']['game'])
                # Check if they're streaming the right game
                if status['stream']['game'].lower().replace(' ','').replace(":","").replace("=","") in [ name.lower().replace(' ','') for name in conf["G"] ]:
                    # Make a link to the stream with the streamer's username as the link title
                    statusSection += "* [" + streamer + " - " + status['stream']['game'] + "](" + status['stream']['channel']['url'] + ")\n\n"
        except:
            print("Status of "+streamer+" exceeded too many failed attempts. "
                  "If problems persist with this streamer, open an issue here: "
                  "https://github.com/WolfgangAxel/RedTwiBot/issues/new\n"
                  "Request response was: ")
            print(status)
            print("Skipping.")
            continue
    ########################################################### Youtube
    for streamer in conf["YS"]:
        fails = 0
        while True:
            # Get the status
            status = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+
                                  streamer+"&type=video&eventType=live&key="+conf["Y"]["k"])
            # Be nice to Google servers
            time.sleep(0.5)
            # Parse it
            status = json.loads(str(status.content,'utf-8'))
            # If there were no errors, then keep going
            # If there were errors, try again
            # If there were 10 consecutive errors, skip it (handled later).
            if not "error" in status or fails > 8:
                break
            fails += 1
            print("Error with request for "+streamer+"'s stream. Attempts remaining: "+str(10-fails)+"/10")
        # Check if they're streaming at all
        try:
            if status['items']:
                print(streamer+" is streaming "+status['items'][0]['snippet']['title'])
                # Check if they're streaming the right game
                for name in conf["G"]:
                    if name.lower().replace(' ','') in status['items'][0]['snippet']['title'].lower().replace(' ','').replace(":","").replace("=",""):
                        # Make a link to the stream with the streamer's username as the link title
                        statusSection += "* [" + status['items'][0]['snippet']['channelTitle'] + " - " + status['items'][0]['snippet']['title'] + "](" + "https://www.youtube.com/watch?v=" + status['items'][0]['id']['videoId'] + ")\n\n"
        except:
            print("Status of "+streamer+" exceeded too many failed attempts. "
                  "If problems persist with this streamer, open an issue here: "
                  "https://github.com/WolfgangAxel/RedTwiBot/issues/new\n"
                  "Request response was: ")
            print(status)
            print("Skipping.")
            continue
    
    if statusSection == "\n\n****\n\n**Streaming now:**\n\n":
        # If no one is streaming
        statusSection += "* No active streams\n\n"
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
        if not message.author.name in mods:
            # If it's not from the moderators, we don't care
            message.mark_read()
            continue
        print("Message from moderator!")
        fails = 0
        for parser in ["Add YouTube streamer","Add Twitch streamer","Add game","Remove YouTube streamer","Remove Twitch streamer","Remove game"]:
            try:
                thing = re.search(parser+": (.*)",message.body).group(1)
                figurer = parser.split(" ")
                if figurer[0] == "Add":
                    addThing(thing,figurer[1][0]+figurer[2][0].upper())
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
        if fails == 4:
            message.reply("Error with request. Please use one of the following:\n\n"
                          "* `Add streamer: NAME`\n\n"
                          "* `Add game: NAME`\n\n"
                          "* `Remove streamer: NAME`\n\n"
                          "* `Remove game: NAME`")
            #message.mark_read()
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
            "json"]
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
        print("Error!\n\n  Line "+str(lineNumber)+" -> "+e.__str__()+"\n\nRetrying in one minute.")
        time.sleep(60)
