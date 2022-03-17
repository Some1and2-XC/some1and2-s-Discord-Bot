#!/usr/bin/env python3

# File for NPC classes

from AjustingPoints import *
from DataParsing import *
from QualityOfLife import *

from time import sleep

from discord.ui import Button, View
from table2ascii import table2ascii as t2a, PresetStyle

# Shop NPC

def GetShopText(index, items, name, dialog):

	body = []
	for ShopItem in range(index, index + 3):
		ShopItem %= len(items)
		body.append([items[ShopItem].name, f"{items[ShopItem].price} NUTS", items[ShopItem].description])
		if ShopItem == (index + 1) % len(items):
			body[-1][0] = f">{body[-1][0]}"

	output = t2a(
		header=["Item", "Price", "Description"],
		body=body,
		first_col_heading=True,
		style=PresetStyle.thin_rounded
	)
	return f">>> ***{name} : {dialog}***\n```{output}```"

class ShopView:

	def __init__(self, name, dialog, items, message, index=0):

		self.CallCommand = "shop"
		self.buttonL = ShopButton(label="▲", items=items, name=name, dialog=dialog, direction=-1, message=message, style=1, index=index)
		self.Selection = ShopButton(label="BUY", items=items, name=name, dialog=dialog, direction=0, message=message, style=3, index=index)
		self.buttonR = ShopButton(label="▼", items=items, name=name, dialog=dialog, direction=1, message=message, style=1, index=index)
		self.CloseButton = ShopButton(label="X", items=items, name=name, dialog=dialog, direction="close", message=message, style=4, index=index)

		self.view = [self.buttonL, self.Selection, self.buttonR, self.CloseButton]
		self.content = GetShopText(index, items, name, dialog)

	def OnContact(self, message):
		1
		return self.content

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

				ShopViewClass = ShopView(self.name, self.dialog, self.items, self.message, index=(self.index))
				view=View()

				for Item in ShopViewClass.view:
					view.add_item(Item)

				await interaction.message.edit(content=ShopViewClass.content + self.Purchase(interaction, (self.items[(self.index + 1) % len(self.items)])), view=view)
				return

			ShopViewClass = ShopView(self.name, self.dialog, self.items, self.message, index=(self.index + self.direction))

			view=View()

			for Item in ShopViewClass.view:
				view.add_item(Item)

			await interaction.message.edit(content=ShopViewClass.content, view=view)

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return

	def Purchase(self, interaction, item):

		if BuyItem(self.message.author.id, item) is not False:
			return f"\n```You Have Sucessfully Purchased {item.name}!```"

		else:
			return "\n```Sorry, not enough NUTS```"

# Inventory Menu

def GetInventoryText(index, items, UserID):

	body = []
	for ShopItem in range(index, index + 3):

		if ShopItem == index + 1:
			ShopItem %= len(items)
			name = ">" + items[ShopItem][0].name

		else:
			ShopItem %= len(items)
			name = items[ShopItem][0].name


		body.append(["{} x{}".format(name, items[ShopItem][1]), items[ShopItem][0].description])

	output = t2a(
		header=["Item", "Description"],
		body=body,
		first_col_heading=True,
		style=PresetStyle.thin_rounded
	)
	return f">>> <@!{UserID}>'s ***Inventory:***\n```{output}```"

class InventoryView:

	def __init__(self, message, index=0):

		items = ViewItems(message.author.id)

		buttonL = InventoryButton(label="▲", items=items, direction=-1, message=message, style=1, index=index)
		UpdateButton = InventoryButton(label="UPDATE", items=items, direction=0, message=message, style=3, index=index)
		buttonR = InventoryButton(label="▼", items=items, direction=1, message=message, style=1, index=index)
		CloseButton = InventoryButton(label="X", items=items, direction="close", message=message, style=4, index=index)

		if len(items) == 0:
			[[item("None", 0, "None", "None", "None"), 0]]

		self.view = [buttonL, UpdateButton, buttonR, CloseButton]
		self.content = GetInventoryText(index, items, str(message.author.id))

	def OnContact(self, message):
		1
		return self.content

class InventoryButton(Button):

	def __init__(self, label, items, direction, message, style=None, index=0):
		super().__init__(label=label, style=style)
		self.message = message
		self.items = items
		if len(items) == 0:
			self.items = [[]]

		self.index = (index) % len(self.items)
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

			InventoryViewClass = InventoryView(self.message, index=(self.index + self.direction))

			view=View()

			for Item in InventoryViewClass.view:
				view.add_item(Item)

			await interaction.message.edit(content=InventoryViewClass.content, view=view)

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return

# Battles

def GetEnemyText(enemy, UserID):

	hp = enemy.health
	
	lvl = GetCombatPointLevel(enemy.xp)

	EnemyDamage = GetMelee(enemy.WeaponKey).damage

	TextHeader = f"> ***LEVEL {lvl} {enemy.name}***\n> *{hp}HP\n> ~{EnemyDamage} Damage*"


	header = ["Weapon Type", "Weapon Name", "Damage"]

	body = []
	for weapon in ViewMelee(UserID):
		body.append([weapon[0].ItemType, weapon[0].name, weapon[0].damage])

	output = t2a(
		header=header,
		body=body,
		first_col_heading=True,
		style=PresetStyle.thin_rounded
	)

	# Adds > at in the front of every line
	output = "\n> ".join( output.split("\n") )

	return f"{TextHeader}\n\n> ***Weapon Menu:***\n> ```{output}```"

class EnemyView:

	def __init__(self, enemy, message, hp = None):
		
		self.view = [
			EnemyButton(label="▲", enemy=enemy, action=None, message=message, style=1),
			EnemyButton(label="✦", enemy=enemy, action="DAMAGE", message=message, style=3),
			EnemyButton(label="▼", enemy=enemy, action=None, message=message, style=1),
			EnemyButton(label="✚", enemy=enemy, action="HEAL", message=message, style=4),
			EnemyButton(label="RUN", enemy=enemy, action="RUN", message=message)
		]
		self.content = GetEnemyText(enemy, str(message.author.id))

	def OnContact(self, message):
		1
		return self.content

class EnemyButton(Button):

	def __init__(self, label, enemy, action, message, style=2):
		super().__init__(label=label, style=style)
		self.enemy = enemy
		self.action = action
		self.message = message

	async def callback(self, interaction):

		if interaction.user.id == self.message.author.id and self.action is not None:
			DamageToEnemy = None
			if self.action == "DAMAGE":

				DamageToEnemy = GetFifteenPercent(ViewMelee(self.message.author.id)[0][0].damage)
				
				self.enemy.health -= DamageToEnemy
				
				if self.enemy.health <= 0:
					await interaction.message.delete()
					await self.message.delete()
					return

			if self.action == "RUN":
				await interaction.message.delete()
				try:
					await self.message.delete()
				except:
					print("Unable to Delete Message!\nMessage no longer Exists")
				return
			
			EnemyViewClass = EnemyView(self.enemy, self.message)

			view=View()

			for Item in EnemyViewClass.view:
				view.add_item(Item)

			if DamageToEnemy is not None:
				await interaction.message.edit(content=EnemyViewClass.content + f"\n\n> ```yaml\n> You Dealt {DamageToEnemy} Damage```", view=view)
				sleep(1)
				await interaction.message.edit(content=EnemyViewClass.content + f"\n\n> ```yaml\n> __INSERTBADGUYLATER__ Dealt {DamageToEnemy} Damage```", view=view)

			else:
				await interaction.message.edit(content=EnemyViewClass.content, view=view)

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return


def GetItemBoxText():
	1
	return ">>> ***FREE SHIT***"


class ItemBoxView:

	def __init__(self, items, text=None, message):
		
		if text is None:
			text = ">>> ***ITEMBOX***"

		self.view = [
			ItemBoxButton("OPEN", items, message, style=4)
		]
		self.content = text

	def OnContact(self, message):
		1
		return self.content

class ItemBoxButton(Button):

	def __init__(self, label, items, message, style=1):
		super().__init__(label=label, style=style)
		self.items = items
		self.message = message
		self.content = text

	async def callback(self, interaction):
		if interaction.user.id == self.message.author.id and self.action is not None:

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return




class msg:
	def __init__(self):
		self.author = author()

class author:
	def __init__(self):
		self.id = 123456789



# print(EnemyView(GetEnemy("TEST_Zombie"), msg()))