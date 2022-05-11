#!/usr/bin/env python3

# Quality of Life

import json
from random import randint

def ReturnPointsString(UserID: int, data: dict) -> str:

	string = f"<@!{UserID}> has **"
	for i in range(1, 9):
		
		key = IndexToKey(i)
		if key is not False:
			string += f"{data[key]} {key}"
			if i != 8:
				if i == 7:
					string += " and "
				else:
					string += " | "

	return f"{string}**"

def ReturnLVLString(UserID: int, data: dict) -> str:
	string = f">>> <@!{UserID}> has **"

	string += " | ".join( f"{XPType} LVL{data[XPType]}" for XPType in data )

	string += "**"

	return string

def IndexToKey(Index: int) -> str:
	if Index == 1:
		key = "POG"
	if Index == 2:
		key = "KEK"
	if Index == 3:
		key = "SUS"
	if Index == 4:
		key = "IQ"
	if Index == 5:
		key = "COOKIES"
	if Index == 6:
		key = False
	if Index == 7:
		key = "NUTS"
	if Index == 8:
		key = "TOTAL-NUTS"
	return key

def DoesUserIDExist(UserID: int) -> bool:
	with open("points.plk", "r") as file:
		data = json.loads(file.read())
		file.close()
	
	if str(UserID) in data:
		return True

	else:
		return False

def IfCommand(MessageData, command: str, TestMode: bool) -> bool:
	if MessageData.content.lower().startswith(command.lower()) and not TestMode:
		return True
	else:
		return False

def GetFifteenPercent(number: int) -> int:
	1
	return int(.5 + number * 0.01 * (85 + randint(0, 30)))

def IndexCarve(MapDict: dict, Indexes: list):
	# Goes through `MapDict` looking for the next index in the `Indexes`
	if len(Indexes) == 0:
		return MapDict
	if Indexes[0] not in MapDict:
		return False
	return IndexCarve(MapDict[Indexes[0]], Indexes[1:])

def IndexWriteCarve(PointsDict: dict, Indexes: list, FinalState={}) -> dict:
	# takes PointsDict, uses the Indexes list and changes that index to FinalState. Returns the list changed
	def Carve(PointsDict: dict, Indexes: list, FinalState, States: list = []) -> list:
	
		States.append(PointsDict)

		if len(Indexes) == 0:

			if FinalState is not None:
				States[-1] = FinalState

			return States
	
		if Indexes[0] not in PointsDict:
			PointsDict[Indexes[0]] = {}

		return Carve(PointsDict[Indexes[0]], Indexes[1:], FinalState, States)

	def Write(Indexes: list, States: list) -> dict:

		for i in range(len(States) - 1):
			States[-i-2][Indexes[-i-1]] = States[-i-1]

		return States[0]

	return Write(Indexes, Carve(PointsDict, Indexes, FinalState))