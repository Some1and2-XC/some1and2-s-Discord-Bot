# `@some1and2`'s RPG discord bot
A discord bot developed by @some1and2 the aims to function as an `RPG` within the format of a discord bot

# Functionality
 - Map System
    - The bot has a system which has a `json` file that has all the map information on it
    - The map works by holding nestled dictionaries that functonally work as directories that lead to the backend names of NPC's

 - Various NPC's
    - The bot uses the backend names of NPC's to index them from the `items.plk` file to create `NPC` data objects
    - These data objects are based on classes which come in a few forms:
       - Shop
       - Text
       - Enemy
    - These `NPC`'s use the interaction variables set to respond to when they are called

 - Menu System
    - The bot also sports a top of the line `menu`
    - Menu uses menu buttons to cycle through different types of inventories the player has
    - Menu displays important information such as how much `cash` (the in game currency) a particular player has as well as how much `xp` each player has

 - Combat System
    - No `RPG` is complete without a combat system!
    - The combat system thus far is fairly basic, you have a `health` amount, based on the amount of `health` `xp` you have
    - The amount of damage is dependent on the weapon selected, the menu for the combat system has options for various kinds of `melee` combat weapons
    - After an enemy dies, it drops an amount of cash which is preset in the `items.plk` file
    - it also either drops the weapon is uses, unless the player already has its weapon in which case it drops that weapons corresponding cash value (also set in `items.plk`)

 - Leveling System
    - The bot has an exponential leveling system designed to make it harder to get higher of a level the more xp you have
    - The level is calculated by the cumulative amount of `xp` a player has and is generally calculated on the fly [the player level is not stored anywhere, the xp is]


# Basic Structure of Files::
 - The configuration of the `discord.py` elements as well as settings up how the bot will reaction to messages. 
 - Most commands use `IfCommand()` function, the basic use of it is to see if a message starts with a certain string, returning True if it does. 
 - The majority of the work is done by the back end instead of by the botCV.py file
 - Each type of `NPC` in the `NPC.py` file works by having two classes and a function attached to them
 - The main class that is made for each type of `NPC` calls the `Get Text` function attached to the `NPC` type to attach text to the view sent by botCV.py
 - The secondary class attached to each `NPC` is the class for the `NPC`'s buttons
 - The `NPC`'s buttons work by responding to actions taken by reconstructing a new message and calls back to the main `NPC` class to resend a new message \[With data from the Old `NPC` class\]

# Current Work::
### See `TODO.md` to see what is being worked

---
*Reach out to @some1and2 for clairification if needed*
