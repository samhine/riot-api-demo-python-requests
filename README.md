# riot-api-demo
Short demonstration to show how the Riot API can queried use Python and requests

## Riot API Key

Before doing anything, you need a key to make requests to the Riot API. Riot requires this so they can monitor your usage, and thottle you if needed.

To get a Riot API key, you must make a developer account - all the information you need can be found here https://developer.riotgames.com/docs/portal.

Your key will look something like this `RGAPI-aa56eod5-a985-4g41-b2a4-ebb75jb2fa0e`.

## Python and Requests

Python is a progamming language which allows you to be relatively concise while defining tasks. It's quite easy to learn, and very powerful when mastered. You can install Python from their website, I'll be using Python 3.7.4, but any 3.X version will work https://www.python.org/downloads/release/python-374/. Navigate to the "Files" section, and download the appropirate installer - allow all options when the installer asks about PATH variables.

Requests is a module in Python, which allows you to make RESTful requests. REST is simply an agreed upon standard of how a server (in this case Riot's API) and a client (your Python script) should communicate. Riot gives you everything you need to know about the server side of this communication in their API reference https://developer.riotgames.com/apis.

Before starting the following, I'd take a day or two learning basic Python syntax using one of many online tutorials.

## Getting started

Our first task is to install the `requests` module. For this we need to use the command line. Open up your terminal of choice, and type
```pip install requests```
This now means you can use the requests module in any Python program you create through a simple import.

You need to create a project directory. Create a folder anywhere to store the files we'll be creating.

Create a new file called `main.py`, and open it using your favourite text editor. I use VS Code (https://code.visualstudio.com/).

To run `main.py` at any point to check your code is working, open a terminal in the directory and type `python main.py` (if you can't access access Python this way try following this tutorial: https://www.youtube.com/watch?v=BArhFr06nPM).

Inside the `main.py` file we'll need a few things, copy and paste the following (NB: lines starting with a # are comments, not actual code).

```
# Importing the requests library
import requests
# JSON is installed by default, and allows us to read responses from Riot
import json

# Defining our API key
secret = "YOUR-API-KEY-HERE"

# Headers for all our requests
headers = {
    'X-Riot-Token':secret
}

```

The above contains everything you need to start making custom requests!
For this example, I want to view all the data associated to my most recently played game. The endpoints we'll be using for this are;

https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName - To find my summoner ID, which is needed to make further requests about myself.

https://developer.riotgames.com/apis#match-v4/GET_getMatchlist - To find my match history.

https://developer.riotgames.com/apis#match-v4/GET_getMatch - To find information about a specific game.

## Making our first request

To find information about a player, Riot requires that you use something called an "encrypted account ID", so we have to find out what mine is to make further queries.

```
# We want to GET information from the URL specified, and include our API key so Riot knows it can provide this information. GET is a RESTful standard, and is used to retrieve information from an API (there are others, such as UPDATE, DELETE and POST).
response = requests.get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Montagne", headers=headers)
# Format the request into JSON to make it readable
response_readable = response.json()
# Index (query) the readable response to find the encrypted account ID
account_id = response_readable["accountId"]
# Gives: DhP5nm0xSVcAr1NJ_v1HsiazPXvRTsmbPSn0RmFYhRtCSQ8
```

The above might seem a bit confusing the first time you read through it, but is the core of all the requests we'll be making.

1. Format a URL to find the information you need
2. Attach the headers to make sure we're authenticated
3. Make the request, and convert it into a readable format
4. Grab the information we need from the readable response

The indexing stage can get more and more confusing for different types of request. As you can imagine, theres a lot of data for a game, and it can be hard to grab the information you need.

## Finding the information we need

I want to find the amount of kills I had for my most recently played game. We'll need to follow these steps;

1. Make a request to see my last 100 matches 
2. Find the ID of my most recent match
3. Make a request to find all the information about this match
4. Wrangle the response to pick out the information we need

So, let's get started.

```
# Construct the URL. We can use + to "concatenate" two strings (sections of text) together; here we're plugging in the account ID for the summoner we want the matches for (me). 
recent_games = requests.get("https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/"+account_id, headers=headers)
# Convert it to a readable format
recent_games_readable = recent_games.json()
# Find the ID of my most recent (0th) game
most_recent_game_id = recent_games_readable["matches"][0]["gameId"]
```

Now we have the ID of my most recent game, we can get started on finding everything out about it, which is another endpoint.

```
# Contruct URL using ID we just found, and chain the JSON command to make it readable straight away.
game_info_readable = requests.get("https://euw1.api.riotgames.com//lol/match/v4/matches/"+str(most_recent_game_id), headers=headers).json()
print(json.dumps(game_info_readable, indent=4, sort_keys=True))
```

Now, this data is quite convoluted due to the volume of information it contains. Reading through https://developer.riotgames.com/apis#match-v4/GET_getMatch, you can see how it's all structured, but this can quite hard to interpret. At this point, I'd recommend reading the printed output and getting a feel for everything.

Something to mention is that all in game statistics are assigned to something called a "participantId", and new participantId's are assigned for every game. Our first step is to find my participantId for this specific game.

```
# Grab all the participant information
participant_info = game_info_readable["participantIdentities"]
# For each player in the information, if we find me, extract my ID
for player in participant_info:
    if player["player"]["summonerName"] == "Montagne":
        my_participant_id = player["participantId"]
```

The above is our first taste of complex querying from data that's given back to us from the API. We have to use a loop to see the information we need, instead of using basic indexing.

Now we have the participant ID, we're ready to find the amount of kills I had this game.

```
# Participants holds all the juicy information about a plyer
player_statistics = game_info_readable["participants"]
# We loop through again to find out which one is me
for player in player_statistics:
    if player["participantId"] == my_participant_id:
        my_statistics = player["stats"]

# Simply index my kills from the statistics
my_kills = my_statistics["kills"]
```

And we're done! 
Obviously, this is a small piece of information which is relatively unimportant by itself. Instead, it's common to grab all the statistics about a player and place it into a table for later use - using something like Pandas (https://github.com/pandas-dev/pandas).

## Follow up

There are some Python libraries out there which handle a lot of the fluff of making requests (for example: https://github.com/pseudonym117/Riot-Watcher). Over time however, making a lot of these basic requests can be put into functions (pieces of reusable code) so you don't need to repeat yourself so often.

As you improve at Python in general, the process of extracting the pieces of data you want, and manipulating it, becomes a lot easier and very powerful.
Tens of thousands of games can be analysed over the course of a few minutes.

