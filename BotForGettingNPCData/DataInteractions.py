#!/usr/bin/env python3

import json
from Lindex import lindex
from time import asctime
from random import randint

database = "PersonInfo.dtb"

def QUERY() -> bool:
	global database

	FILEISBROKENSTRING = "{}"

	# Makes sure that PersonInfo.dtb file exists and works properly
	try:
		with open(database, "r") as file:
			json.loads(file.read())
			file.close()

	except:
		with open(database, "r") as file:
			data = file.read()
			file.close()

		name = "Backup--" + "-".join(asctime().split(":")) + ".dtb"
		# name = "-".join(name.split(":"))


		with open(name, "w") as file:
			file.write(data)
			file.close()
		with open(database, "w") as file:
			file.write(FILEISBROKENSTRING)
			file.close()

# Returns PersonInfo
def GetInfo() -> dict:
	global database
	QUERY()

	with open(database, "r") as data:
		file = json.loads(data.read())
		data.close()

	return lindex(file)

# Writes file to PersonInfo file
def WriteInfo(file: dict) -> bool:
	global database
	QUERY()

	with open(database, "w") as data:
		data.write(json.dumps(file))
		data.close()

	return True

def AddIndex(UserName: str, Type: str, data: str):

	# print(f"name: {UserName}\nType: {Type}\nData: {data}")

	def DictionaryifyString(data: str) -> dict:

		data = data.split(",")

		def SplitOnEqual(ind):
			t = ind.split("=")
			t[0] = RemoveSpaces(t[0])
			t[1] = RemoveSpaces("".join(i for i in t[1::]))
			return t

		def RemoveSpaces(string):
			badletters = " \"\'"
			try:
				while string[0] in badletters:
					string = string[1:]
				while string[-1] in badletters:
					string = string[:-1]
			except:
				string = ""
			return string

		data = [SplitOnEqual(i) for i in data]

		data = dict(data)

		return data

	data = DictionaryifyString(data)

	if "name" in data:
		Name = data["name"]
	else:
		Name = "".join( chr(randint(65, 90)) for i in range(4) )

	DTBData = GetInfo()
	DTBData.set(Type, UserName, Name, data)
	WriteInfo(DTBData)

# lindex(GetInfo()).pprint()

# AddIndex(UserName = "Some1and2#2570", Type = "weapon", data = """name = "Rlly Good Sword", price = 250, ComputerName = "Good_Sword_1", description = "Swing Swong", damage = 9""")
# +add_weapon name = "Rlly Good Sword", price = 250, ComputerName = "Good_Sword_1", description = "Swing Swong", damage = 9