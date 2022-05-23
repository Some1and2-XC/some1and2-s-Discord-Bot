#!/usr/bin/env python3

import os

# Pip Commands

import discord
from dotenv import load_dotenv

from DataInteractions import *
from screens import *

intents = discord.Intents.none()
intents.messages = True
intents.message_content = True
intents.reactions = True

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

TestMode = False

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

def IfCommand(MessageData, command: str, TestMode: bool) -> bool:
	if MessageData.content.lower().startswith(command.lower()) and not TestMode:
		return True
	else:
		return False

def RemoveToFirstSpace(txt: str) -> str:
	txt = " ".join(i for i in txt.split(" ")[1::])
	return txt

@client.event
async def on_message(message):
	if message.author != client.user:

		if IfCommand(message, "+add_weapon", TestMode):

			index = "weapon"

			message.content = RemoveToFirstSpace(message.content)
			if len(message.content) == 0:
				# This is where the help menu for each addition could be

				dialog = [
					"The Information Required for a Weapon is the following: ",
					"Item Name | Just the name of the item",
					"Item Description | A breif description of the item for tooltips",
					"Approximate Damage | doesn't really matter too much the specific, for reference a hand does 5 damage",
					"Approximate Cost of the weapon | specifics again don't matter",
					"The name the Computer Calls the item [this again doesn't matter too much, a good example of this however could be `bronze_sword_1`]",
					"To add a weapon, the format should be `+add_weapon name = #, price = #, ComputerName = #, description = #, damage = #`",
					'an example of this format being used to make the `hand` weapon would be `+add_weapon name = "Hands", price = 500, ComputerName = "TEST_hand", description = "Just your Hand?", damage = 5`',
				]

				HelpScreen = TextNPCView("**Adding Weapons**", dialog, message)

				OutView = HelpScreen.view
				view = View()

				for Item in OutView:
					view.add_item(Item)

				embed = discord.Embed(
					title = HelpScreen.title,
					description = HelpScreen.content,
					color = HelpScreen.color
				)

				await message.channel.send(embed=embed, view=view)

			else:
				AddIndex(str(await client.fetch_user(message.author.id)), index, message.content)

				dialog = ["Thank You For the Contribution!"]

				HelpScreen = TextNPCView(f"**{index}**", dialog, message)

				OutView = HelpScreen.view
				view = View()

				for Item in OutView:
					view.add_item(Item)

				embed = discord.Embed(
					title = HelpScreen.title,
					description = HelpScreen.content,
					color = HelpScreen.color
				)

				await message.channel.send(embed=embed, view=view)

		if IfCommand(message, "+add_enemy", TestMode):

			index = "enemy"

			message.content = RemoveToFirstSpace(message.content)
			if len(message.content) == 0:
				# This is where the help menu for each addition could be

				dialog = [
					"The Information Required for an Enemy is the following: ",
					"Enemy Name | Just the name of the enemy",
					"Enemy Description | A breif description of the enemy for tooltips",
					"The name the Computer Calls the enemy [this again doesn't matter too much, a good example of this however could be `zombie_enemy_1`]",
					"Weapon name | The name of the weapon carried by the enemy",
					"To add a enemy, the format should be `+add_enemy name = #, description = #, ComputerName = #, WeaponName = #`",
					'an example of this format being used to make the `Zombie` enemy would be `+add_enemy name = "Zombie", description = "He is a zombie :l", ComputerName = "TEST_Zombie", WeaponKey = "TEST_bronze_sword"`',
				]

				HelpScreen = TextNPCView("**Adding Enemy**", dialog, message)

				OutView = HelpScreen.view
				view = View()

				for Item in OutView:
					view.add_item(Item)

				embed = discord.Embed(
					title = HelpScreen.title,
					description = HelpScreen.content,
					color = HelpScreen.color
				)

				await message.channel.send(embed=embed, view=view)

			else:
				AddIndex(str(await client.fetch_user(message.author.id)), index, message.content)

				dialog = ["Thank You For the Contribution!"]

				HelpScreen = TextNPCView(f"**{index}**", dialog, message)

				OutView = HelpScreen.view
				view = View()

				for Item in OutView:
					view.add_item(Item)

				embed = discord.Embed(
					title = HelpScreen.title,
					description = HelpScreen.content,
					color = HelpScreen.color
				)

				await message.channel.send(embed=embed, view=view)
		# v Working on this right now, as it is, this has just been copy and pasted from `+add_enemy`
		if IfCommand(message, "+add_NPC", TestMode):

			index = "NPC"

			message.content = RemoveToFirstSpace(message.content)
			if len(message.content) == 0:
				# This is where the help menu for each addition could be

				dialog = [
					"The Information Required for an Enemy is the following: ",
					"Enemy Name | Just the name of the enemy",
					"Enemy Description | A breif description of the enemy for tooltips",
					"The name the Computer Calls the enemy [this again doesn't matter too much, a good example of this however could be `zombie_enemy_1`]",
					"Weapon name | The name of the weapon carried by the enemy",
					"To add a enemy, the format should be `+add_enemy name = #, description = #, ComputerName = #, WeaponName = #`",
					'an example of this format being used to make the `Zombie` enemy would be `+add_enemy name = "Zombie", description = "He is a zombie :l", ComputerName = "TEST_Zombie", WeaponKey = "TEST_bronze_sword"`',
				]

				HelpScreen = TextNPCView("**Adding Enemy**", dialog, message)

				OutView = HelpScreen.view
				view = View()

				for Item in OutView:
					view.add_item(Item)

				embed = discord.Embed(
					title = HelpScreen.title,
					description = HelpScreen.content,
					color = HelpScreen.color
				)

				await message.channel.send(embed=embed, view=view)

			else:
				AddIndex(str(await client.fetch_user(message.author.id)), index, message.content)

				dialog = ["Thank You For the Contribution!"]

				HelpScreen = TextNPCView(f"**{index}**", dialog, message)

				OutView = HelpScreen.view
				view = View()

				for Item in OutView:
					view.add_item(Item)

				embed = discord.Embed(
					title = HelpScreen.title,
					description = HelpScreen.content,
					color = HelpScreen.color
				)

				await message.channel.send(embed=embed, view=view)

		if IfCommand(message, "+add_item", TestMode):

			index = "item"

			message.content = RemoveToFirstSpace(message.content)
			if len(message.content) == 0:
				# This is where the help menu for each addition could be
				pass
			else:
				print(message.content)

		if IfCommand(message, "+add_custom", TestMode):

			index = "custom"

			message.content = RemoveToFirstSpace(message.content)
			if len(message.content) == 0:
				# This is where the help menu for each addition could be
				pass
			else:
				print(message.content)

		if IfCommand(message, "+help", TestMode):

			dialog = [
				"This bot is for letting people from the Discord Server decide and contribute to the ongoing discord Universe / `RPG` project",
				"You can now get involved with the future of the `RPG` project by contributing `NPC`'s, `enemies` and `weapons` to the game",
				"What is needed is simple information about whatever game data you are going to contribute. ",
				"For More information about any particular type of contribution, reference its command",
				"`+add_weapon` : For adding weapon data\n`+add_enemy` : For adding enemy data\n`+add_NPC` : For adding NPC data\n`+add_custom` : For adding custom data\n`+add_item` : For adding item data",
				"Don't forget that any information submitted can be altered and fixed to fix any issues that arise in the future, submissions would be greatly appreciated"
			]

			HelpScreen = TextNPCView("**Module Information**", dialog, message)

			OutView = HelpScreen.view
			view = View()

			for Item in OutView:
				view.add_item(Item)

			embed = discord.Embed(
				title = HelpScreen.title,
				description = HelpScreen.content,
				color = HelpScreen.color
			)

			await message.channel.send(embed=embed, view=view)

client.run(TOKEN)
