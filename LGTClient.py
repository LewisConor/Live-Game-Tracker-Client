#Created by Conor Lewis / Uploaded on 11/07/2022
#This is a client for the Live Game Tracker Extension.
#It is a simple client that will connect to the game client and send the game data to the server.
#It will also delete the game data at the end of the game too.
import urllib3
import os
import requests
import time
import json
import math
from collections import Counter

#Complains at Client URL because it doesnt have SSL Certs
urllib3.disable_warnings()

#Variables
username = ""
ext = ".json"
lastRequest = None

playerID = 0

oldAbilityList = None
abilityOrder = []

oldItemList = None
oldItemListLength = 0
addedItems = {"items": [], "time": 0}
itemOrder = []
regionJsonData = { 'region': 'Null' }

lastInfo = []

#Opening Code
print("Welcome to the Live Game Tracker Client.")
print("Select your Region (Number):\n1. BR\n2. EUW\n3. EUNE\n4. JP\n5. KR\n6. LAN\n7. LAS\n8. NA\n9. OCE\n10. RU\n11. TR\n12. TW")

#Region Selection
while regionJsonData['region'] == 'Null':
    region = int(input("Region Num: "))

    if(region < 0 or region > 12):
        print("Invalid Region")
        continue
    else:
        if(region == 1):
            regionJsonData['region'] = "br"
        elif(region == 2):
            regionJsonData['region'] = "euw"
        elif(region == 3):
            regionJsonData['region'] = "eune"
        elif(region == 4):
            regionJsonData['region'] = "jp"
        elif(region == 5):
            regionJsonData['region'] = "kr"
        elif(region == 6):
            regionJsonData['region'] = "lan"
        elif(region == 7):
            regionJsonData['region'] = "las"
        elif(region == 8):
            regionJsonData['region'] = "na"
        elif(region == 9):
            regionJsonData['region'] = "oce"
        elif(region == 10):
            regionJsonData['region'] = "ru"
        elif(region == 11):
            regionJsonData['region'] = "tr"

#Main Loop
while True:
    os.system("cls")
    print("Welcome to the Live Game Tracker Client. Listening for Client Game Data from 127.0.0.1:2999")

    for i in range(len(lastInfo)):
        print(lastInfo[i])

    #Waits Every 5 Seconds for Data
    time.sleep(5 - time.time() % 5)

    lastInfo = []
    
    #Attempt Requests with Game
    try:
        request = requests.get("https://127.0.0.1:2999/liveclientdata/allgamedata", verify = False)
        
        if(request.status_code == 200):
            jsonData = request.json()

            lastInfo.append("Game Data acquired at Game Time: " + str(math.trunc(jsonData["gameData"]["gameTime"]) / 60))
            
            if(username == ""):
                requestName = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayername", verify = False)
                if(requestName.status_code == 200):
                    username = requestName.json()
                else:
                    print("Error getting Player Name")
            else:
                for i in range(len(jsonData["allPlayers"])):
                    if(jsonData["allPlayers"][i]["summonerName"] == username):
                        playerID = i
                        break


                #Ability Order Data
                if(oldAbilityList == None):
                    oldAbilityList = jsonData["activePlayer"]["abilities"]
                    
                    for i in range(4):
                        if(i == 0):
                            if(oldAbilityList["Q"]["abilityLevel"] == 1):
                                abilityOrder.append("Q")
                                break
                        
                        if(i == 1):
                            if(oldAbilityList["W"]["abilityLevel"] == 1):
                                abilityOrder.append("W")
                                break
                        
                        if(i == 2):
                            if(oldAbilityList["E"]["abilityLevel"] == 1):
                                abilityOrder.append("E")
                                break
                        
                        if(i == 3):
                            if(oldAbilityList["R"]["abilityLevel"] == 1):

                                abilityOrder.append("R")
                                break
                else:
                    newAbilityList = jsonData["activePlayer"]["abilities"]
                    if(newAbilityList != oldAbilityList):
                        for i in range(4):
                            if(i == 0):
                                if(oldAbilityList["Q"]["abilityLevel"] != newAbilityList["Q"]["abilityLevel"]):
                                    abilityOrder.append("Q")
                                    break
                            
                            if(i == 1):
                                if(oldAbilityList["W"]["abilityLevel"] != newAbilityList["W"]["abilityLevel"]):
                                    abilityOrder.append("W")
                                    break
                            
                            if(i == 2):
                                if(oldAbilityList["E"]["abilityLevel"] != newAbilityList["E"]["abilityLevel"]):
                                    abilityOrder.append("E")
                                    break
                            
                            if(i == 3):
                                if(oldAbilityList["R"]["abilityLevel"] != newAbilityList["R"]["abilityLevel"]):
                                    abilityOrder.append("R")
                                    break
                        
                        oldAbilityList = newAbilityList

                #Item Order Data
                itemData = jsonData["allPlayers"][playerID]["items"]
                itemDataLength = len(itemData)

                if(oldItemList == None):
                    if(itemDataLength > 0):
                        for i in itemData:
                            addedItems["items"].append(i["itemID"])
                    
                        addedItems["time"] = math.trunc(jsonData["gameData"]["gameTime"]) / 60
                        itemOrder.append(addedItems)
                        
                        oldItemList = itemData
                        oldItemListLength = itemDataLength
                else:
                    addedItems = {"items": [], "time": 0}
                    if(itemDataLength > 0):
                        if(itemDataLength > oldItemListLength):
                            oldIDs = []
                            for i in oldItemList:
                                oldIDs.append(i["itemID"])

                            newIDs = []
                            for i in itemData:
                                newIDs.append(i["itemID"])

                            difference = list((Counter(newIDs) - Counter(oldIDs)).elements())

                            for i in difference:
                                for j in itemData:
                                    if(j["itemID"] == i):
                                        addedItems["items"].append(j["itemID"])
                                        break
                            
                            if(len(addedItems["items"]) > 0):
                                addedItems["time"] = math.trunc(jsonData["gameData"]["gameTime"]) / 60
                                itemOrder.append(addedItems)

                            oldItemList = itemData
                            oldItemListLength = itemDataLength
                        elif(itemDataLength < oldItemListLength or itemDataLength == oldItemListLength):
                            oldIDs = []
                            for i in oldItemList:
                                oldIDs.append(i["itemID"])

                            newIDs = []
                            for i in itemData:
                                newIDs.append(i["itemID"])

                            difference = list(set(newIDs) - set(oldIDs))

                            for i in difference:
                                for j in itemData:
                                    if(j["itemID"] == i):
                                        addedItems["items"].append(j["itemID"])
                                        break
                            
                            if(len(addedItems["items"]) > 0):
                                addedItems["time"] = math.trunc(jsonData["gameData"]["gameTime"]) / 60
                                itemOrder.append(addedItems)

                            oldItemList = itemData
                            oldItemListLength = itemDataLength
        
                jsonData["abilityOrder"] = abilityOrder
                jsonData["itemOrder"] = itemOrder

                fileName = username + ext
                data = open(fileName, "w")
                data.write(json.dumps(jsonData))
                data.close()

                try:
                    f = {'file': open(fileName, 'rb')}
                    r = requests.post("https://conorlewis.net/streamerGameData/upload.php", data=regionJsonData, files=f)
                    if(r.status_code == 200):
                        lastInfo.append("Data Uploaded to Server")
                    else:
                        lastInfo.append("Error Uploading Data")
                except:
                    lastInfo.append("Error Uploading Data")
        else:
            lastInfo.append("Game Entered Loading State")

        lastRequest = request
    except:
        lastInfo.append("Not in Game")
        if(lastRequest != None):
            lastRequest = None
            oldAbilityList = None
            abilityOrder = []

            oldItemList = None
            oldItemListLength = 0
            addedItems = {"items": [], "time": 0}
            itemOrder = []

            r = requests.post("https://conorlewis.net/streamerGameData/delete.php", data = {'fileName': username, 'region': regionJsonData['region']})
            if(r.status_code == 200):
                lastInfo.append("Data Deleted from Server")