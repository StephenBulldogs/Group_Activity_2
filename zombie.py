"""
Title : Group Project (Zombie Game)
Author: Team Anarchy
Date:
"""

# Define location
locations = "none"
# Player's current location and inventory
current_location = "none"
inventory = []
health = 100

def reset_game():
    global health, locations, current_location, inventory
    health = 100
    locations = {
        "residence_dining_center": {
            "description": "You are in the RDC. You hear a loud noise. turning your head you see what you can only describe as zombies attacking others.\nYou run to the exit, you stop at the doors you can choose to hide or go out?",
            "exits": {"out": "rdc_hallway", },
            "items": [],
            "item_desc": "",
            "hide": "a zombie bites you!",
            "hide_result": "die",
        },
        "rdc_hallway": {
            "description": "You're heart racing you must choose go left towards the dorms or go right towards kirby student center",
            "exits": {"left": "griggs_hall", "right": "kirby_student_center_floor_3", },
            "items": ["backpack"],
            "item_desc": "On the ground you see a",
            "hide": "You hide in the bathrooms for 5 mins",
            "hide_result": "nothing",

        },
        "griggs_hall": {
            "description": "You entered griggs hall.",
            "exits": {"back": "rdc_hallway"},
            "items": [],
            "item_desc": "",
            "hide": "Nowhere to hide",
            "hide_result": "nothing",
        },
        "kirby_student_center_floor_3": {
            "description": "You entered kirby student center floor 3.",
            "exits": {"back": "rdc_hallway", "down": "kirby_student_center_floor_2", },
            "items": [],
            "item_desc": "",
            "hide": "Nowhere to hide",
            "hide_result": "nothing",
        },
        "kirby_student_center_floor_2": {
            "description": "You entered kirby student center floor 2.",
            "exits": {"up": "kirby_student_center_floor_3", },
            "items": [],
            "item_desc": "",
            "hide": "Nowhere to hide",
            "hide_result": "nothing",
        }
    }
    current_location = "residence_dining_center"
    inventory = []


def display_menu():
    print("\n--- Main Menu ---")
    print("1. Display Rules")
    print("2. Play Game")
    print("3. Exit")

def display_rules():
    print("Commands: Go, Take, Inventory, Use, Attack, Hide, Menu")

def display_location():
    print(locations[current_location]["description"])
    if locations[current_location]["items"]:
        print(locations[current_location]["item_desc"], ", ".join(locations[current_location]["items"]))

def handle_command(command):
    global current_location, inventory
    parts = command.lower().split()
    verb = parts[0]
    noun = " ".join(parts[1:]) if len(parts) > 1 else ""

    if verb == "go":
        if noun in locations[current_location]["exits"]:
            current_location = locations[current_location]["exits"][noun]
        else:
            print("You can't go that way.")
    elif verb == "take":
        if noun in locations[current_location]["items"]:
            inventory.append(noun)
            locations[current_location]["items"].remove(noun)
            print(f"You took the {noun}.")
        else:
            print(f"There is no {noun} here.")
    else:
        print("Invalid command.")

def main_menu():
    global health
    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            display_rules()
        elif choice == '2':
            # Game loop2
            while True:
                print(f"Current Health: {health}")
                display_location()
                command = input("> ").strip()
                if command == "menu":
                    break
                elif command == "hide":
                    print(locations[current_location]["hide"])
                    if locations[current_location]["hide_result"] == "die":
                        health = 0
                    else:
                        continue
                elif command == "inventory":
                    if inventory:
                        print("Your inventory:", ", ".join(inventory))
                    else:
                        print("Your inventory is empty.")
                else:
                    handle_command(command)
                if health == 0:
                    print("You Died\nGame Over!")
                    reset_game()
                    break
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")


#Starts everything
reset_game()
main_menu()
