#!/usr/bin/env python3

# For this file, anytime `def tf(args):` is used, tf is a temporary function, it should be deleted soon after its declared

from discord import Embed
from discord.ui import Button, View
from table2ascii import table2ascii as t2a, PresetStyle

# NPC Super Class
class NPC:
	def __init__(self, CallCommand, TxtFunc, Button):

		self.CallCommand = CallCommand
		self.TxtFunc = TxtFunc
		self.Button = Button

		self.view = False
		self.title = False
		self.content = False
		self.color = False

	async def open(self, interaction = None, desc=""):

		# Raises Error is `self.test()` returns `False`
		assert self.test()

		embed = Embed(
			title=self.title,
			description=self.content + desc,
			color = self.color
		)

		view=View()

		for Item in self.view:
			view.add_item(Item)

		if interaction is None:
			await self.message.channel.send(embed=embed, view=view)
			return

		else:
			await interaction.response.edit_message(embed=embed, view=view)
			return

	# Function for testing wether a subclass is setup correctly
	def test(self):

		TestDict = {
			"view" : self.view,
			"title" : self.title,
			"content" : self.content,
			"color" : self.color
		}

		for i in TestDict:
			if TestDict[i] is False:
				print(f"Test: Error: {i} is not Set | NPC: {self.CallCommand}")
				return False

		return True

# NPC Button Super Class
class SubBtn(Button):
	def __init__(self, parent: NPC, InteractionFunc, label, style = None):
		super().__init__(label=label, style=style)

		self.parent = parent
		self.InteractionFunc = InteractionFunc

	async def callback(self, interaction):
		if interaction.user.id == self.parent.message.author.id:

			desc = self.InteractionFunc(parent) -> str # Returns Optional Description (if needed)

			if type(desc) is not str:
				desc = ""

			parent.open(interaction = interaction, desc = desc)

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return

# Menu Views

def tf(items, index):

	ItemIndex = [ item for item in items ]

	separator = " | "

	output = ""

	body = []
	for selection in range(index, index + 3):

		output += separator

		if selection == index + 1:
			output += "__***"

		output += ItemIndex[selection % len(items)]

		if selection == index + 1:
			output += "***__"

	return f"{output[len(separator)::]}"

class menu(NPC):
	def __init__(self, UserName, message, index=0):

		def tf(items, index):

			ItemIndex = [ item for item in items ]

			separator = " | "

			output = ""

			body = []
			for selection in range(index, index + 3):

				output += separator

				if selection == index + 1:
					output += "__***"

				output += ItemIndex[selection % len(items)]

				if selection == index + 1:
					output += "***__"

			return f"{output[len(separator)::]}"

		super.__init__(CallCommand = "menu", TxtFunc = tf, Button = MenuButton)

		del tf

		self.message = message

		# All the different menu items that can be scrolled through, the keys in MenuItems is their pretty name, Menuitems[key] is the index
		self.MenuItems = {
			"Melees": "melee",
			"Items": "items",
			"XP": "xp"
		}

		self.index = index % len(self.MenuItems)



		self.view = [
			self.Button(parent = self,    label="◀", action="LEFT", MenuItems=self.MenuItems, style=1),
			self.Button(parent = self,    label="SELECT", action="SELECT", MenuItems=self.MenuItems, style=3),
			self.Button(parent = self,    label="▶", action="RIGHT", MenuItems=self.MenuItems, style=1),
			self.Button(parent = self,    label="X", action="close", MenuItems=self.MenuItems, style=4)
		]

		del tf

		self.title = GetMenuText(self.MenuItems, index)

		CombatLevel = ViewCombatPoints(message.author.id)

		# Finds the users `overall` combat level
		for entry in range(len(CombatLevel)):
			if CombatLevel[entry][0].name == "OVERALL":
				CombatLevel = CombatLevel[entry][1]
				break

		self.content = "{UserName}'s Menu\n>>> *LVL {CombatLevel}\n{Cash} Cash*".format(UserName=UserName, CombatLevel=GetCombatPointLevel(CombatLevel), Cash=ViewCash(message.author.id))
		self.color = 0x403af0

class MenuButton(SubBtn):
	def __init__(self, action, MenuItems, label, style=None):

		# def tf():DEFINE WHAT EACH BUTTON DOES HERE

		super().__init__(parent = parent, InteractionFunc = tf, label=label, style=style)

		del tf

		self.action = action
		self.MenuItems = MenuItems

	async def callback(self, interaction):

		if interaction.user.id == self.message.author.id:

			if self.action == "close":
				await interaction.message.delete()

				try:
					await self.message.delete()

				except:
						print("Unable to Delete Message!\nMessage no longer Exists")

				return


			if self.action == "LEFT":
				1
				self.index = self.index - 1

			if self.action == "RIGHT":
				1
				self.index = self.index + 1

			if self.action == "SELECT":

				self.MenuItems = [ self.MenuItems[item] for item in self.MenuItems ]

				self.SentMessage = await InventoryView(self.UserName, self.message, self.index, InventoryType=self.MenuItems[(self.index + 1) % len(self.MenuItems)]).open(interaction)

				return

			await menu(self.UserName, self.message, self.index).open(interaction)

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return