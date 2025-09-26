"""
Title : Group Project (Zombie Game)
Author: Team Anarchy
Date:
"""

import datetime
import cv2


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
command_list = ["out","take","drop","use","left","right","up","down","in","back","turn","examine","fight","defend","run","read"]
items = {
    "backpack":{
        "description": "you see a backpack on the ground.",
        "examine": "Its empty, might still have a use.",
    },
    "knife":{
        "description": "you see a knife.",
        "examine": "A sharp knife, it could be useful.",
    },
}

def reset_game():
    global health, locations, current_location, inventory, set_time, current_time
    health = 100
    locations = {
        "residence_dining_center": {
            "description": "You are in the RDC. You hear a loud noise. turning your head you see what you can only describe as zombies attacking others.\nYou run to the exit, you stop at the doors you can choose to hide or go out?",
            "exits": {"out": "rdc_hallway", },
            "items": ["knife"],
            "hide": "a zombie scratches you!",
            "hide_result": "damage",
            "safe": True,
            "damage": 20,
            "map": "rdc.png",
        },
        "rdc_hallway": {
            "description": "You're heart racing you must choose go left towards the dorms or go right towards kirby student center",
            "exits": {"left": "griggs_hall", "right": "kirby_student_center_floor_3", },
            "items": ["backpack"],
            "hide": "You hide in the bathrooms for 2 mins",
            "hide_result": 120,
            "safe": False,
            "safe_result": "As you attempt to leave a zombie scratches you",
            "damage": 20,
            "map": "rdc_hallway.png",
        },
        "griggs_hall": {
            "description": "You entered griggs hall. You think you hear a noise",
            "exits": {"back": "rdc_hallway"},
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "safe": True,
            "map": "griggs.png",
        },
        "kirby_student_center_floor_3": {
            "description": "You entered kirby student center floor 3.",
            "exits": {"back": "rdc_hallway", "down": "kirby_student_center_floor_2", },
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "safe": True,
            "map": "ksc.png",
        },
        "kirby_student_center_floor_2": {
            "description": "You entered kirby student center floor 2.",
            "exits": {"up": "kirby_student_center_floor_3", },
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "safe": True,
            "map": "ksc.png",
        }
    }
    current_location = "residence_dining_center"
    inventory = []
    set_time = datetime.time(17, 0, 0)
    current_time = datetime.datetime.combine(today, set_time)

def add_time(time):
    global current_time
    current_time += datetime.timedelta(seconds=time)

def display_health():
    global health
    print(f"Your current health: {BLUE}{health}{NORMAL}")

def display_inventory():
    if inventory:
        print("Your inventory:", ", ".join(inventory))
    else:
        print("Your inventory is empty.")

def display_location():
    print(locations[current_location]["description"])
    if locations[current_location]["items"]:
        items_in_location = locations[current_location]["items"]
        for item_name in items_in_location:
            print(items[item_name]["description"])

def display_menu():
    print("\n--- Main Menu ---")
    print("1. Display Rules")
    print("2. Play Game")
    print("3. Exit")

def display_rules():
    print("Commands: Go, Take, Inventory, Drop, Hide, Time, Health, Examine, Menu, Map")
    print("This game uses a Verb/Noun command system: go out, take knife, etc")
    print("You have 30 minutes to get to safety. Changing locations, and hiding take time so be careful not to take to long.")

def display_time():
    global current_time
    print(f"You look at your phone, its currently {current_time}.")

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
    elif verb == "drop":
        if noun in inventory:
            inventory.remove(noun)
            locations[current_location]["items"].append(noun)
            print(f"You dropped the {noun}.")
        else:
            print(f"You do not have a {noun}.")
    elif verb == "examine":
        if noun in inventory:
            print(f"{items[noun]["examine"]}")
        else:
            print(f"You do not have a {noun}.")
    else:
        print("Invalid command.")

def handle_hide():
    global health
    print(locations[current_location]["hide"])
    if locations[current_location]["hide_result"] == "damage":
        health -= locations[current_location]["damage"]
        print(f"You take {RED}{locations[current_location]["damage"]} damage{NORMAL}")
    elif locations[current_location]["hide_result"] >= 0:
        add_time(locations[current_location]["hide_result"])
        if locations[current_location]["safe"] == False:
            locations[current_location]["safe"] = True

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
                command = input("> ").strip().lower()
                if command == "menu":
                    break
                elif command == "hide":
                    handle_hide()
                elif command == "inventory":
                    display_inventory()
                elif command == "time":
                    display_time()
                elif command == "health":
                    display_health()
                elif command == "map":
                    map()
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

def map():
    # Load the image
    image = cv2.imread(locations[current_location]["map"])

    # Display the image in a window
    cv2.imshow('Current Location', image)

    # Wait for a key press (0 means indefinitely, or specify milliseconds)
    cv2.waitKey(0)

    # Close all OpenCV windows
    cv2.destroyAllWindows()

reset_game()
main_menu()
