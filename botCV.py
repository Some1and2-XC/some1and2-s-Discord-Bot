#!/usr/bin/env python3

# Storyboard story for the story of the game
# Also draft how the menus are going to look like

#botCV.py

# Builtins

import os
import time
import random

# Pip Commands

import discord
from dotenv import load_dotenv

# Made Commands

from DataParsing import *
from AjustingPoints import *
from QualityOfLife import *
from NPC import *

intents = discord.Intents.none()
intents.messages = True
intents.message_content = True
intents.reactions = True

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

TestMode = False

Channels = {"LogChannel" : [False]}

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

# Should remove this Probably
@client.event
async def on_raw_reaction_add(payload):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message.author == client.user:
        for i in message.reactions:
            if payload.member in await i.users().flatten() and not payload.member.bot and str(i) != str(payload.emoji):
                await message.remove_reaction(i.emoji, payload.member)

@client.event
async def on_message(message):
    if message.author != client.user:
        global Channels
        TopPermissionValues = ["Some1and2#2570", "zanekyber#9825", "Spike#6128", "Bardock#4474"]
        CommandList = ["POG", "KEK", "SUS", "IQ", "COOKIES", "COOKIE", "NUT", "NUTS", "TOTAL-NUTS"]

        if IfCommand(message, "pspspsps", TestMode) and str(message.author) in TopPermissionValues:
            with open("points.plk", "rb") as file:
                await message.author.send("Here are the points: ", file=discord.File(file, "points.plk"))
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

                ReactionEmojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

                if rated is not False:
                    data = await message.channel.send((await client.fetch_user(rated)).avatar.url)
                    for i in ReactionEmojis:
                        await data.add_reaction(i)
                else:
                    data = await message.channel.send((await client.fetch_user(message.author.id)).avatar.url)
                    for i in ReactionEmojis:
                        await data.add_reaction(i)

            return

        if IfCommand(message, "!profile", TestMode):
            user = ParseForCmd("!profile", message.content)

            returnMessage = message.content.split(" ")

            if DoesUserIDExist(message.author.id) is not False and user is not False:
                if len(returnMessage) >= 3 and str(message.author) in TopPermissionValues:
                    del returnMessage[0]
                    del returnMessage[0]
                    returnMessage = " ".join( str(i) for i in returnMessage )
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

                    if len(data) >= 3:

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

        if IfCommand(message, "+bbbbb", TestMode):
            bossguy = EnemyView(GetEnemy("TEST_BAD"), await client.fetch_user(message.author.id), message)

            if OutMessage is not None:
                OutView = bossguy.view
                view = View()

                for Item in OutView:
                    view.add_item(Item)

                embed = discord.Embed(
                    title = bossguy.title,
                    description = bossguy.content,
                    color = bossguy.color
                )

                await message.channel.send(embed=embed, view=view)

        rpgCMD = "+"
        if IfCommand(message, rpgCMD, TestMode):
            # if the message starts with the command string, do things but first removes the 'rpgCMD' of the message
            if len(rpgCMD) < len(message.content):
                message.content = message.content[len(rpgCMD)::]

                if IfCommand(message, "test", False):
                    1
                    pass

                if IfCommand(message, "help", False):
                    embed = discord.Embed(
                        title = "**+help**",
                        description = "`+near` to see things to do ***near*** you\n`+menu` will open your ***inventory***"
                    )

                    view = View()

                    view.add_item(GenericCloseButton(message=message))

                    await message.channel.send(embed=embed, view=view)

                if IfCommand(message, "menu", False):

                    await menu(await client.fetch_user(message.author.id), message).open()

                    return

                area = MapView(message.author.id)

                # makes the `UserName` variable to the message authors username to only have one API call
                UserName = await client.fetch_user(message.author.id)

                place = [ ReturnGeneralPerson(person, message, UserName) for person in area ]

                del UserName, area

                if IfCommand(message, "near", TestMode):
                    embed = discord.Embed(
                        title = "Some things to do **Near** you!:",
                        description = " | ".join( f"**+{str(person.CallCommand)}**" for person in place )
                    )

                    view = View()

                    view.add_item(GenericCloseButton(message=message))

                    await message.channel.send(embed=embed, view=view)
                    return

                for person in place:
                    if IfCommand(message, person.CallCommand, False):

                        await person.open()

                        return

        if str(message.author) in TopPermissionValues and not TestMode:
            # Sudo commands
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

client.run(TOKEN)
