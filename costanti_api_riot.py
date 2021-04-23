API_KEY = "api_key=RGAPI-4592796f-cdba-454d-87f8-8cc9c3543c55"

#query
SUMMONER = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{0}?"+API_KEY
MATCHES_ID_BY_PUUID = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?start={1}&count={2}&"+API_KEY
MATCH_BY_ID = "https://europe.api.riotgames.com/lol/match/v5/matches/{0}?"+API_KEY
MATCH_TIMELINE_BY_ID = "https://europe.api.riotgames.com/lol/match/v5/matches/{0}/timeline?"+API_KEY

#assets
ITEMS = "http://ddragon.leagueoflegends.com/cdn/11.8.1/data/en_US/item.json" 
