# Sidebar Streamers
A Reddit/Twitch bot that will update your subreddit statusbar when streamers are playing your sub's game.

## Requirements

* [Python 3](https://pyython.org/downloads/)
 * [Praw](http://praw.readthedocs.io)
 * [Requests](docs.python-requests.org/)

## Usage
The script will ask for all necessary credentials on the first load. After that, all information is pulled from and maintained in `credentials.ini`.

The script will put the stream section at the bottom of the sidebar if it is not found elsewhere. Once made, you may move it around and what's above and below will be maintained. If you do move the section around, maintain the two line feeds above and below the two sets of `****` that sandwich the stream section.

Any moderator of the subreddit may message the bot with one of the following (note the spaces):

* `Add streamer: NAME`
* `Add game: NAME`
* `Remove streamer: NAME`
* `Remove game: NAME`

These will add and remove streamers and games from the list of acceptable/approved streamers and games. If a streamer is in this list, their status will be retrieved every time the bot updates, and if they are listed as playing a game on the list of games, a link to their stream will be put in the sidebar. When the stream stops, the link will be removed.

# Note

Due to how `configparser` is used, colons (`:`) and equal signs (`=`) will be removed from streamer names and game titles. Keep this in mind if you plan to use the `remove` PM options.
