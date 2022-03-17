#!/usr/bin/env python3

# Quality of Life

import json
from random import randint

def ReturnPointsString(UserID, data):

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

def IndexToKey(Index):
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

def DoesUserIDExist(UserID):
	with open("points.plk", "r") as file:
		data = json.loads(file.read())
		file.close()
	
	if str(UserID) in data:
		return True

	else:
		return False

def IfCommand(MessageData, command, TestMode):
	if MessageData.content.lower().startswith(command.lower()) and not TestMode:
		return True
	else:
		return False

def GetFifteenPercent(number):
	1
	return int(number * 0.01 * (85 + randint(0, 30)))
