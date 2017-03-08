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
            print("No values found for section "+item+".")
            while True:
                confirm = input("Proceed anyway? Proceeding without "
                                "certain values might cause errors down "
                                "the road (y/n)\n==> ")
                if confirm.lower() == "y":
                    print("Ignoring empty section.")
                    break
                elif confirm.lower() == "n":
                    print("Aborting!")
                    raise Exception
                else:
                    print("Confirmation failed.Restarting entry.")
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
    for things,dic in [["games",gameList],["streamers",strmList]]:
        print("We will now build the list of acceptable "+things)
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
                    dic[thing.lower()] = "Good"
                    print("Added "+thing)
            else:
                print("No "+things[:-1]+" entered. Nothing to add.")
    
    conf["R"] = redCreds
    conf["T"] = twiCreds
    conf["M"] = mscCreds
    conf["G"] = gameList
    conf["S"] = strmList
    saveConfig()
    return conf

#### Utility

def addThing(thing,kind):
    """
    Add a thing to the list and save the file.
    """
    conf[kind][thing.lower()] = "Good"
    saveConfig()

def delThing(thing,kind):
    """
    Remove a thing from the list and save the file.
    """
    _ = conf[kind].pop(thing.lower())
    saveConfig()

def updateSidebar():
    statusSection = "\n\n****\n\n**Streaming now:**\n\n"
    for streamer in conf["S"]:
        # Get the status
        status = requests.get("https://api.twitch.tv/kraken/streams/"+streamer,
                              headers={'Accept':'application/vnd.twitchtv.v3+json',
                                       'Client-ID':conf["T"]["c"]})
        # Parse it
        status = json.loads(str(status.content,'utf-8'))
        # Check if they're streaming at all
        if status['stream']:
            print(streamer+" is playing "+status['stream']['game'])
            # Check if they're streaming the right game
            if status['stream']['game'].lower().replace(' ','') in [ name.lower().replace(' ','') for name in conf["G"] ]:
                # Make a link to the stream with the streamer's username as the link title
                statusSection += "* [" + streamer + "](" + status['stream']['channel']['url'] + ")\n\n"
    if statusSection == "\n\n****\n\n**Streaming now:**\n\n":
        # Make a sad face if no-one is streaming
        statusSection += "* None :(\n\n"
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
        for parser in ["Add streamer","Add game","Remove streamer","Remove game"]:
            try:
                thing = re.search(parser+": (.*)",message.body).group(1)
                figurer = parser.split(" ")
                if figurer[0] == "Add":
                    addThing(thing,figurer[1][0].upper())
                else:
                    try:
                        delThing(thing,figurer[1][0].upper())
                    except:
                        message.reply(thing+" not found, so not removed.")
                        message.mark_read()
                        continue
                if figurer[0][-1] == "d":
                    figurer[0] += "e"
                figurer[0] += "d"
                message.reply("Successfully "+figurer[0].lower()+" "+figurer[1])
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
    configSections = ["R","T","M","G","S"]
    conf = loadConfig(myPath)
except Exception as e:
    input(str(e.args)+"\nPress enter to regenerate the configuration file.")
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
        checkInbox()
        updateSidebar()
        time.sleep(eval(conf["M"]["sleepTime"]))
    except Exception as e:
        print("Error!\n\n"+str(e.args)+"\n\nRetrying in one minute.")
        time.sleep(60)
