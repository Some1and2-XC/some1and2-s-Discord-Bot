#!/usr/bin/env python3

# Ajusting Points

import json
from datetime import datetime
from operator import itemgetter

from AjustingItems import *

def GetCookie(UserID):
	global EmptyPoints

	with open("points.plk", "r") as file:
		data = json.loads(file.read())
		file.close()

	if str(UserID) in data:
		if data[str(UserID)]["COOKIE-DATE"] == str(datetime.date(datetime.now())):
			return False 

	else:
		print("GetCookie")
		data[str(UserID)] = EmptyPoints

	data[str(UserID)]["COOKIES"] += 1
	data[str(UserID)]["COOKIE-DATE"] = str(datetime.date(datetime.now()))
	data[str(UserID)]["NUTS"] += 300
	data[str(UserID)]["TOTAL-NUTS"] += 300


	with open("points.plk", "w") as file:
		file.write(json.dumps(data))
		file.close()

	return

def PointsSet(UserID, key, change):
	global EmptyPoints
	# This is for directly overiding points to be set at something specific
	with open("points.plk", "r") as file:
		data = json.loads(file.read())
		if str(UserID) in data:
			data[str(UserID)][key] = change

		else:
			print("PointsSet")
			data[str(UserID)] = EmptyPoints
			data[str(UserID)][key] = change

		file.close()


	with open("points.plk", "w") as file:
		file.write(json.dumps(data))
		file.close()

	return

def PointsAdd(UserID, key, Ammount):
	global EmptyPoints
	# Changes points of UserID by Amount in key
	with open("points.plk", "r") as file:
		data = json.loads(file.read())

		if str(UserID) in data:
			if key in data[str(UserID)]:
				data[str(UserID)][key] += int(Ammount)

			else:
				data[str(UserID)][key] = int(Ammount)

		else:
			print("PointsAdd")
			data[str(UserID)] = EmptyPoints
			data[str(UserID)][key] += int(Ammount)
		file.close()

	with open("points.plk", "w") as file:
		file.write(json.dumps(data))
		file.close()

	return

def ViewPoints(UserID):
	# Querying Points of UserID

	global EmptyPoints
	with open("points.plk", "r") as file:
		data = json.loads(file.read())

		if str(UserID) in data:
			outData = data[str(UserID)]

		else:
			print("ViewPoints")
			data = EmptyPoints

		file.close()

	return outData

def RankPoints(UserID, key):
	# Ranks UserID's points against everyone elses points to get rank
	global EmptyPoints
	with open("points.plk", "r") as file:

		data = json.loads(file.read())
		
		rank = 1

		if str(UserID) in data and key in data[str(UserID)]:
			userPoints = data[str(UserID)][key]

		else:
			userPoints = EmptyPoints[key]

		for i in data:
			if data[i][key] > userPoints:
				rank += 1
		
		file.close()

	return rank

def SortByIndex(Index):
	with open("points.plk", "r") as file:
		data1 = json.loads(file.read())
		file.close()

	data2 = []
	for UserID in data1:

		if Index in data1[str(UserID)] and "PROFILE" in data1[str(UserID)]:
			data2.append([UserID, data1[str(UserID)][Index], data1[str(UserID)]["PROFILE"]])

		else:
			data2.append([UserID, data1[str(UserID)][Index]])

	return sorted(data2, key = itemgetter(1))[::-1]

def BuyItem(UserID, ItemData):
	global EmptyPoints
	EmptyPoints = {'POG': 0, 'KEK': 0, 'SUS': 0, 'IQ': 0, 'COOKIES': 0, 'COOKIE-DATE': 0, 'NUTS': 0, 'TOTAL-NUTS': 0, 'RPG':{}}

	# This is for if someone buys an item from an item shop using RPG things
	with open("points.plk", "r") as file:
		data = json.loads(file.read())
		if str(UserID) in data:
			if "RPG" not in data[str(UserID)]:
				data[str(UserID)]["RPG"] = {}
				if ItemData.ItemType not in data[str(UserID)]["RPG"]:
					data[str(UserID)]["RPG"][ItemData.ItemType] = {}

		else:
			print("BuyItem")
			data[str(UserID)] = EmptyPoints

		file.close()

	UserData = data[str(UserID)]

	if UserData["NUTS"] >= ItemData.price:

		data[str(UserID)]["NUTS"] -= ItemData.price

		if ItemData.ItemType not in data[str(UserID)]["RPG"]:
			data[str(UserID)]["RPG"][ItemData.ItemType] = {}

		if ItemData.ItemKey in data[str(UserID)]["RPG"]:
			data[str(UserID)]["RPG"][ItemData.ItemType][ItemData.ItemKey] += 1

		else:
			data[str(UserID)]["RPG"][ItemData.ItemType][ItemData.ItemKey] = 1

		with open("points.plk", "w") as file:
			file.write(json.dumps(data))
			file.close()
		return True
	else:

		with open("points.plk", "w") as file:
			file.write(json.dumps(data))
			file.close()
		return False

def FreeItem(UserID, ItemData):
	global EmptyPoints
	EmptyPoints = {'POG': 0, 'KEK': 0, 'SUS': 0, 'IQ': 0, 'COOKIES': 0, 'COOKIE-DATE': 0, 'NUTS': 0, 'TOTAL-NUTS': 0, 'RPG':{"items":{}}}

	# This is for if someone buys an item from an item shop using RPG things
	with open("points.plk", "r") as file:
		data = json.loads(file.read())
		if str(UserID) in data:
			if "RPG" not in data[str(UserID)]:
				data[str(UserID)]["RPG"] = {}

		else:
			print("GetItem")
			data[str(UserID)] = EmptyPoints

		file.close()

	UserData = data[str(UserID)]
	
	if ItemData.ItemType in data[str(UserID)]["RPG"]:
		data[str(UserID)]["RPG"][ItemData.ItemType] = {}

	if ItemData.ItemKey not in data[str(UserID)]["RPG"][ItemData.ItemType]:
		data[str(UserID)]["RPG"]["items"][ItemData.ItemKey][ItemData.ItemKey] = 1

	else:
		return False

	with open("points.plk", "w") as file:
		file.write(json.dumps(data))
		file.close()

	return True

def ViewItems(UserID):
	UserID = str(UserID)
	with open("points.plk", "r") as file:
		data = json.loads(file.read())
		file.close()

	if UserID in data and "RPG" in data[UserID] and "items" in data[UserID]["RPG"]:
		data = data[UserID]["RPG"]["items"]
		return [(GetItem(item), data[item]) for item in data]
	else:
		return []