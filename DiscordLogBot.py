
import discord
from pathlib import Path
import json
import asyncio
import random
import os
from datetime import date
from datetime import datetime

client = discord.Client()
@client.event
#Just gets it ready
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
#message event triggers on message send
async def on_message(message):
    username = message.author
    #await message.channel.send("<@279425776892248064> is number 1 bitch>")
    #Makes sure the bot isn't detecting it's own messages 
    if message.author == client.user:
        return
    ## NEEDED VARIABLES FOR PATHING ETC
    userMessage = message.author.id
    messageContent = message.content
    finalMessage = userMessage, messageContent
    currentPath = os.path.dirname(os.path.realpath(__file__))
    workingPathFolder = currentPath + "\\" + str(userMessage) + "\\" + str(username)
    workingPathFileNew = workingPathFolder + "\\messageManifest 0.json"
    #simple filter list 
    filterList = ["!random",""]
    #debugging variable
    IncNumb = "0"
    
    #This is a function to create profiles for users who currently don't have logs 
    def CreateProfile():
        isFile = os.path.isfile(workingPathFileNew)
        if isFile == False and message.content not in filterList:
            print("No Profile Found Attemping Creation \n")
            try:
                Path(workingPathFolder).mkdir( parents=True, exist_ok=True )
                FileCreate = open(workingPathFileNew, 'w')
                FileCreate.close()
                print("Profile Creation Success \n")
            except:
                print("Profile Creation Failed \n")
            return
        else:
            return
    CreateProfile()
    
    #A random function for a user to see their own message randomly selected 
    if "!random" in message.content[0:7].lower():
        splitMessage = message.content.split(" ")
        if len(splitMessage) == 2:
            num = ""
            for c in splitMessage[1]:
                if c.isdigit():
                    num = num + c
            if str(num) in str(message.author.id):
                await message.channel.send("Please use !random without directing it with an <@" + str(message.author.id) + "> to select a message from yourself")
                return
            workingPathFolderForRandom = currentPath + "\\" + str(num)
            folderWalk = [x[0] for x in os.walk(workingPathFolderForRandom)]
            chosenRandom = random.randint(1, len(folderWalk) -1)
            workingPathFolder = folderWalk[chosenRandom]
            foundFiles = [x for x in os.listdir(workingPathFolder)]
            randomfile = random.randint(1, len(foundFiles) -1)
            print("selecting random file from: " + str(len(foundFiles)))
            print(workingPathFolder)
            selectionPath = workingPathFolder + "\\" + foundFiles[randomfile]
            fileChosen = open(selectionPath)
            loadedJson = json.load(fileChosen)
            fileChosen.close()
            await message.channel.send(loadedJson["message"] + " || " + loadedJson["date"])
            return
        else:
            foundFiles = [x for x in os.listdir(workingPathFolder)]
            randomfile = random.randint(1, len(foundFiles) -1)
            print("selecting random file from: " + str(len(foundFiles)))
            selectionPath = workingPathFolder + "\\" + foundFiles[randomfile]
            fileChosen = open(selectionPath)
            loadedJson = json.load(fileChosen)
            fileChosen.close()
            await message.channel.send(loadedJson["message"] + " || " + loadedJson["date"])
            return
    
    dateStamp = str(date.today()) + " " + str(datetime.now().strftime("%H:%M:%S"))
    #JSON FORMAT THE DATA IS STORED IN
    messageStorage = {
                     "message": message.content,
                     "date": dateStamp
                     }
                     
    print("message stored \n" + str(messageStorage))

    #A List Comprehension to create a list of all known items it can pull from.
    def count_files(dir):
        return len([1 for x in list(os.scandir(dir)) if x.is_file()])
    IncNumb = count_files(workingPathFolder)
    workingPathFileOld = workingPathFolder + "\\" + "messageManifest "+str(IncNumb)+".json" 
    with open(workingPathFileOld, "w") as write_file:
        json.dump(messageStorage, write_file)
        
    #EARLY CODE 
    #channel = message.channel
    #await channel.send(str(finalMessage))

    
