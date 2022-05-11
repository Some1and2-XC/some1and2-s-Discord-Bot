#!/usr/bin/env python3

from NPC import *

def MakeAll():

	data = GetItems()

	ItemList = [
		# General Items
		item(name="Sticks", price=50, ItemKey="TEST_Stick", description="Just a stick"),
		item(name="Bombs", price=50, ItemKey="TEST_Bomb", description="Don't drop it!"),
		item(name="Arrows", price=50, ItemKey="TEST_Arrow", description="Bow Bullets"),

		# General Weapons
		melee(name="Hands", price=500, ItemKey="TEST_hand", description="Just your Hand?", damage=5, CritPercent=0),
		melee(name="Bronze Sword", price=10, ItemKey="TEST_bronze_sword", description="Good & Reliable Weapon", damage=10, CritPercent=10),
		melee(name="Sword O'Big PP", price=69420420, ItemKey="TEST_god_sword", description="giuy", damage=42069, CritPercent=200),
		melee(name="The Bee Movie", price=15, ItemKey="TEST_Bee", description="According...", damage=314159265, CritPercent=0),

		# General Enemies
		enemy(name="Zombie", level=1, health=15, xp=10, cash=5, EnemyKey="TEST_Zombie", description="Ah jeez, hes just a really bad guy y'know?", WeaponKey="TEST_bronze_sword", WeaponDrop=True),
		enemy(name="Big Bad uhh, Boss guy?", level=500, health=42069, xp=250000, cash=420420, EnemyKey="TEST_BAD", description="bbbbbbbbbad guy", WeaponKey="TEST_god_sword", WeaponDrop=True),

		# General NPCs

		NPC(name="ShopKeeper - Zan", dialog="WELCOME TRAVELER!", PersonIndex="TEST_SHOP_zan", NPCType="shop", ItemType="NPC", items=["TEST_Stick", "TEST_Bomb", "TEST_Arrow"]),
		NPC(name="???", dialog=["go away"], PersonIndex="NPC_filler1", NPCType="text", ItemType="NPC")
	]

	NewDone = 0

	# If the new items that are added to the file wants to be printed off
	ShowNew = False

	for SingularItem in ItemList:
		initial = NewDone
		if SingularItem.ItemType == "items":
			if AddItem(SingularItem):
				NewDone += 1

		if SingularItem.ItemType == "melee":
			if AddMelee(SingularItem):
				NewDone += 1

		if SingularItem.ItemType == "enemy":
			if AddEnemy(SingularItem):
				NewDone += 1

		if SingularItem.ItemType == "NPC":
			if AddNPC(SingularItem):
				NewDone += 1

		if initial != NewDone and ShowNew:
			print(f"Item: {SingularItem}\nData: {SingularItem.__dict__}")

	print(f"{NewDone} / {len(ItemList)} New Items Made")

	return

MakeAll()