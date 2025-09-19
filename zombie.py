"""
Title : Group Project (Zombie Game)
Author: Team Anarchy
Date:
"""

import datetime

BOLD = "\033[1m"
NORMAL = "\033[0m"
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'

today = datetime.date.today()
locations = "none"
current_location = "none"
inventory = []
health = 0
set_time = 0
current_time = 0
target_time = datetime.datetime.combine(today, datetime.time(17, 30))

def reset_game():
    global health, locations, current_location, inventory, set_time, current_time
    health = 100
    locations = {
        "residence_dining_center": {
            "description": "You are in the RDC. You hear a loud noise. turning your head you see what you can only describe as zombies attacking others.\nYou run to the exit, you stop at the doors you can choose to hide or go out?",
            "exits": {"out": "rdc_hallway", },
            "items": [],
            "item_desc": "",
            "hide": "a zombie scratches you!",
            "hide_result": "damage",
            "safe": True,
            "damage": 20,
        },
        "rdc_hallway": {
            "description": "You're heart racing you must choose go left towards the dorms or go right towards kirby student center",
            "exits": {"left": "griggs_hall", "right": "kirby_student_center_floor_3", },
            "items": ["backpack"],
            "item_desc": "On the ground you see a",
            "hide": "You hide in the bathrooms for 2 mins",
            "hide_result": 120,
            "safe": False,
            "safe_result": "As you attempt to leave a zombie scratches you",
            "damage": 20,
        },
        "griggs_hall": {
            "description": "You entered griggs hall. You think you hear a noise",
            "exits": {"back": "rdc_hallway"},
            "items": [],
            "item_desc": "",
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "safe": True,
        },
        "kirby_student_center_floor_3": {
            "description": "You entered kirby student center floor 3.",
            "exits": {"back": "rdc_hallway", "down": "kirby_student_center_floor_2", },
            "items": [],
            "item_desc": "",
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "safe": True,
        },
        "kirby_student_center_floor_2": {
            "description": "You entered kirby student center floor 2.",
            "exits": {"up": "kirby_student_center_floor_3", },
            "items": [],
            "item_desc": "",
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "safe": True,
        }
    }
    current_location = "residence_dining_center"
    inventory = []
    set_time = datetime.time(17, 0, 0)
    current_time = datetime.datetime.combine(today, set_time)

def add_time(time):
    global current_time
    current_time += datetime.timedelta(seconds=time)

def display_menu():
    print("\n--- Main Menu ---")
    print("1. Display Rules")
    print("2. Play Game")
    print("3. Exit")

def display_time():
    global current_time
    print(f"You look at your phone, its currently {current_time}")

def display_health():
    global health
    print(f"Your current health: {BLUE}{health}{NORMAL}")

def display_rules():
    print("Commands: Go, Take, Inventory, Use, Attack, Hide, Time, Health, Menu")

def display_location():
    print(locations[current_location]["description"])
    if locations[current_location]["items"]:
        print(locations[current_location]["item_desc"], ", ".join(locations[current_location]["items"]))

def handle_command(command):
    global current_location, inventory, current_time, health
    parts = command.lower().split()
    verb = parts[0]
    noun = " ".join(parts[1:]) if len(parts) > 1 else ""

    if verb == "go":
        if noun in locations[current_location]["exits"]:
            if locations[current_location]["safe"] == False:
                print(f"{locations[current_location]["safe_result"]}, you take {RED}{locations[current_location]["damage"]} damage{NORMAL}")
                health -= locations[current_location]["damage"]
            current_location = locations[current_location]["exits"][noun]
            add_time(30)
        else:
            print("You can't go that way.")
    elif verb == "take":
        if noun in locations[current_location]["items"]:
            inventory.append(noun)
            locations[current_location]["items"].remove(noun)
            print(f"You took the {noun}.")
        else:
            print(f"There is no {noun} here.")
    elif verb == "hide":
        print(locations[current_location]["hide"])
        if locations[current_location]["hide_result"] == "damage":
            health -= locations[current_location]["damage"]
            print(f"You take {RED}{locations[current_location]["damage"]} damage{NORMAL}")
        elif locations[current_location]["hide_result"] >= 0:
            add_time(locations[current_location]["hide_result"])
            if locations[current_location]["safe"] == False:
                locations[current_location]["safe"] = True
    elif verb == "inventory":
        if inventory:
            print("Your inventory:", ", ".join(inventory))
        else:
            print("Your inventory is empty.")
    elif verb == "time":
        display_time()
    elif verb == "health":
        display_health()
    else:
        print("Invalid command.")

def main_menu():
    global health, current_time
    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            display_rules()
        elif choice == '2':
            while True:
                display_location()
                command = input("> ").strip()
                if command == "menu":
                    break
                else:
                    handle_command(command)
                if health == 0:
                    print(f"You Died\n{RED}Game Over!{NORMAL}")
                    reset_game()
                    break
                if current_time >= target_time:
                    print(f"The zombies have overrun the school.\n{RED}Game Over!{NORMAL}")
                    reset_game()
                    break
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

reset_game()
main_menu()
