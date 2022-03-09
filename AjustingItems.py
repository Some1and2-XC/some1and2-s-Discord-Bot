#!/usr/bin/env python3

# Ajusting Items

import json

def QUERY():
	# Makes sure that items.plk file exists and works properly
	try:
		
		with open("items.plk", "r") as file:
			if file.read() != "":
				return
			file.close()

		with open("items.plk", "w") as file:
			file.write("{}")
			file.close()
		return

	except:
		with open("items.plk", "w") as file:
			file.write("{}")
			file.close()
		return

def AddItem(ItemData):

	QUERY()

	with open("items.plk", "r") as file:
		data = json.loads(file.read())
		if ItemData.ItemKey in data:
			return
		file.close()

	with open("items.plk", "w") as file:
		data[ItemData.ItemKey] = {
			"name" : ItemData.name,
			"price" : ItemData.price,
			"description" : ItemData.description
		}
		file.write(json.dumps(data))
		file.close()

def GetItem(ItemKey):
	
	QUERY()

	with open("items.plk", "r") as file:
		data = json.loads(file.read())
		file.close()

	if ItemKey in data:
		return data[ItemKey]

	else:
		return False

def PrintItems():

	QUERY()

	with open("items.plk", "r") as file:
		data = json.loads(file.read())
		print("\n".join(f"{i} | {str(data[i])}" for i in data))

# PrintItems()