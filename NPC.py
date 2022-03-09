#!/usr/bin/env python3

# File for NPC classes

from AjustingItems import *
from AjustingPoints import *
from DataParsing import *

def ImportItem(ItemKey):
	ItemData = GetItem(ItemKey)
	return item(ItemData["name"], ItemData["price"], ItemKey, ItemData["description"], ItemData["ItemType"])

class NPC:
	def __init__(self, name, dialog, CallCommand):
		self.name = name
		self.dialog = dialog
		self.CallCommand = CallCommand

	def OnContact(self, message):
		message.channel.send("I Have Nothing to Say")

# Shop NPC
class shop(NPC):

	def __init__(self, name, dialog):
		super().__init__(name, dialog, "shop")
		self.catalog = []

	def AddCatalog(self, catalog):
		for ShopItem in catalog:
			AddItem(ShopItem)
		self.catalog = catalog

	def OnContact(self, message):

		MessageHeader = f">>> ***{self.name}: ***\n"

		selection = ParseForShopItem(self.CallCommand, message.content)

		found = False

		for ShopItem in self.catalog:
			
			if selection is False:
				break

			if ShopItem.name.lower() == selection.lower():
				if BuyItem(message.author.id, ShopItem) is not False:
					return f"{MessageHeader}```You Have Sucessfully Purchased {ShopItem.name}!```"

				else:
					return f"{MessageHeader}```Sorry, not enough NUTS```"

				found = True

				break

		if not found:

			return f">>> ***{self.name}: {self.dialog}***\n```" + " | ".join(f"{ShopItem.name} : {ShopItem.price} NUTS" for ShopItem in self.catalog) + "```"

		del found

		return

# NPC that gives free stuff
class ItemGiver(NPC):

	def __init__(self, name, dialog, item):
		super().__init__(name, dialog, name)
		self.item = item

	def OnContact(self, message):

		if FreeItem(message.author.id, self.item):
			return f">>> ***{self.name}: *** **{self.dialog}** \n```You Have Sucessfully Recived {self.item.name}!```"

		else:
			return f">>> ***{self.name}: *** \n```You Already Recived {self.item.name}!```"

class item:

	def __init__(self, name, price, ItemKey, description, ItemType):
		self.name = name
		self.price = price
		self.ItemKey = ItemKey
		self.description = description
		self.ItemType = ItemType

