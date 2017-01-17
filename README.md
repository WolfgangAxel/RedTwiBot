# RedTwiBot
A Reddit/Twitch bot that will update your subreddit statusbar when streamers are playing your sub's game.

## Usage
Make a folder on whatever host computer you'll be using. Download `RedTwiBot.py` into that folder, then create the following:

* `streamers.txt`
* `sidebar.md`

`streamers.txt` should be a list of usernames of Twitch users who frequently stream your game. It should be new line separated like so:

    person-one
    person2
    PERSON_Three

`sidebar.md` should be the regular markdown for your subreddit's sidebar, however, where you want the links to appear insert the following:

    ====
    
    ====

Text both before and after these spacers will be preserved. Anything between them will be ignored and overwritten.

Lastly, before launching the script, you will need to open `RedTwiBot.py` and enter in the following in the appropriate areas near the top:

* The reddit bot's:
 * Username
 * Password
 * Client-id
 * Secret
 * Subreddit (must be a moderator, obviously)
 * hoster's personal account's username (Reddit's API requires it)
* The twitch account's client-id
* Any number of game titles (If your game has multiple versions or multiple titles or whatever.)
* Time in seconds between refreshes (Default is 180, a.k.a. 3 minutes)

## How it works

The bot first checks to make sure all files and variables are accounted for. If everything is good, it will try connecting to Reddit. If that is successful, it will read `streamers.txt` and download the stream status for each account in the list. If a stream is online and playing a game in your list of game names, the account name will be used as a link to the stream and will be added to your sidebar under a section called `Streaming now:`. If no-one on your list is streaming, the list will read `None :(`. If no new streams have started or ended since the last update, nothing happens. If there is a new stream or one ends, the sidebar will be updated. After the sidebar has (or hasn't) been updated, the bot will sleep for a duration of your choosing before starting the process over again from reading `streamers.txt`. This way, you may update the list of streamers at any time and the bot will always be using the updated list.
