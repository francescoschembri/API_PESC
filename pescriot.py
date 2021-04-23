import requests
from costanti_api_riot import *


def getPlayerInfo(name):
    return requests.get(SUMMONER.format(name)).json()

def getMatchesIdOfPlayer(name, num_matches = 10):
    player_puuid = getPlayerInfo(name)["puuid"]
    return requests.get(MATCHES_ID_BY_PUUID.format(player_puuid, 0, num_matches)).json()


def getMatchInfoById(id):
    return requests.get(MATCH_BY_ID.format(id)).json()
    
def getPatchOfMatchId(id):
    return getMatchInfoById(id)["info"]["gameVersion"]

def getInfoOfPlayerInMatchId(name, id):
    info = getMatchInfoById(id)["info"]["participants"]
    for p in info:
        if p["summonerName"] == name:
            return p

def getChampionOfPlayerInMatchId(name, id):
    return getInfoOfPlayerInMatchId(name, id)["championName"]

'''
def getOpponentChampionOfPlayerInMatchId(name, id):
    info = getInfoOfPlayerInMatchId(name, id)
    role = info[""]
    '''

def hasPlayerWonInMatchId(name, id):
    if getInfoOfPlayerInMatchId(name, id)["win"]: return "W"
    return "L"

def getKillsOfPlayerInMatchId(name, id):
    return getInfoOfPlayerInMatchId(name, id)["kills"]

def getDeathsOfPlayerInMatchId(name, id):
    return getInfoOfPlayerInMatchId(name, id)["deaths"]

def getAssistsOfPlayerInMatchId(name, id):
    return getInfoOfPlayerInMatchId(name, id)["assists"]
    
def getKDAOfPlayerInMatchId(name, id):
    return "{:0.2f}".format((getKillsOfPlayerInMatchId(name, id) + 
    getAssistsOfPlayerInMatchId(name, id))/getDeathsOfPlayerInMatchId(name, id))

def getParticipantIdInMatchId(name, id):
    return getInfoOfPlayerInMatchId(name, id)["participantId"]

def getMatchTimelineInfoById(id):
    return requests.get(MATCH_TIMELINE_BY_ID.format(id)).json()["info"]

def getItemFromId(id):
    return requests.get(ITEMS).json()["data"][str(id)]["name"]

def skillSlotToChar(slot):
    if slot == 1: return "Q"
    if slot == 2: return "W"
    if slot == 3: return "E"
    if slot == 4: return "R"

def getSkillOrderOfPlayerInMatchId(name, id):
    participantId = getParticipantIdInMatchId(name, id)
    frames = getMatchTimelineInfoById(id)["frames"]
    events = [frame["events"] for frame in frames]
    events = [e for event in events for e in event if e["type"] == "SKILL_LEVEL_UP" and e["participantId"] == participantId]
    skills = [skillSlotToChar(e["skillSlot"]) for e in sorted(events, key = lambda e: e["timestamp"])]
    skill_order = skills[0]
    for skill in skills[1:]:
        skill_order += " > " + skill
    return skill_order


def getBuildPathOfPlayerInMatchId(name, id):
    participantId = getParticipantIdInMatchId(name, id)
    frames = getMatchTimelineInfoById(id)["frames"]
    events = [frame["events"] for frame in frames]
    events = [e for event in events for e in event if e["type"] == "ITEM_PURCHASED" and e["participantId"] == participantId]
    events = sorted(events, key = lambda e: e["timestamp"])
    build_path = getItemFromId(events[0]["itemId"])
    for event in events[1:]:
        build_path += " > " + getItemFromId(event["itemId"])
    return build_path
    
def getGoldEarndInMatchWithIdByPlayer(name, id):
    return getInfoOfPlayerInMatchId(name, id)["goldEarned"]

def getTotalDamageDealtInMatchWithIdByPlayer(name, id):
    return getInfoOfPlayerInMatchId(name, id)["totalDamageDealt"]

def getCsFarmaedInMatchWithIdByPlayer(name, id):
    return getInfoOfPlayerInMatchId(name, id)["totalMinionsKilled"] + getInfoOfPlayerInMatchId(name, id)["neutralMinionsKilled"]

def makeSpreadSheetRowForMatchIdOfPlayer(name, id):
    return [getChampionOfPlayerInMatchId(name, id), "",
                "?", "", getPatchOfMatchId(id), 
                hasPlayerWonInMatchId(name, id),
                getKillsOfPlayerInMatchId(name,id), 
                getDeathsOfPlayerInMatchId(name, id),
                getAssistsOfPlayerInMatchId(name, id), 
                getKDAOfPlayerInMatchId(name, id),
                "?", 
                getGoldEarndInMatchWithIdByPlayer(name,id), 
                getTotalDamageDealtInMatchWithIdByPlayer(name,id), 
                getSkillOrderOfPlayerInMatchId(name, id), 
                getBuildPathOfPlayerInMatchId(name, id)]

def makeSpreadSheetRowsOfPlayer(name, num_games):
    ids = getMatchesIdOfPlayer(name, num_games)
    rows = [(print(id), makeSpreadSheetRowForMatchIdOfPlayer(name, id)) for id in ids]
    return [e[1] for e in rows]
