#!/usr/bin/env python3

# Ajusting Points

import json
from datetime import datetime
from operator import itemgetter

EmptyPoints = {'POG': 0, 'KEK': 0, 'SUS': 0, 'IQ': 0, 'COOKIES': 0, 'COOKIE-DATE': 0, 'NUTS': 0, 'TOTAL-NUTS': 0}
EmptyStats = {"HP": 0, "STRENGTH": 0, "INTELLIGENCE": 0}

# Writing to Files

def GetPoints():
	# Returns Points File
	
	QUERY()

	with open("points.plk", "r") as data:
		file = json.loads(data.read())
		data.close()

	return file

def WritePoints(file):
	# Writes file to points.plk

	QUERY()

	with open("points.plk", "w") as data:
		data.write(json.dumps(file))
		data.close()

	return True

def GetItems():
	# Returns Points File
	
	QUERY()

	with open("items.plk", "r") as data:
		file = json.loads(data.read())
		data.close()

	return file

def WriteItems(file):
	# Writes file to points.plk

	QUERY()

	with open("items.plk", "w") as data:
		data.write(json.dumps(file))
		data.close()

	return True

# Quality of File Check

def QUERY():

	# Makes sure that points.plk file exists and works properly
	try:
		with open("points.plk", "r") as file:
			json.loads(file.read())
			file.close()

	except:
		with open("points.plk", "w") as file:
			file.write("{}")
			file.close()

	# Makes sure that items.plk file exists and works properly
	try:
		with open("items.plk", "r") as file:
			json.loads(file.read())
			file.close()
		return

	except:
		with open("items.plk", "w") as file:
			file.write("{}")
			file.close()
		return

# Points Functions

def GetCookie(UserID):
	# Function to give a cookie to UserID
	global EmptyPoints

	data = GetPoints()

	UserID = str(UserID)

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


	WritePoints(data)

	return True

def PointsSet(UserID, key, change):
	# This is for directly overiding points to be set at something specific
	global EmptyPoints

	data = GetPoints()

	UserID = str(UserID)

	if UserID not in data:
		data[UserID] = EmptyPoints

	data[UserID][key] = change

	WritePoints(data)

	return True

def PointsAdd(UserID, key, Ammount):
	# Changes points of UserID by Amount in key
	global EmptyPoints

	data = GetPoints()

	UserID = str(UserID)

	if UserID not in data:
		data[UserID] = EmptyPoints

	if key in data[UserID]:
		data[UserID][key] += int(Ammount)

	else:
		data[UserID][key] = int(Ammount)

	WritePoints(data)

	return

def ViewPoints(UserID):
	# Querying Points of UserID
	global EmptyPoints

	data = GetPoints()

	UserID = str(UserID)

	if UserID not in data:
		return EmptyPoints

	else:
		return data[UserID]

def RankPoints(UserID, key):
	# Ranks UserID's points against everyone elses points to get rank
	global EmptyPoints

	data = GetPoints()

	UserID = str(UserID)
		
	rank = 1

	if UserID not in data:
		UserPoints = EmptyPoints[key]

	else:
		userPoints = data[UserID][key]

	for i in data:
		if data[i][key] > userPoints:
			rank += 1

	return rank

def SortByIndex(Index):

	data1 = GetPoints()

	data2 = []

	for UserID in data1:

		if "PROFILE" in data1[UserID]:
			data2.append([UserID, data1[UserID][Index], data1[UserID]["PROFILE"]])

		elif Index not in data1[UserID]:
			return False
		
		else:
			data2.append([UserID, data1[UserID][Index]])

	return sorted(data2, key = itemgetter(1))[::-1]

# Items With Points Functions

def BuyItem(UserID, ItemData):
	# This is for if someone buys an item from an item shop using RPG things
	global EmptyPoints

	data = GetPoints()

	UserID = str(UserID)

	if UserID not in data:
		data[UserID] = EmptyPoints

	if "RPG" not in data[UserID]:
		data[UserID]["RPG"] = {}

	if ItemData.ItemType not in data[UserID]["RPG"]:
		data[UserID]["RPG"][ItemData.ItemType] = {}

	UserData = data[UserID]

	if UserData["NUTS"] >= ItemData.price:

		data[UserID]["NUTS"] -= ItemData.price

		if ItemData.ItemKey in data[UserID]["RPG"][ItemData.ItemType]:
			data[UserID]["RPG"][ItemData.ItemType][ItemData.ItemKey] += 1

		else:
			data[UserID]["RPG"][ItemData.ItemType][ItemData.ItemKey] = 1

		WritePoints(data)

		return True

	return False

def ViewItems(UserID):
	# Returns all the items 'UserID' has

	data = GetPoints()

	UserID = str(UserID)

	if UserID in data and "RPG" in data[UserID] and "items" in data[UserID]["RPG"]:
		data = data[UserID]["RPG"]["items"]
		# Returns a list of ["Item Data", "Amount"]
		return [(GetItem(item, "items"), data[item]) for item in data]

	else:
		return []

# Items With Item File

def ReturnGeneralItem(item):

	ItemType = type(item)

	if ItemType == item:
		return GetItem(item)

	if ItemType == melee:
		return GetMelee(item)

	if ItemType == enemy:
		return GetEnemy(item)

	else:
		return False




class item:

	def __init__(self, name, price, ItemKey, description, ItemType="items"):
		self.name = name
		self.price = price
		self.ItemKey = ItemKey
		self.description = description
		self.ItemType = ItemType

def AddItem(ItemData):

	data = GetItems()

	if ItemData.ItemType not in data:
		data[ItemData.ItemType] = {}

	if ItemData.ItemKey in data[ItemData.ItemType]:
		return False

	data[ItemData.ItemType][ItemData.ItemKey] = {
		"name" : ItemData.name,
		"price" : ItemData.price,
		"description" : ItemData.description
	}

	WriteItems(data)

	return True

def GetItem(ItemKey, ItemType="items"):
	
	data = GetItems()

	if ItemKey in data[ItemType]:
		return item(data[ItemType][ItemKey]["name"], data[ItemType][ItemKey]["price"], ItemKey, data[ItemType][ItemKey]["description"], ItemType)

	else:
		return False

def PrintItems():

	data = GetItems()
	
	return print( "\n".join(f"{i}:" + "".join( "\n" + str(data[i][j]) for j in data[i] ) + "\n" for i in data) )

# Melee Items with Item File

class melee(item):

	def __init__(self, name, price, ItemKey, description, damage, CritPercent, ItemType="melee"):
		super().__init__(name, price, ItemKey, description, ItemType)
		self.damage = damage
		self.CritPercent = CritPercent

def AddMelee(MeleeData):

	data = GetItems()

	if MeleeData.ItemType not in data:
		data[MeleeData.ItemType] = {}

	if MeleeData.ItemKey in data[MeleeData.ItemType]:
		return False

	data[MeleeData.ItemType][MeleeData.ItemKey] = {
		"name" : MeleeData.name,
		"price" : MeleeData.price,
		"description" : MeleeData.description,
		"damage" : MeleeData.damage,
		"CritPercent" : MeleeData.CritPercent
	}

	WriteItems(data)

	return True

def GetMelee(MeleeKey, ItemType="melee"):
	
	data = GetItems()

	if MeleeKey in data[ItemType]:
		return melee(
			data[ItemType][MeleeKey]["name"],
			data[ItemType][MeleeKey]["price"], 
			MeleeKey,
			data[ItemType][MeleeKey]["description"],
			data[ItemType][MeleeKey]["damage"],
			data[ItemType][MeleeKey]["CritPercent"],
			ItemType
		)

	else:
		return False

def ViewMelee(UserID):
	# Returns all the items 'UserID' has

	data = GetPoints()

	UserID = str(UserID)

	if UserID in data and "RPG" in data[UserID] and "melee" in data[UserID]["RPG"]:
		data = data[UserID]["RPG"]["melee"]
		# Returns a list of ["Item Data", "Amount"]
		return [(GetMelee(item), data[item]) for item in data]

	else:
		return []

def GiveMelee(MeleeData, UserID):
	# Gives a player a melee weapon
	global EmptyPoints

	data = GetPoints()

	UserID = str(UserID)

	item = GetMelee(MeleeData.ItemKey)

	if UserID not in data:
		data[UserID] = EmptyPoints

	if "RPG" not in data[UserID]:
		data[UserID]["RPG"] = {}

	if MeleeData.ItemType not in data[UserID]["RPG"]:
		data[UserID]["RPG"][MeleeData.ItemType] = {}

	if MeleeData.ItemKey not in data[UserID]["RPG"][MeleeData.ItemType]:
		data[UserID]["RPG"][MeleeData.ItemType][MeleeData.ItemKey] = 1

	else:
		return False

	WritePoints(data)

	return True

# Enemy Data wuth Item File

class enemy:

	def __init__(self, name, health, xp, EnemyKey, description, WeaponKey, WeaponType="melee", WeaponDrop=False, ItemType="enemy"):
		self.name = name
		self.health = health
		self.xp = xp
		self.EnemyKey = EnemyKey
		self.description = description
		self.WeaponKey = WeaponKey
		self.WeaponType = WeaponType
		self.WeaponDrop = WeaponDrop
		self.ItemType = ItemType

def AddEnemy(EnemyData):

	data = GetItems()

	if EnemyData.ItemType not in data:
		data[EnemyData.ItemType] = {}

	if EnemyData.EnemyKey in data[EnemyData.ItemType]:
		return False

	data[EnemyData.ItemType][EnemyData.EnemyKey] = {
		"name" : EnemyData.name,
		"health" : EnemyData.health,
		"xp" : EnemyData.xp,
		"description" : EnemyData.description,
		"WeaponKey" : EnemyData.WeaponKey,
		"WeaponType" : EnemyData.WeaponType,
		"WeaponDrop" : EnemyData.WeaponDrop,
		"ItemType" : EnemyData.ItemType
	}

	WriteItems(data)

	return True

def GetEnemy(ItemKey, ItemType="enemy"):

	data = GetItems()

	if ItemKey in data[ItemType]:
		return enemy(
			data[ItemType][ItemKey]["name"],
			data[ItemType][ItemKey]["health"],
			data[ItemType][ItemKey]["xp"],
			ItemKey,
			data[ItemType][ItemKey]["description"],
			data[ItemType][ItemKey]["WeaponKey"],
			data[ItemType][ItemKey]["WeaponType"],
			data[ItemType][ItemKey]["WeaponDrop"]
		)

	else:
		return False

# Combat xp Functions

def GetCombatPoints(UserID, key, change):
	# Making Sure UserID is a string instead of the default integer
	global EmptyPoints
	global EmptyStats

	data = GetPoints()

	UserID = str(UserID)

	if UserID not in data:
		data[UserID] = EmptyPoints
	
	if "RPG" not in data[UserID]:
		data[UserID]["RPG"] = {}

	if "CombatStats" not in data[UserID]["RPG"]:
		data[UserID]["RPG"]["CombatStats"] = EmptyStats

	if key not in data[UserID]["RPG"]["CombatStats"]:
		data[UserID]["RPG"]["CombatStats"][key] = change

	else:
		data[UserID]["RPG"]["CombatStats"] += change

	WritePoints(data)

	return

def ViewCombatPoints(UserID):
	# returns a list of (StatKeys, AmountAtStatKeys)
	global EmptyStats

	data = GetPoints()

	UserID = str(UserID)

	if UserID in data and "RPG" in data[UserID] and "CombatStats" in data[UserID]["RPG"]:
		data = data[UserID]["RPG"]["CombatStats"]

	else:
		data = EmptyStats
	
	return [(item, data[item]) for item in data]

# Helpful Functions

def GetHP(level):
	1
	return 50 + level * 5

def GetCombatPointLevel(xp):
	1
	return int(0.1 * (int(xp) + 90) ** .5)

def GetCombatXp(level):
	1
	return (level) ** 2 - 90

# PrintItems()