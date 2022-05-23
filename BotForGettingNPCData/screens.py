#!/usr/bin/env python3

#!/usr/bin/env python3

from discord import Embed
from discord.ui import Button, View
from table2ascii import table2ascii as t2a, PresetStyle
# Text NPC

def GetTextNPCText(TextItems):
	1
	return TextItems[0]

class TextNPCView:
	def __init__(self, name: str, dialog: list, message):

		self.message = message

		self.title = f"***{name}***"
		self.content = GetTextNPCText(dialog)
		self.color = 0xfbff00

		dialog = dialog[1::]

		self.CallCommand = name

		if len(dialog) != 1 or True:
			self.view = [
				TextNPCScrollButton(label="NEXT", name=name, dialog=dialog, message=message, style=1)
			]

		else:
			self.view = [
				
			]

		# Stuff for adding shop NPC to item file
		self.ItemType = "NPC"
		self.NPCType = "text"

	async def open(self, interaction=None):

		embed = Embed(
			title=self.title,
			description=self.content,
			color = self.color
		)

		view=View()

		for Item in self.view:
			view.add_item(Item)

		if interaction is None:
			return await self.message.channel.send(embed=embed, view=view)

		else:
			return await interaction.response.edit_message(embed=embed, view=view)

class TextNPCScrollButton(Button):
	def __init__(self, label: str, name: str, dialog: list, message, style=None):
		super().__init__(label=label, style=style)
		self.name = name
		self.dialog = dialog
		self.message = message

	async def callback(self, interaction):
		if interaction.user.id == self.message.author.id:
			if len(self.dialog) > 0:
				await TextNPCView(self.name, self.dialog, self.message).open(interaction)

			else:
				await interaction.message.delete()
				try:
					await self.message.delete()
				except:
					print("Unable to Delete Message!\nMessage no longer Exists")
				return
				

		else:
			await interaction.response.send_message("This view is Not Yours!", ephemeral=True)
			return
