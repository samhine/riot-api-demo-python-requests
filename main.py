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

# We want to GET information from the URL specified, and include our API key so Riot knows it can provide this information. GET is a RESTful standard, and is used to retrieve information from an API (there are others, such as UPDATE, DELETE and POST).
response = requests.get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Montagne", headers=headers)
# Format the request into JSON to make it readable
response_readable = response.json()
# Index (query) the readable response to find the encrypted account ID
account_id = response_readable["accountId"]
# Gives: 

# Construct the URL. We can use + to "concatenate" two strings (sections of text) together; here we're plugging in the account ID for the summoner we want the matches for (me). 
recent_games = requests.get("https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/"+account_id, headers=headers)
# Convert it to a readable format
recent_games_readable = recent_games.json()
# Find the ID of my most recent (0th) game
most_recent_game_id = recent_games_readable["matches"][0]["gameId"]

# Contruct URL using ID we just found, and chain the JSON command to make it readable straight away.
game_info_readable = requests.get("https://euw1.api.riotgames.com//lol/match/v4/matches/"+str(most_recent_game_id), headers=headers).json()
print(json.dumps(game_info_readable, indent=4, sort_keys=True))

# Grab all the participant information
participant_info = game_info_readable["participantIdentities"]
# For each player in the information, if we find me, extract my ID
for player in participant_info:
    if player["player"]["summonerName"] == "Montagne":
        my_participant_id = player["participantId"]

# "participants" holds all the juicy information about a plyer
player_statistics = game_info_readable["participants"]
# We loop through again to find out which one is me
for player in player_statistics:
    if player["participantId"] == my_participant_id:
        my_statistics = player["stats"]

# Simply index my kills from the statistics
my_kills = my_statistics["kills"]