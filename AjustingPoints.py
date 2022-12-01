#!/usr/bin/env python3

# Ajusting Points

import json
from datetime import datetime
from operator import itemgetter

from QualityOfLife import *

from lindex import lindex

EmptyPoints = {'POG': 0, 'KEK': 0, 'SUS': 0, 'IQ': 0, 'COOKIES': 0, 'COOKIE-DATE': 0, 'NUTS': 0, 'TOTAL-NUTS': 0}
EmptyStats = {"OVERALL": 0, "HP": 0, "STRENGTH": 0, "INTELLIGENCE": 0}
EmptyMap = ["lucia", "palmer", "Neville"]

# Directly Changing Files Functions
if True:

	# Quality of File Check
	def QUERY() -> bool:

		FILEISBROKENSTRING = "{}"

		# Makes sure that points.plk file exists and works properly
		try:
			with open("points.plk", "r") as file:
				json.loads(file.read())
				file.close()

		except:
			with open("points.plk", "w") as file:
				file.write(FILEISBROKENSTRING)
				file.close()

		# Makes sure that items.plk file exists and works properly
		try:
			with open("items.plk", "r") as file:
				json.loads(file.read())
				file.close()

		except:
			with open("items.plk", "w") as file:
				file.write(FILEISBROKENSTRING)
				file.close()

		# Makes sure that map.plk file exists and works properly
		try:
			with open("map.plk", "r") as file:
				json.loads(file.read())
				file.close()

		except:
			with open("map.plk", "w") as file:
				file.write(FILEISBROKENSTRING)
				file.close()

		return True

	# Returns Points File
	def GetPoints() -> dict:
		
		QUERY()

		with open("points.plk", "r") as data:
			file = json.loads(data.read())
			data.close()

		return file

	# Writes file to points.plk
	def WritePoints(file: dict) -> bool:

		QUERY()

		with open("points.plk", "w") as data:
			data.write(json.dumps(file))
			data.close()

		return True

	# Returns items.plk File
	def GetItems() -> dict:
		
		QUERY()

		with open("items.plk", "r") as data:
			file = json.loads(data.read())
			data.close()

		return file

	# Writes file to points.plk
	def WriteItems(file: dict) -> bool:

		QUERY()

		with open("items.plk", "w") as data:
			data.write(json.dumps(file))
			data.close()

		return True

	# Returns map.plk File
	def GetMap():
		
		QUERY()

		with open("map.plk", "r") as data:
			file = json.loads(data.read())
			data.close()

		return file

# Points Functions
if True:

	# Function to give a cookie to `UserID`
	def GetCookie(UserID: int) -> bool:
		global EmptyPoints

		data = lindex(GetPoints())

		UserID = str(UserID)

		if UserID in data and "POG" in data[UserID]:
			if data.RTN(UserID, "COOKIE-DATE") == str(datetime.date(datetime.now())):
				return False 

		else:
			for key in EmptyPoints:
				data[UserID][key] = EmptyPoints[key]

		data.add(UserID, "COOKIES", 1)
		data.set(UserID, "COOKIE-DATE", str(datetime.date(datetime.now())))
		data.add(UserID, "NUTS", 300)
		data.add(UserID, "TOTAL-NUTS", 300)


		WritePoints(data)

		return True

	# To Set UserID's points to something specific
	def PointsSet(UserID: int, key: str, change: int) -> bool:
		global EmptyPoints

		data = GetPoints()

		UserID = str(UserID)

		if UserID not in data and "POG" not in data[UserID]:
			for key in EmptyPoints:
				data[UserID][key] = EmptyPoints[key]

		data[UserID][key] = change

		WritePoints(data)

		return True

	# Changes points of UserID by amnt in key
	def PointsAdd(UserID: int, key: str, amnt: int) -> bool:
		global EmptyPoints

		data = GetPoints()

		UserID = str(UserID)

		if UserID not in data and "POG" not in data[UserID]:
			for key in EmptyPoints:
				data[UserID][key] = EmptyPoints[key]

		if key in data[UserID]:
			data[UserID][key] += int(amnt)

		else:
			data[UserID][key] = int(amnt)

		WritePoints(data)

		return True

	# Returns dictionary of the points of `UserID`
	def ViewPoints(UserID: int) -> dict:
		global EmptyPoints

		data = GetPoints()

		UserID = str(UserID)

		if UserID not in data and "POG" not in data[UserID]:
			return EmptyPoints

		else:
			return data[UserID]

	# Ranks UserID's [key] points
	def RankPoints(UserID: int, key: str) -> int:
		global EmptyPoints

		data = GetPoints()

		UserID = str(UserID)
			
		rank = 1

		if UserID not in data and "POG" not in data[UserID]:
			for key in EmptyPoints:
				data[UserID][key] = EmptyPoints[key]

		else:
			UserPoints = data[UserID][key]

		for i in data:
			if data[i][key] > UserPoints:
				rank += 1

		return rank

	# Returns the Points File sorted by highest User [key] to lowest user [key]
	def SortByIndex(key: str, data1: dict = GetPoints()) -> list:

		data2 = []

		for UserID in data1:

			if "PROFILE" in data1[UserID]:
				data2.append([UserID, data1[UserID][key], data1[UserID]["PROFILE"]])

			elif key not in data1[UserID]:
				return False
			
			else:
				data2.append([UserID, data1[UserID][key]])

		return sorted(data2, key = itemgetter(1))[::-1]

# Functions for changing Map information
if True:

	# This function is for setting the map data of `UserID`
	def MapSet(UserID: int, MapIndexes: list) -> bool:
		global EmptyPoints

		if lindex(GetMap()).RTN(MapIndexes) is False:
			return False

		data = lindex(GetPoints()).set(UserID, "RPG", "location", MapIndexes)

		WritePoints(data)

		return True

	# Returns the Map Index of `UserID`
	def MapView(UserID: int) -> dict:

		global EmptyMap

		Indexes = lindex(GetPoints()).RTN(UserID, "RPG", "location")

		if Indexes is False:
			Indexes = EmptyMap

		return lindex(GetMap()).RTN(*Indexes)

# General Item Functions
if True:
	# Adds `item` to `UserID`'s inventory
	def AddGeneralItem(UserID: int, item):
		data = GetItems()

		ItemType = type(item)

		if ItemType == item:
			return GiveItem(UserID, item)

		if ItemType == melee:
			return GiveMelee(UserID, item)

		return False

	# Takes item index and returns the item that corellates to it | Returns different classes depending on the item
	def ReturnGeneralItem(item: str):

		data = GetItems()

		ItemsFound = []

		for category in data:
			if item in data[category]:

				if category == "items":
					return GetItem(item)

				if category == "melee":
					return GetMelee(item)

				if category == "enemy":
					return GetEnemy(item)

		return False

# Functions for ajusting items that belong to players
if True:
	class item:

		def __init__(self, name: str, price: int, ItemKey: str, description: str, ItemType: str="items"):
			self.name = name
			self.price = price
			self.ItemKey = ItemKey
			self.description = description
			self.ItemType = ItemType

	# Adds item to the `items.plk` file
	def AddItem(ItemData: item) -> bool:

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

	# Returns class version of Items based on ItemKey & ItemType
	def GetItem(ItemKey: str, ItemType: str="items"):
		
		data = GetItems()

		if ItemKey in data[ItemType]:
			return item(data[ItemType][ItemKey]["name"], data[ItemType][ItemKey]["price"], ItemKey, data[ItemType][ItemKey]["description"], ItemType)

		return False

	# This is for if someone buys an item from an item shop
	def BuyItem(UserID: int, ItemData: item):
		global EmptyPoints

		data = lindex(GetPoints())

		UserID = str(UserID)

		UsersCash = data.RTN(UserID, "RPG", "cash")

		if UsersCash >= ItemData.price:
			data.add(UserID, "RPG", "cash", num = -ItemData.price)
			data.add(UserID, "RPG", ItemData.ItemType, ItemData.ItemKey, num = 1)

			WritePoints(data)

			return True

		return False

	# Returns a list of all the items 'UserID' has
	def ViewItems(UserID: int) -> list:

		UserID = str(UserID)

		data = lindex(GetPoints()).RTN(UserID, "RPG", "items")

		if data is False:
			return []

		items = []
		
		for item in data:
			if ReturnGeneralItem(item) is not False:
				items.append([ReturnGeneralItem(item), data[item]])

		return items

	# Gives a `UserID` a `ItemData`
	def GiveItem(UserID: int, ItemData: item) -> bool:
		global EmptyPoints
		
		data = lindex(GetPoints())
		
		UserID = str(UserID)

		indexes = [UserID, "RPG", ItemData.ItemType, ItemData.ItemKey]

		data.add(*indexes, num = 1)
		
		return True

# Melee Items with Item File
if True:
	class melee(item):

		def __init__(self, name, price, ItemKey, description, damage, CritPercent, ItemType="melee"):
			super().__init__(name, price, ItemKey, description, ItemType)
			self.damage = damage
			self.CritPercent = CritPercent

	# Adds `MeleeData` to items.plk file
	def AddMelee(MeleeData: melee) -> bool:

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

	# Returns `melee` class based on `MeleeKey`
	def GetMelee(MeleeKey: str, ItemType="melee"):
		
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

	# Returns list of all the melees 'UserID' has
	def ViewMelee(UserID: int) -> list:
		UserID = str(UserID)

		PlayerData = lindex(GetPoints()).RTN(UserID, "RPG", "melee")

		if PlayerData is not False:
			# Returns a list of ["Item Data", "Amount"]
			return [(GetMelee(item), PlayerData[item]) for item in PlayerData]

		else:
			return [(GetMelee("TEST_hand"), 2)]

	# Gives a player a melee weapon
	def GiveMelee(UserID: int, MeleeData: melee) -> bool:
		global EmptyPoints

		data = lindex(GetPoints())
		UserID = str(UserID)
		item = GetMelee(MeleeData.ItemKey)
		indexes = [UserID, "RPG", MeleeData.ItemType, MeleeData.ItemKey]

		data.add(indexes, num = 1)

		WritePoints(data)

		return True

# Enemy Data with Item File
if True:
	class enemy:

		def __init__(self, name, level, health, xp, cash, EnemyKey, description, WeaponKey, WeaponType="melee", WeaponDrop=False, ItemType="enemy"):
			self.name = name
			self.level = level
			self.health = health
			self.xp = xp
			self.cash = cash
			self.EnemyKey = EnemyKey
			self.description = description
			self.WeaponKey = WeaponKey
			self.WeaponType = WeaponType
			self.WeaponDrop = WeaponDrop
			self.ItemType = ItemType

	def AddEnemy(EnemyData: enemy) -> bool:

		data = GetItems()

		if EnemyData.ItemType not in data:
			data[EnemyData.ItemType] = {}

		if EnemyData.EnemyKey in data[EnemyData.ItemType]:
			return False

		data[EnemyData.ItemType][EnemyData.EnemyKey] = {
			"name" : EnemyData.name,
			"level" : EnemyData.level,
			"health" : EnemyData.health,
			"xp" : EnemyData.xp,
			"cash" : EnemyData.cash,
			"description" : EnemyData.description,
			"WeaponKey" : EnemyData.WeaponKey,
			"WeaponType" : EnemyData.WeaponType,
			"WeaponDrop" : EnemyData.WeaponDrop,
			"ItemType" : EnemyData.ItemType
		}

		WriteItems(data)

		return True

	# Returns `enemy` Class based on ItemKey
	def GetEnemy(ItemKey, ItemType="enemy"):

		data = GetItems()

		if ItemKey in data[ItemType]:
			return enemy(
				data[ItemType][ItemKey]["name"],
				data[ItemType][ItemKey]["level"],
				data[ItemType][ItemKey]["health"],
				data[ItemType][ItemKey]["xp"],
				data[ItemType][ItemKey]["cash"],
				ItemKey,
				data[ItemType][ItemKey]["description"],
				data[ItemType][ItemKey]["WeaponKey"],
				data[ItemType][ItemKey]["WeaponType"],
				data[ItemType][ItemKey]["WeaponDrop"]
			)

		else:
			return False

# Combat xp Functions
if True:
	class experience:
		def __init__(self, name):
			self.name = name

	# Gives `UserID` `change` `key` xp
	def GiveCombatPoints(UserID: int, key: str, change: int) -> bool:
		global EmptyPoints
		global EmptyStats

		if key not in EmptyStats:
			return False

		data = lindex(GetPoints())
		UserID = str(UserID)
		indexes = [UserID, "RPG", "CombatStats"]

		UserCombatStats = data.RTN(*indexes)

		if UserCombatStats is False:
			UserCombatStats = EmptyStats
			data.set(*indexes, num = EmptyStats)

		indexes.append(key)

		data.add(*indexes, change)

		WritePoints(data)

		return True

	# returns a list of (StatKeys, AmountAtStatKeys)
	def ViewCombatPoints(UserID: int) -> list:
		global EmptyStats

		data = GetPoints()

		UserID = str(UserID)

		# Going over stats and making "OVERALL" first in most menus

		StatKeys = [ xp for xp in EmptyStats ]
		StatKeys = [StatKeys[-1], *StatKeys[:-1:]]

		if UserID in data and "RPG" in data[UserID] and "CombatStats" in data[UserID]["RPG"]:
			return [ [experience(entry), data[UserID]["RPG"]["CombatStats"][entry]] for entry in StatKeys ]

		else:
			return [ [experience(entry), EmptyStats[entry]] for entry in StatKeys ]

	# returns a dictionary of `UserID`'s Combat Points
	def ViewCombatPointDict(UserID: int) -> dict:
		global EmptyStats

		CBP = lindex(GetPoints()).RTN(str(UserID), "RPG", "CombatStats")

		if CBP is False:
			return EmptyStats

		return CBP

	# returns HP based on HP level
	def GetHP(level: int) -> int:
		1
		return 50 + level * 5

	# Returns CombatPointLevel based on xp
	def GetCombatPointLevel(xp: int) -> int:
		1
		return int(0.1 * (int(xp) + 90) ** .5)

	# Returns how much Cash `UserID` has
	def ViewCash(UserID: int) -> int:
		1
		return int(lindex(GetPoints()).RTN(str(UserID), "RPG", "cash"))

	# Gives a `UserID` `amnt` of cash
	def GiveCash(UserID: int, amnt: int) -> bool:

		global EmptyPoints

		UserID = str(UserID)
		data = lindex(GetPoints())
		indexes = [UserID, "RPG", "cash"]

		# uses int because if IndexCarve returns `False` it will be turned into `0`
		data.add(*indexes, amnt)

		WritePoints(data)

		return True

# Map Functions with map & points file
if True:

	# Gets Data & NPC's that are close to `UserID`
	def GetClose(UserID: int) -> list:
		QUERY()
		


# lindex(GetPoints()).pprint()
# lindex(GetMap()).pprint()