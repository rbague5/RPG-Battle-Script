from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

print("\n\n")


# Create Black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")


# Create White magic
cure = Spell("Cure", 25, 120, "white")
cura = Spell("Cura", 32, 200, "white")


#Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixir", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixir", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
				{"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
				{"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]



# Instantiate People / Person(hp, mp, atk, df, magic)
player1 = Person("Valos :", 3260, 132, 300, 34, player_magic, player_items)
player2 = Person("Nick  :", 4160, 188, 300, 34, player_magic, player_items)
player3 = Person("Robot :", 3089, 174, 300, 34, player_magic, player_items)
enemy = Person("Magus   :", 1200, 701, 525, 25, [], [])

players = [player1, player2, player3]



running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATACKS!" + bcolors.ENDC)

while running:
	print("===========================")
	print("\n\n")
	print("NAME                     HP                                                          MP")

	for player in players:
		player.get_stats()

	for player in players:

		player.choose_action()
		choice = input("    Chose action:")
		index = int(choice) - 1

		if index == 0:
			dmg = player.generate_damage()
			enemy.take_damage(dmg)
			print("You attacked for", dmg, "points of damage.")
		elif index == 1:
			player.choose_magic()
			magic_choice = int(input("Choose magic:")) - 1

			if magic_choice == -1:
				continue

			spell = player.magic[magic_choice]
			magic_dmg = spell.generate_damage()

			current_mp = player.get_mp()

			if spell.cost > current_mp:
				print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
				continue

			player.reduce_mp(spell.cost)

			if spell.type == "white":
				player.heal(magic_dmg)
				print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
			elif spell.type == "black":
				enemy.take_damage(magic_dmg)
				print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

		elif index == 2:
			player.choose_items()
			item_choice = int(input("Choose item:")) - 1

			if item_choice == -1:
				continue

			item = player.items[item_choice]["item"]

			if player.items[item_choice]["quantity"] == 0:
				print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
				continue

			player.items[item_choice]["quantity"] -= 1

			if item.type == "potion":
				player.heal(item.prop)
				print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
			elif item.type == "elixer":
				player.hp = player.maxhp
				player.mp = player.maxmp
				print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
			elif item.type == "attack":
				enemy.take_damage(item.prop)
				print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage" + bcolors.ENDC)

	enemy_choice = 1

	enemy_dmg = enemy.generate_damage()
	player1.take_damage(enemy_dmg)
	print("Enemy attacks for", enemy_dmg)

	print("--------------------------")
	print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")

	if enemy.get_hp() == 0:
		print(bcolors.OKGREEN + bcolors.BOLD + "YOU WIN!" + bcolors.ENDC)
		running = False
	elif player.get_hp() == 0:
		print(bcolors.FAIL + bcolors.BOLD + "Your enemy has defeated you!" + bcolors.ENDC)
		running = False


