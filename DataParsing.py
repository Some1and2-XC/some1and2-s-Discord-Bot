#!/usr/bin/env python3

# Data Parsing

import re

def ParseForNum(message, listOfCmds: list):
	# Takes a Message and returns a number, command and user it is directed at
	message = message.lower()
	try:
		num = re.findall(r"^[/-]?[0-9]+", message)[0]
		usr = re.findall(r"[\<\@\!]+[0-9]+\>", message)[0]
		for TestCmd in listOfCmds:
			cmd = re.findall(re.escape(TestCmd.lower()), message.lower())
			if cmd != []:
				cmd = cmd[0]
				if re.findall(r"^" + re.escape(num + cmd + " " + usr), message) != []:
					usr = re.findall(r"[0-9]+", usr)[0]
					return (num, cmd.upper(), usr)
		return False

	except:
		return False

def ParseForCmd(cmd: str, text: str):
	# gets command and returns userid supplied
	# "!command <!@69420>"
	# Returns 69420

	try:
		UserID = re.findall(r"^" + re.escape(cmd) + r" [\<\@\!]*[0-9]+", text)[0]
		UserID = re.findall(r"[0-9]+", UserID)[0]
		return UserID

	except:
		return False

def ParseForValue(cmd: str, text: str):
	# Gets the text after a command !top iq, returns iq
	try:
		if text.startswith(str(cmd)):
			return text.split(" ")[1]
		else:
			return False
	except:
		return False

def ParseForShopItem(cmd: str, text: str):
	try:
		text = text.lower()
		cmd = cmd.lower()
		if text.startswith(cmd) and len(text) > len(cmd):
			text = text[len(cmd)::]
			text = re.findall(r"^[ ]?[A-Za-z]+", text)[0]
			text = re.findall(r"[A-Za-z]+", text)[0]
			if text is not None:
				return text
			else:
				return False
		else:
			return False

	except:
		return False
