#!/usr/bin/env python3

#botCV.py

# Builtins

import os
import time
import random

# Pip Commands

import nextcord
from nextcord import *
from nextcord.ext import *
from dotenv import load_dotenv

# Made Commands

from DataParsing import *
from AjustingPoints import *
from QualityOfLife import *
from NPC import *

# import NPC

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv("DISCORD_GUILD")

TestMode = False

Channels = {"LogChannel" : [False], "CasinoState" : [False], "BlackJackTable" : [False]}

client = nextcord.Client()
serverIDS = []
TopPermissionValues = ["Some1and2#2570", "zanekyber#9825", "Spike#6128", "Bardock#4474", "Vintheruler1#7617"]
EmptyPoints = {'POG': 0, 'KEK': 0, 'SUS': 0, 'IQ': 0, 'COOKIES': 0, 'COOKIE-DATE': 0, 'NUTS': 0, 'TOTAL-NUTS': 0, 'RPG':{}}
CommandList = ["POG", "KEK", "SUS", "IQ", "COOKIES", "COOKIE", "NUT", "NUTS", "TOTAL-NUTS"]
ReactionEmojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    client.add_startup_application_commands()
    await client.rollout_application_commands()
    for guild in client.guilds:
        serverIDS.append(guild.id)



@client.event
async def on_raw_reaction_add(payload):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message.author == client.user:
        for i in message.reactions:
            if payload.member in await i.users().flatten() and not payload.member.bot and str(i) != str(payload.emoji):
                await message.remove_reaction(i.emoji, payload.member)

@client.slash_command(name="test", description="Testing slash command.", guild_ids=serverIDS)
async def test(interaction: Interaction):
    await interaction.response.send_message("testing testing 123")

@client.slash_command(name="pspspsps", description="Backing up the Points File",guild_ids=serverIDS)
async def pspspsps(interaction: Interaction):
    if str(interaction.user) in TopPermissionValues:
        with open("points.plk", "rb") as file:
            member = interaction.user
            chan = await member.create_dm()
            try:
                await chan.send("Here are the points: ", file=nextcord.File(file, "points.plk"))
                await interaction.response.send_message("Please check your DMS for the file.", ephemeral=True)
                #MAKE IT SEND IN THE USER DMS
            except Exception as e:
                await interaction.response.send_message(f"An error has occured: \n{e}")

            file.close()

        print(str(interaction.user.id) + " backed up point file")
        
        return
    else:
        await interaction.response.send_message("You are not in the TopPermission value!")

@client.event
async def on_message(message):
    global Channels, EmptyPoints, UserCards, CpuCards
    if message.author != client.user:

        if IfCommand(message, "pspspsps", TestMode) and str(message.author) in TopPermissionValues:
            with open("points.plk", "rb") as file:
                await message.author.send("Here are the points: ", file=nextcord.File(file, "points.plk"))
                file.close()
            print(str(message.author.id) + " backed up point file")
            return

        if IfCommand(message, "setloglocation", TestMode):
            if str(message.author) in TopPermissionValues:
                if not Channels["LogChannel"][0]:
                    Channels["LogChannel"].append(message)
                    Channels["LogChannel"][0] = True
                    print("Log Channel Set!")
                    return

        if IfCommand(message, "setblackjacktable", TestMode):
            if str(message.author) in TopPermissionValues:
                if not Channels["BlackJackTable"][0]:
                    Channels["BlackJackTable"][0] = True
                    Channels["BlackJackTable"].append(message)
                    print("Black Jack Table Set!")
                    return

        if IfCommand(message, "!kick", TestMode):
            if str(message.author) in TopPermissionValues:
                Channels["CasinoState"] = [False]
                return

        if IfCommand(message, "!points", TestMode):
            # Checks Users points +Ranking for each of the points
            rank = ""
            # Adds all of the points along with the rank# to a string
            for i in range(1, 9):
                PointType = IndexToKey(i)
                if PointType is not False:
                    rank += PointType + " RANK: #" + str(RankPoints(message.author.id, PointType))
                    if i != 8:
                        if i == 7:
                            rank += " and "
                        else:
                            rank += " | "
            ListOfPoints = ViewPoints(message.author.id)
            EndMessage = ReturnPointsString(message.author.id, ListOfPoints)
            await message.channel.send(f">>> {EndMessage}\n\n**{rank}**")
            return

        if IfCommand(message, "!cookie", TestMode):
            # This is for the !cookie command
            # If they did not get a cookie yet this will not return anything, if they did. This function will return false
            if GetCookie(message.author.id) is not False:
                ListOfPoints = ViewPoints(message.author.id)
                EndMessage = ReturnPointsString(message.author.id, ListOfPoints)
                rank = "COOKIES" + " RANK: #" + str(RankPoints(message.author.id, "COOKIES"))
                # print(ListOfPoints)
                print(EndMessage)
                print(rank)
                await message.channel.send(f">>> {EndMessage}\n\n`{rank}`")
            else:
                rank = "COOKIES" + " RANK: #" + str(RankPoints(message.author.id, "COOKIES"))
                await message.channel.send(">>> <@!{UserID}> *You already got a COOKIE today!*\n\n**{CookieAmnt} COOKIES | {rank}**".format(UserID=message.author.id, CookieAmnt=ViewPoints(message.author.id)["COOKIES"], rank=rank))

        if IfCommand(message, "!rate", TestMode):
            if str(message.author) in TopPermissionValues:
                rated = ParseForCmd("!rate", message.content)
                try:
                    data = await message.channel.send((await client.fetch_user(rated)).avatar_url)
                    for i in ReactionEmojis:
                        await data.add_reaction(i)
                except:
                    1

            return

        if IfCommand(message, "!profile", TestMode):
            user = ParseForCmd("!profile", message.content)

            returnMessage = message.content.split(" ")

            if DoesUserIDExist(message.author.id) is not False and user is not False:
                if len(returnMessage) >= 3 and str(message.author) in TopPermissionValues:
                    del returnMessage[0]
                    del returnMessage[0]
                    returnMessage = " ".join([str(i) for i in returnMessage])
                    if len(returnMessage) <= 280:
                        PointsSet(user, "PROFILE", returnMessage)
                        await message.channel.send(">>> <@!{UserID1}> Set the Profile of <@!{UserID2}> : `{ProfileData}`".format(UserID1=message.author.id, UserID2=user, ProfileData=ViewPoints(user)["PROFILE"]))
                    else:
                        await message.channel.send(f">>> <@!{user}> Profile too Long!")

                elif str(ViewPoints(user)["PROFILE"]) != "0":
                    await message.channel.send(">>> <@!{UserID}> : `{ProfileData}`".format(UserID=user, ProfileData=ViewPoints(user)["PROFILE"]))
                else:
                    await message.channel.send(f">>> <@!{user}> Doesn't have a Profile Setup Yet!")

            elif user == False or not returnMessage[1].startswith("<"):
                user = message.author.id
                if len(returnMessage) >= 2:
                    del returnMessage[0]
                    returnMessage = " ".join([str(i) for i in returnMessage])
                    if len(returnMessage) <= 280:
                        PointsSet(user, "PROFILE", returnMessage)
                        await message.channel.send(">>> <@!{UserID}> Set their Profile : `{ProfileData}`".format(UserID=message.author.id, ProfileData=ViewPoints(user)["PROFILE"]))
                    else:
                        await message.channel.send(f">>> <@!{user}> Profile too Long!" )

                elif "PROFILE" in str(ViewPoints(user)):
                    await message.channel.send(">>> <@!{UserID}> : `{ProfileData}`".format(UserID=user, ProfileData=ViewPoints(user)["PROFILE"]))

                else:
                    await message.channel.send(f">>> <@!{user}> You do not have a Profile Setup Setup Yet \n to Setup a Profile do !profile [info]")
            else:
                await message.channel.send(f">>> <@!{user}> Doesn't have a Profile Setup Yet!")

        if IfCommand(message, "!top", TestMode):
            Index = ParseForValue("!top", message.content)
            if Index is not False:
                Index = Index.upper()
                if Index in CommandList:
                    data = SortByIndex(Index)

                    OutMessage = ">>> "
                    
                    for i in range(3):

                        if i == 0:
                            OutMessage += "`1st"
                        elif i == 1:
                            OutMessage += "`2nd"
                        elif i == 2:
                            OutMessage += "`3rd"
                        user = str(await client.fetch_user(data[i][0])).split("#")[0]
                        OutMessage += f" : {user}` "

                        if len(data[i]) >= 3:
                            OutMessage += f"***AKA*** `{data[i][2]}` "

                        OutMessage += f"has {data[i][1]} {Index.upper()}\n"

                    await message.channel.send(f"{OutMessage}")

        rpgCMD = "+"
        if IfCommand(message, rpgCMD, False):
            # if the message starts with the command string, do things but first removes the 'rpgCMD' of the message
            if len(rpgCMD) < len(message.content):
                message.content = message.content[len(rpgCMD)::]

                if IfCommand(message, "inventory", False):
                    items = ViewItems(message.author.id)
                    if len(items) != 0:
                        LongestWord = 0
                        for i in items:
                            try:
                                if len(i[0]["name"]) + len(str(i[1])) > LongestWord:
                                    LongestWord = len(i[0]["name"]) + len(str(i[1]))
                            except:
                                # If this ever happens, there is probably an item that doesn't exist in the items.plk file
                                print(LongestWord, i)
                        # time.sleep(1)
                        OutMessage = f">>> <@!{message.author.id}>'s **Inventory**: \n```" + "\n\n".join("{}{} x{} : {}".format(" " * (LongestWord - len(i[0]["name"]) - len(str(i[1]))), i[0]["name"], i[1], i[0]["description"]) for i in items) + "```"

                    else:
                        OutMessage = f">>> <@!{message.author.id}> Doesn't have any Items"

                    await message.channel.send(OutMessage)

                # if IfCommand(message, "near", False):
                    # command to see some NPC's and things that are around the player

                if IfCommand(message, "help", False):
                    1
                    await message.channel.send(f">>> The New Commands are `{rpgCMD}inventory` and `{rpgCMD}shop`. To buy something from the shop just type `{rpgCMD}shop [item]`. ")

                area = "castle"
                if area == "castle":
                    
                    Stick = ImportItem("TEST_Stick")
                    Bomb = ImportItem("TEST_Bomb")
                    Arrow = ImportItem("TEST_Arrow")
                    ShopKeeper = shop("ShopKeeper - Zan", "WELCOME TRAVELER!")
                    ShopKeeper.AddCatalog([Stick, Bomb, Arrow])

                    sword = ImportItem("TEST_Wooden_Sword")
                    # OldMan = ItemGiver("OldMan", "It's Dangerous to go alone, take this!", sword)



                    place = [ShopKeeper]

                    for person in place:
                        if IfCommand(message, person.CallCommand, False):
                            OutMessage = person.OnContact(message)
                            if OutMessage is not None:
                                await message.channel.send(OutMessage)

        if str(message.author) in TopPermissionValues and not TestMode:
            # Admin
            # This checks if the person sending the message has permission for commands as well as if the message is a command
            CommandParse = ParseForNum(message.content.lower(), CommandList)

            if CommandParse is not False:
                (num, cmd, usr) = CommandParse
                
                if cmd == "COOKIE":
                    cmd = "COOKIES"
                
                del CommandParse

                if cmd == "NUTS" and int(num) > 0:
                    PointsAdd(usr, "TOTAL-NUTS", num)

                PointsAdd(usr, cmd, num)

                ListOfPoints = ViewPoints(usr)
                EndMessage = ReturnPointsString(usr, ListOfPoints)
                rank = f"**{cmd} RANK: #{RankPoints(usr, cmd)}**"
                # print(ListOfPoints)
                if EndMessage is not False and rank is not False:
                    print(EndMessage)
                    print(rank)
                await message.channel.send(f">>> {EndMessage}\n\n{rank}")
                if Channels["LogChannel"][0] is True:
                    await Channels["LogChannel"][1].channel.send(f">>> <@!{message.author.id}> Sent <@!{usr}> {num} {cmd}")

        if not TestMode:
            # This is to divide casino command from the rest of the commands

            # Casino Functions

            def listSum(lst):
                # Gets the sum of all the data in a list
                n = 0

                for i in lst:
                    n += i

                return n

            def drawCard(lst):
                lst.append(random.randint(2, 14))
                if lst[-1] > 11:
                    lst[-1] = 10

            if message.content.lower().startswith("!casino"):
                await message.channel.send(">>> The only game that is running at the moment is blackjack, to start type !BlackJack\nBlackJack costs 50 NUTS to Enter and if you Win you get 150 NUTS. ")

            if Channels["BlackJackTable"][0] and Channels["BlackJackTable"][1].channel.id == message.channel.id:

                if message.content.lower().startswith("!blackjack"):
                    if Channels["CasinoState"][0] is False and ViewPoints(message.author.id)["NUTS"] >= 50:
                        # Channels["CasinoState"] = <Isrunning> <Gametype> <Message Data> <Game State>
                        Channels["CasinoState"] = [True, "BlackJack", message, 0]
                        PointsAdd(message.author.id, "NUTS", -50)
                        if Channels["CasinoState"][3] == 0:
                            await message.channel.send(">>> ***BlackJack***")
                            time.sleep(1)
                            await message.channel.send(">>> The Dealer Draws Two Cards")
                            time.sleep(1)
                            CpuCards = []
                            drawCard(CpuCards)
                            if CpuCards[-1] == 11:
                                await message.channel.send(">>> One of the Cards is an Ace!")

                            else:
                                await message.channel.send(f">>> One of the Cards the Dealer Draws is a {CpuCards[-1]}")

                            time.sleep(1)
                            await message.channel.send(">>> ***Your Turn***")
                            time.sleep(1)
                            await message.channel.send(">>> You Draw Two Cards")
                            time.sleep(1)
                            UserCards = []
                            drawCard(UserCards)
                            drawCard(UserCards)
                            if UserCards[0] == 11:
                                OutMessage = "The First Card is an Ace!"
                            else:
                                OutMessage = f"The First Card is a {UserCards[0]}"
                            if UserCards[1] == 11:
                                OutMessage += " And the Second Card is an Ace!"
                            else:
                                OutMessage += f" And the Second Card is a {UserCards[1]}"
                            await message.channel.send(OutMessage)
                            time.sleep(1)
                            await message.channel.send(f">>> Your Score is {listSum(UserCards)}, Do you want to '!Hit' or '!Stand'")
                            Channels["CasinoState"][3] = 1

                if Channels["CasinoState"][0]:
                    if Channels["CasinoState"][1] == "BlackJack":
                        WinAmnt = 150
                        if message.channel == Channels["CasinoState"][2].channel and message.author.id == Channels["CasinoState"][2].author.id:
                            if Channels["CasinoState"][3] == 1:
                                if message.content.lower().startswith("!hit"):
                                    await message.channel.send(">>> You Hit!")
                                    time.sleep(1)
                                    drawCard(UserCards)
                                    if UserCards[-1] == 11:
                                        EndMessage = "You draw an Ace!"
                                    else:
                                        EndMessage = f"You draw a {UserCards[-1]}"
                                    await message.channel.send(EndMessage)
                                    if listSum(UserCards) > 21:
                                        if 11 not in UserCards:
                                            time.sleep(1)
                                            await message.channel.send(">>> You BUST!")
                                            Channels["CasinoState"] = [False]
                                        else:
                                            for i in range(listSum(UserCards)):
                                                if UserCards[i] == 11:
                                                    UserCards[i] -= 10
                                                    break
                                    if Channels["CasinoState"][0]:
                                        time.sleep(1)
                                        if listSum(UserCards) == 21:
                                            await message.channel.send(">>> Your Score is 21, You WIN!")
                                            Channels["CasinoState"] = [False]
                                            PointsAdd(message.author.id, "NUTS", WinAmnt)
                                            PointsAdd(message.author.id, "TOTAL-NUTS", WinAmnt)


                                        else:
                                            await message.channel.send(f">>> Your Score is {listSum(UserCards)}, Do you want to '!Hit' or '!Stand'")

                                if message.content.lower().startswith("!stand"):
                                    await message.channel.send(">>> You Stand!")
                                    time.sleep(1)
                                    await message.channel.send(">>> *** Dealers Turn ***")
                                    time.sleep(1)
                                    Channels["CasinoState"] = [False]
                                    while listSum(CpuCards) <= 16:
                                        drawCard(CpuCards)
                                        if CpuCards[-1] == 11:
                                            EndMessage = "The Dealer Draws an Ace!"
                                        else:
                                            EndMessage = f"The Dealer Draws a {CpuCards[-1]}"
                                        await message.channel.send(EndMessage)
                                        time.sleep(1)
                                        await message.channel.send(f">>> The Dealers Score is {listSum(CpuCards)}")
                                        while listSum(CpuCards) > 21 and 11 in CpuCards:
                                            for i in range(listSum(CpuCards)):
                                                if CpuCards[i] == 11:
                                                    CpuCards[i] -= 10
                                                    break
                                        time.sleep(1)

                                    time.sleep(1)
                                    if listSum(CpuCards) > 21:
                                        await message.channel.send(">>> The Dealer Busts! \n You Win!")
                                        PointsAdd(message.author.id, "NUTS", WinAmnt)
                                        PointsAdd(message.author.id, "TOTAL-NUTS", WinAmnt)

                                    else:
                                        await message.channel.send(">>> The Dealer Stands!")
                                        time.sleep(1)
                                        if listSum(CpuCards) > listSum(UserCards):
                                            await message.channel.send(">>> You Lose!")
                                        elif listSum(CpuCards) == listSum(UserCards):
                                            await message.channel.send(">>> You Tied!")
                                            PointsAdd(message.author.id, "NUTS", 50)
                                        elif listSum(CpuCards) < listSum(UserCards):
                                            await message.channel.send(">>> You Win!")
                                            PointsAdd(message.author.id, "NUTS", WinAmnt)
                                            PointsAdd(message.author.id, "TOTAL-NUTS", WinAmnt)




client.run(TOKEN)
