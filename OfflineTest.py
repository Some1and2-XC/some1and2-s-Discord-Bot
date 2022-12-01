#!/usr/bin/env python3

from Test_botCV import on_message

import asyncio

def CarefulPrint(t: str):
	for i in str(t):
		try:
			print(i, end="")
		except:
			print("@", end="")
	print()

def ViewButtons(view):
	t = " | ".join( str(i.label) for i in view._children)
	CarefulPrint(t)

class message:
	def __init__(self, content: str, UserName: str = "some1and2", UsrID: int = 42069):
		self.content = content
		self.UserName = UserName

		class author:
			def __init__(self):
				self.id = UsrID

		self.author = author()

	class channel:
		# def send(message: str = "", embed = None, view = None):
		async def send(*args, **kwargs):
			global GBLmessage, GBLembed, GBLview

			message = args
			if "embed" in kwargs:
				embed = kwargs["embed"]

			if "view" in kwargs:
				view = kwargs["view"]

			try:
				print(messsage)
			except:
				print("--No Message attached--")

			if embed is not None and view is not None:
				print(embed)
				print(view)

				print("-" * 25)

				print(embed.title)
				print(embed.description)

				ViewButtons(view)

			GBLmessage = message
			GBLembed = embed
			GBLview = view

class interaction:
	def __init__(self):
		UsrID = 1
		class user:
			def __init__(self):
				self = message.author
t = message("+tst")

asyncio.run(on_message(t))

# CarefulPrint(GBLview.children[0])

input()