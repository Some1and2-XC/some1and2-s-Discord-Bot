#!/usr/bin/env python3

# File for NPC classes

from AjustingPoints import *
from DataParsing import *
from QualityOfLife import *

from time import sleep

from discord import Embed
from discord.ui import Button, View
from table2ascii import table2ascii as t2a, PresetStyle

# Menu Views

def GetMenuText(items, index):

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

class menu:
	def __init__(self, UserName, message, index=0):

		self.message = message

		self.CallCommand = "menu"

		# All the different menu items that can be scrolled through
		self.MenuItems = {
			"Melees": "melee",
			"Items": "items",
			"XP": "xp"
		}

		index = index % len(self.MenuItems)

		self.view = [
			MenuButton(label="◀", action="LEFT", UserName=UserName, message=message, MenuItems=self.MenuItems, index=index, style=1),
			MenuButton(label="SELECT", action="SELECT", UserName=UserName, message=message, MenuItems=self.MenuItems, index=index, style=3),
			MenuButton(label="▶", action="RIGHT", UserName=UserName, message=message, MenuItems=self.MenuItems, index=index, style=1),
			MenuButton(label="X", action="close", UserName=UserName, message=message, MenuItems=self.MenuItems, index=index, style=4)
		]

		self.title = GetMenuText(self.MenuItems, index)
		CombatLevel = ViewCombatPoints(message.author.id)
		for entry in range(len(CombatLevel)):
			if CombatLevel[entry][0].name == "OVERALL":
				CombatLevel = CombatLevel[entry][1]
				break

		self.content = "{UserName}'s Menu\n>>> *LVL {CombatLevel}\n{Cash} Cash*".format(UserName=UserName, CombatLevel=GetCombatPointLevel(CombatLevel), Cash=ViewCash(message.author.id))
		self.color = 0x403af0

	async def open(self, interaction=None):

		embed = Embed(
			title=self.title,
			description=self.content,
			color = self.color
		)

		view=View()

		for Item in self.view:
			view.add_item(Item)

		if interaction is None:
			return await self.message.channel.send(embed=embed, view=view)

		else:
			return await interaction.response.edit_message(embed=embed, view=view)

class MenuButton(Button):
	def __init__(self, label, action, UserName, message, MenuItems, index, style=None):
		super().__init__(label=label, style=style)
		self.action = action
		self.UserName = UserName
		self.message = message
		self.MenuItems = MenuItems
		self.index = index

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

# NPC Class (Is seperate from the other items.plk classes to avoid circular import from AjustingPoints.py)

class NPC:
	def __init__(self, name, dialog, PersonIndex, NPCType, ItemType="NPC", items=None):
		self.name = name
		self.dialog = dialog
		self.PersonIndex = PersonIndex
		self.NPCType = NPCType
		self.ItemType = ItemType
		self.items = items

def AddNPC(NPCData) -> bool:

	data = lindex(GetItems())

	# If this person does not exist, IndexCarve() will return False. If the person does exist, it will return its information
	if data.RTN(NPCData.ItemType, NPCData.NPCType, NPCData.PersonIndex) is not False:
		return False

	if NPCData.NPCType == "shop":

		DataToWrite = {
			"PersonIndex" : NPCData.PersonIndex,
			"name" : NPCData.name,
			"dialog" : NPCData.dialog,
			"items" : NPCData.items
		}

	if NPCData.NPCType == "text":

		DataToWrite = {
			"PersonIndex" : NPCData.PersonIndex,
			"name" : NPCData.name,
			"dialog" : NPCData.dialog,
		}

	data.set(NPCData.ItemType, NPCData.NPCType, NPCData.PersonIndex, DataToWrite)

	WriteItems(data)

	return True

def GetNPC(message, PersonIndex, NPCType, ItemType="NPC"):

	data = GetItems()

	if ItemType in data:
		if NPCType in data[ItemType]:
			if PersonIndex in data[ItemType][NPCType]:

				if NPCType == "shop":

					return ShopView(
						data[ItemType][NPCType][PersonIndex]["name"],
						data[ItemType][NPCType][PersonIndex]["dialog"],
						data[ItemType][NPCType][PersonIndex]["items"],
						message
					)

				if NPCType == "text":
					return TextNPCView(
						data[ItemType][NPCType][PersonIndex]["name"],
						data[ItemType][NPCType][PersonIndex]["dialog"],
						message
					)

	return False

def ReturnGeneralPerson(lst, message, UserName=None):
	
	if lst[0] == "enemy":

		return EnemyView(GetEnemy(lst[1]), UserName, message)

	if lst[0] == "NPC":

		return GetNPC(message, lst[2], lst[1])

	return False

# Shop NPC

def GetShopText(index, items, message):

	items = [ ReturnGeneralItem(item) for item in items ]

	TopText = f"Your Wallet: **{ViewCash(message.author.id)} CASH**"

	body = []
	for ShopItem in range(index, index + 3):
		ShopItem %= len(items)
		body.append([items[ShopItem].name, f"{items[ShopItem].price} Cash", items[ShopItem].description])
		if ShopItem == (index + 1) % len(items):
			body[-1][0] = f">{body[-1][0]}"

	output = t2a(
		header=["Item", "Price", "Description"],
		body=body,
		first_col_heading=True,
		style=PresetStyle.thin_rounded
	)
	return f"{TopText}\n```{output}```"

class ShopView:

	def __init__(self, name, dialog, items, message, index=0):

		self.message = message

		self.title = f"***{name} : {dialog}***"

		self.content = GetShopText(index, items, message)

		self.color = 0x00fffb

		self.CallCommand = "shop"
		self.view = [
			ShopButton(label="▲", items=items, name=name, dialog=dialog, direction=-1, message=message, style=1, index=index),
			ShopButton(label="BUY", items=items, name=name, dialog=dialog, direction=0, message=message, style=3, index=index),
			ShopButton(label="▼", items=items, name=name, dialog=dialog, direction=1, message=message, style=1, index=index),
			ShopButton(label="X", items=items, name=name, dialog=dialog, direction="close", message=message, style=4, index=index)
		]

		# Stuff for adding shop NPC to item file
		self.ItemType = "NPC"
		self.NPCType = "shop"
		self.items = items

	async def open(self, interaction=None, desc=""):

		embed = Embed(
			title=self.title,
			description=self.content + desc,
			color = self.color
		)

		view=View()

		for Item in self.view:
			view.add_item(Item)

		if interaction is None:
			return await self.message.channel.send(embed=embed, view=view)

		else:
			return await interaction.response.edit_message(embed=embed, view=view)

class ShopButton(Button):

	def __init__(self, label, items, name, dialog, direction, message, style=None, index=0):
		super().__init__(label=label, style=style)
		self.message = message
		self.items = items
		self.name = name
		self.dialog = dialog
		self.index = (index) % len(items)
		self.direction = direction

	async def callback(self, interaction):

		if self.direction == "close":
			await interaction.message.delete()
			try:
				await self.message.delete()
			except:
					print("Unable to Delete Message!\nMessage no longer Exists")
			return

		if interaction.user.id == self.message.author.id:

			if self.direction == 0:

				PurchaseText = self.Purchase(interaction, (self.items[(self.index + 1) % len(self.items)]))

				await ShopView(self.name, self.dialog, self.items, self.message, index=(self.index)).open(interaction, PurchaseText)

				return

			await ShopView(self.name, self.dialog, self.items, self.message, index=(self.index + self.direction)).open(interaction)

			return

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return

	def Purchase(self, interaction, item):

		item = ReturnGeneralItem(item)

		if BuyItem(self.message.author.id, item) is not False:
			return f"\n```You Have Sucessfully Purchased {item.name}!```"

		else:
			return "\n```Sorry, not enough NUTS```"

# Text NPC

def GetTextNPCText(TextItems):
	1
	return TextItems[0]

class TextNPCView:
	def __init__(self, name: str, dialog: list, message):

		self.message = message

		self.title = f"***{name}***"
		self.content = GetTextNPCText(dialog)
		self.color = 0xfbff00

		dialog = dialog[1::]

		self.CallCommand = name

		if len(dialog) != 1:
			self.view = [
				TextNPCScrollButton(label="NEXT", name=name, dialog=dialog, message=message, style=1)
			]

		else:
			self.view = [
				
			]

		# Stuff for adding shop NPC to item file
		self.ItemType = "NPC"
		self.NPCType = "text"

	async def open(self, interaction=None):

		embed = Embed(
			title=self.title,
			description=self.content,
			color = self.color
		)

		view=View()

		for Item in self.view:
			view.add_item(Item)

		if interaction is None:
			return await self.message.channel.send(embed=embed, view=view)

		else:
			return await interaction.response.edit_message(embed=embed, view=view)

class TextNPCScrollButton(Button):
	def __init__(self, label: str, name: str, dialog: list, message, style=None):
		super().__init__(label=label, style=style)
		self.name = name
		self.dialog = dialog
		self.message = message

	async def callback(self, interaction):
		if interaction.user.id == self.message.author.id:
			if len(self.dialog) > 0:
				await TextNPCView(self.name, self.dialog, self.message).open(interaction)

			else:
				await interaction.message.delete()
				try:
					await self.message.delete()
				except:
					print("Unable to Delete Message!\nMessage no longer Exists")
				return
				

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return

# Inventory Menu

def GetInventoryText(index, items, UserID, InventoryType=None):

	if len(items) == 0:
		items = [[item("None", "???", "None", "None", "None"), "???"]]

	body = []
	for InventoryItem in range(index, index + 3):

		if InventoryItem == index + 1:
			InventoryItem %= len(items)
			name = ">" + items[InventoryItem][0].name

		else:
			InventoryItem %= len(items)
			name = items[InventoryItem][0].name

		if InventoryType == "xp":
			body.append([name, f"{items[InventoryItem][1]}XP"])

		else:
			body.append([name, f"x{items[InventoryItem][1]}"])

	output = t2a(
		header=["Item", "Quantity"],
		body=body,
		first_col_heading=True,
		style=PresetStyle.thin_rounded
	)

	return f"```{output}```"

class InventoryView:

	def __init__(self, UserName, message, color=None, index=0, InventoryType=None):

		self.message = message

		if InventoryType is not None:
			if InventoryType == "items":
				items = ViewItems(message.author.id)

			elif InventoryType == "melee":
				items = ViewMelee(message.author.id)

			elif InventoryType == "xp":
				items = ViewCombatPoints(message.author.id)

			else:
				print(f"Something Bad, {InventoryType}doesn't exist! [Class InventoryView]")
				return

		else:
			items = [] # Lazy Coding at its finest

		self.view = [
			InventoryButton(label="▲", items=items, direction=-1, message=message, style=1, index=index, InventoryType=InventoryType, UserName=UserName),
			InventoryButton(label="UPDATE", items=items, direction=0, message=message, style=3, index=index, InventoryType=InventoryType, UserName=UserName),
			InventoryButton(label="▼", items=items, direction=1, message=message, style=1, index=index, InventoryType=InventoryType, UserName=UserName),
			InventoryButton(label="^", items=items, direction="close", message=message, style=4, index=index, InventoryType=InventoryType, UserName=UserName),
		]
		self.title = f"{UserName}'s ***Inventory:***"
		self.content = GetInventoryText(index, items, str(message.author.id), InventoryType)
		self.color = 0x8c3af0

	async def open(self, interaction=None):

		embed = Embed(
			title=self.title,
			description=self.content,
			color = self.color
		)

		view=View()

		for Item in self.view:
			view.add_item(Item)

		if interaction is None:
			return await self.message.channel.send(embed=embed, view=view)

		else:
			return await interaction.response.edit_message(embed=embed, view=view)

class InventoryButton(Button):

	def __init__(self, label, items, direction, message, style=None, index=0, InventoryType=None, UserName=None):
		super().__init__(label=label, style=style)
		self.message = message
		self.UserName = UserName
		self.items = items
		self.InventoryType = InventoryType
		if len(items) == 0:
			self.items = [[]]

		self.index = (index) % len(self.items)
		self.direction = direction

	async def callback(self, interaction):

		if interaction.user.id == self.message.author.id:

			if self.direction == "close":
				
				await menu(self.UserName, self.message).open(interaction)

				return

			await InventoryView(self.UserName, self.message, index=(self.index + self.direction), InventoryType=self.InventoryType).open(interaction)

			return

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return

# Battles

def GetEnemyText(enemy, UserName, PlayerHealth, UserID, index):

	hp = enemy.health
	
	lvl = enemy.level

	EnemyDamage = GetMelee(enemy.WeaponKey).damage

	TextHeader = f"> *{hp}HP\n> ~{EnemyDamage} Damage*\n\n**{UserName}**\n> {PlayerHealth}HP"


	header = ["Type", "Weapon Name", "Damage"]

	body = []

	UserWeapons = ViewMelee(UserID)

	for weapon in range(index, len(UserWeapons) + index):

		weapon %= len(UserWeapons)
		
		body.append([UserWeapons[weapon][0].ItemType, UserWeapons[weapon][0].name, UserWeapons[weapon][0].damage])

	output = t2a(
		header=header,
		body=body,
		first_col_heading=True,
		style=PresetStyle.thin_rounded
	)


	return f"{TextHeader}\n\n ***Weapon Menu:***\n```{output}```"

class EnemyView:

	def __init__(self, enemy, UserName, message, index=0, PlayerHealth=None):

		self.message = message

		if PlayerHealth is None:
			PlayerHealth = GetHP(ViewCombatPointDict(message.author.id)["HP"])

		self.CallCommand = "battle"

		self.title = f"***LEVEL {enemy.level} {enemy.name}***"
		self.content = GetEnemyText(enemy, UserName, PlayerHealth, str(message.author.id), index)
		self.color = 0xff0000

		self.view = [
			EnemyButton(label="▲", enemy=enemy, PlayerHealth=PlayerHealth, action="UP", UserName=UserName, message=message, index=index, style=1),
			EnemyButton(label="✦", enemy=enemy, PlayerHealth=PlayerHealth, action="DAMAGE", UserName=UserName, message=message, index=index, style=3),
			EnemyButton(label="▼", enemy=enemy, PlayerHealth=PlayerHealth, action="DOWN", UserName=UserName, message=message, index=index, style=1),
			EnemyButton(label="RUN", enemy=enemy, PlayerHealth=PlayerHealth, action="RUN", UserName=UserName, message=message, index=index)
		]


	def OnContact(self, message):
		1
		return self.content

	async def open(self, interaction=None, desc=""):

		embed = Embed(
			title=self.title,
			description=self.content + desc,
			color = self.color
		)

		view=View()

		for Item in self.view:
			view.add_item(Item)

		if interaction is None:
			return await self.message.channel.send(embed=embed, view=view)

		else:
			return await interaction.response.edit_message(embed=embed, view=view)

class EnemyButton(Button):

	def __init__(self, label, enemy, PlayerHealth, action, UserName, message, index, style=2):
		super().__init__(label=label, style=style)
		self.enemy = enemy
		self.PlayerHealth = PlayerHealth
		self.action = action
		self.UserName = UserName
		self.message = message
		self.index = index

	async def callback(self, interaction):

		if interaction.user.id == self.message.author.id and self.action is not None:
			DamageToEnemy = None
			if self.action == "DAMAGE":

				DamageToEnemy = GetFifteenPercent(ViewMelee(self.message.author.id)[self.index][0].damage)
				DamageToPlayer = GetFifteenPercent(ReturnGeneralItem(self.enemy.WeaponKey).damage)

				self.enemy.health -= DamageToEnemy
				self.PlayerHealth -= DamageToPlayer

				if self.enemy.health <= 0:

					items = []

					cash = self.enemy.cash

					if self.enemy.WeaponDrop:
						UserWeapons = [ item[0].ItemKey for item in ViewMelee(self.message.author.id) ]

						if self.enemy.WeaponKey not in UserWeapons:
							items.append(self.enemy.WeaponKey)

						else:
							cash += GetMelee(self.enemy.WeaponKey).price

					await ItemBoxView(items, self.enemy.xp, cash, self.message).open(interaction)

					return

				if self.PlayerHealth <= 0:
					await interaction.message.delete()
					try:
						await self.message.delete()
					except:
						print("Unable to Delete Message!\nMessage no longer Exists")

					await DeathScreen(self.enemy, self.message).open(interaction)

					return


			if self.action == "RUN":
				await interaction.message.delete()
				try:
					await self.message.delete()
				except:
					print("Unable to Delete Message!\nMessage no longer Exists")
				return
			
			if self.action == "UP":
				1
				self.index = (self.index - 1) % len(ViewMelee(self.message.author.id))

			if self.action == "DOWN":
				1
				self.index = (self.index + 1) % len(ViewMelee(self.message.author.id))

			EnemyViewClass = EnemyView(self.enemy, self.UserName, self.message, self.index, self.PlayerHealth)

			# This is an exception to the way that opening views using the .open() function to send views
			# This is just because it is easier to leave the code as is instead of reworking the .open() command for the Enemy Class
			if DamageToEnemy is not None:

				await EnemyViewClass.open(interaction, f"\n\n```yaml\nYou Dealt {DamageToEnemy} Damage\n\n{self.enemy.name} Dealt {DamageToPlayer} Damage```")

			else:
				await EnemyViewClass.open(interaction)

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return

# Item Boxes

def GetItemBoxText(items, xp=0, cash=0):

	# gets the name and description of each
	items = [ ReturnGeneralItem(item) for item in items ]
	items = [ [item.name, item.description] for item in items ]

	if xp != 0:
		items = [ ["XP", f"x{xp}"], *items]

	if cash != 0:
		items = [ ["Cash", f"x{cash}"], *items]


	output = t2a(
		header=["Item", "Details"],
		body=items,
		first_col_heading=True,
		style=PresetStyle.thin_rounded
	)
	return f"```{output}```"

class ItemBoxView:

	def __init__(self, items, xp = 0, cash = 0, message=None, text=None):

		self.message = message

		if text is None:
			text = "***ITEMBOX***"

		self.title = text
		self.content = ""
		self.color = 0x46eb34

		self.view = [
			ItemBoxButton(label="OPEN", items=items, xp=xp, cash=cash, action="OPEN", color=self.color, message=message, style=3)
		]

	async def open(self, interaction=None):

		embed = Embed(
			title=self.title,
			description=self.content,
			color = self.color
		)

		view=View()

		for Item in self.view:
			view.add_item(Item)

		if interaction is None:
			return await self.message.channel.send(embed=embed, view=view)

		else:
			return await interaction.response.edit_message(embed=embed, view=view)

class ItemBoxButton(Button):

	def __init__(self, label, items, xp, cash, action, color, message, style=1):
		super().__init__(label=label, style=style)
		self.items = items
		self.xp = xp
		self.cash = cash
		self.action = action
		self.color = color
		self.message = message

	async def callback(self, interaction):

		if self.action == "CLOSE":
			await interaction.message.delete()

			try:
				await self.message.delete()
			except:
				print("Unable to Delete Message!\nMessage no longer Exists")

		if interaction.user.id == self.message.author.id and self.action is not None:

			if self.action == "OPEN":

				if len(self.items) > 0:
					AddGeneralItem(self.message.author.id, ReturnGeneralItem(self.items[0]))
				
				GiveCash(self.message.author.id, self.cash)

				GiveCombatPoints(self.message.author.id, "OVERALL", self.xp)

				view=View()
				view.add_item(ItemBoxButton(label="X", items=None, xp=self.xp, cash=self.cash, action="CLOSE", color=self.color, message=self.message, style=4))

				embed = Embed(
					title = "***ITEM BOX***",
					description = GetItemBoxText(self.items, self.xp, self.cash),
					color=self.color
				)

				await interaction.response.edit_message(embed=embed, view=view)

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return

class GenericCloseButton(Button):
	def __init__(self, message=None, label="x", style=4):
		super().__init__(label=label, style=style)
		self.message = message

	async def callback(self, interaction):

		if interaction.user.id == self.message.author.id:

			await interaction.message.delete()
			if self.message is not None:
				try:
					await self.message.delete()
				except:
					print("Unable to Delete Message!\nMessage no longer Exists")
			return

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return

class DeathScreen:
	def __init__(self, enemy, message):

		self.message = message

		money = ViewCash(message.author.id)

		GiveCash(message.author.id, money * -1)

		self.title = "**YOU DIED**"
		self.content = f"> <@!{message.author.id}> was KILLED by **{enemy.name}** & lost **{money} CASH**"
		self.color = 0x000000

		self.view = [
			GenericCloseButton()
		]

	async def open(self, interaction=None):

		embed = Embed(
			title=self.title,
			description=self.content,
			color = self.color
		)

		view=View()

		for Item in self.view:
			view.add_item(Item)

		if interaction is None:
			return await self.message.channel.send(embed=embed, view=view)

		else:
			return await interaction.response.edit_message(embed=embed, view=view)
