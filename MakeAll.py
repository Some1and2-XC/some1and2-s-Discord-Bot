#!/usr/bin/env python3

from NPC import *

def MakeAll():

	data = GetItems()


	ItemList = [
		item(name="Sticks", price=50, ItemKey="TEST_Stick", description="Just a stick"),
		item(name="Bombs", price=50, ItemKey="TEST_Bomb", description="Don't drop it!"),
		item(name="Arrows", price=50, ItemKey="TEST_Arrow", description="Bow Bullets"),
		melee(name="Bronze Sword", price=500, ItemKey="TEST_bronze_sword", description="Good & Reliable Weapon", damage=10, CritPercent=10),
		enemy(name="Zombie", health=50, xp=10, EnemyKey="TEST_Zombie", description="Ah jeez, hes just a really bad guy y'know?", WeaponKey="TEST_bronze_sword", WeaponDrop=False)
	]

	NewDone = 0

	for SingularItem in ItemList:
		if SingularItem.ItemType == "items":
			if AddItem(SingularItem):
				NewDone += 1

		if SingularItem.ItemType == "melee":
			if AddMelee(SingularItem):
				NewDone += 1

		if SingularItem.ItemType == "enemy":
			if AddEnemy(SingularItem):
				NewDone += 1

	print(f"{NewDone} / {len(ItemList)} New Items Made")


	return

MakeAll()