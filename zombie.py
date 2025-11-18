"""
Title : Group Project (Zombie Game)
Author: Team Anarchy
Date:
"""

import datetime
import cv2
import json

#Console Styles for print
BOLD = "\033[1m"
NORMAL = "\033[0m"
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'

#Variables and Tables Needed
file_name = "data.txt"
today = datetime.date.today()
locations = "none"
current_location = "none"
previous_location = "none"
inventory = []
health = 0
set_time = 0
current_time = 0
target_time = datetime.datetime.combine(today, datetime.time(17, 30))
items = {
    "backpack":{
        "description": "You see a backpack on the ground.",
        "examine": "It has an army logo on it, you find keys inside",
        "damage": 0
    },
    "knife":{
        "description": "You see a knife.",
        "examine": "A sharp knife, it could be useful.",
        "damage": 40
    },
    "gun":{
        "description": "It's a gun!",
        "examine": "It is a gun, I hope you know how to use it!",
        "damage": 200
    },
}

zombies = {
    "normal":{
        "description": "There is a normal zombie blocking your path!",
        "health": 40,
        "strength": 20
    },
    "big":{
        "description": "There is a big zombie blocking your path!",
        "health": 80,
        "strength": 40
    },
    "giant":{
        "description": "There is a giant zombie blocking your path!",
        "health": 200,
        "strength": 60
    },
    "boss":{
        "description": "There is a wave of giant zombies blocking your path! You should run!",
        "health": 1000,
        "strength": 200
    },
}

def save_game():
    global file_name, health, locations, current_location, inventory, current_time, previous_location
    verify = input("Are you sure you want to Save Game? (Yes or No): ").lower().strip() == "yes"
    if verify:
        #Convert Current Time to JSON acceptable string
        game_time = current_time.isoformat()
        #Converts all the needed data to one dictionary for JSON (easy to read)
        data_to_save = {
            "health": health,
            "current_location": current_location,
            "previous_location": previous_location,
            "current_time": game_time,
            "inventory": inventory,
            "locations": locations,
        }
        # Save the dictionary to a text file
        with open(file_name, "w") as f:
            json.dump(data_to_save, f, indent=4)  # indent for human readability

        print("Data saved successfully")

def load_game():
    global file_name, health, locations, current_location, inventory, current_time, previous_location
    verify = input("Are you sure you want to load game? (Yes or No): ").lower().strip() == "yes"
    if verify:
        # Load the data from the file
        with open(file_name, "r") as f:
            loaded_data = json.load(f)

        # Access your loaded data
        health = loaded_data["health"]
        locations = loaded_data["locations"]
        inventory = loaded_data["inventory"]
        game_time = loaded_data["current_time"]
        current_location = loaded_data["current_location"]
        previous_location = loaded_data["previous_location"]
        #Convert the JSON acceptable string to DateTime format
        saved_time = datetime.datetime.fromisoformat(game_time)
        #Get today's date
        today = datetime.date.today()
        #Replace saved file with today's date in case they saved at another time
        current_time = saved_time.replace(year=today.year, month=today.month, day=today.day)

        print("Data loaded successfully")

#Reset Game (also Normal Mode)
def reset_game():
    global health, locations, current_location, inventory, set_time, current_time, previous_location
    health = 100
    locations = {
        "residence_dining_center": {
            "description": "You hear a loud noise nearby...As you turn your head, you see zombies attacking other students!\nYou go to run towards an exit. At the doors you have the choice to hide or to go out?",
            "exits": {"out": "rdc_hallway", },
            "items": ["knife"],
            "hide": "A zombie scratches you!",
            "hide_result": "damage",
            "map": "rdc.png",
            "safe": True,
            "damage": 20,
            "zombie": ["normal","normal"]
        },
        "rdc_hallway": {
            "description": "Your heart is racing. You must choose to go left towards the Griggs dorms or go right towards Kirby Student Center",
            "exits": {"left": "griggs_hall", "right": "kirby_student_center_floor_3", },
            "items": ["backpack"],
            "hide": "You hide in the bathrooms for 2 mins",
            "hide_result": 120,
            "map": "rdc_hallway.png",
            "safe": False,
            "safe_result": "As you attempt to leave, a zombie scratches you!",
            "damage": 20,
            "zombie": []
        },
        "griggs_hall": {
            "description": "You've entered Griggs Hall. You think you hear a noise...",
            "exits": {"back": "rdc_hallway"},
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "map": "griggs.png",
            "safe": True,
            "zombie": ["giant"]
        },
        "kirby_student_center_floor_3": {
            "description": "You've entered Kirby Student Center floor 3. Behind you is either the RDC, or you can go down the stairs",
            "exits": {"back": "rdc_hallway", "down": "kirby_student_center_floor_2", },
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "map": "ksc.png",
            "safe": True,
            "zombie": []
        },
        "kirby_student_center_floor_2": {
            "description": "You've entered Kirby Student Center floor 2. All the doors are blocked. You can go down or up.",
            "exits": {"up": "kirby_student_center_floor_3", "down": "kirby_student_center_floor_1", },
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "map": "ksc.png",
            "safe": True,
            "zombie": []
        },
        "kirby_student_center_floor_1": {
            "description": "You've entered Kirby Student Center floor 1. The path is blocked besides going forward to the Solon Campus Center stairs",
            "exits": {"up": "kirby_student_center_floor_2", "forward": "scc_stairs"},
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "map": "ksc.png",
            "safe": True,
            "zombie": ["big"]
        },
        "scc_stairs": {
            "description": "You entered Solon Campus Stairs, though you find that most of the path is blocked off. You can leave on Kirby or the 'math' dept",
            "exits": {"kirby": "kirby_student_center_floor_1", "math": "math_department"},
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "map": "solon.png",
            "safe": True,
            "zombie": []
        },
        "math_department": {
            "description": "You entered the Solon Campus Center math department. You can either take the stairs up towards Kirby, or go forward to the wedge ...\nbut you hear some people talking in the Veteran Center... do you want to go in?",
            "exits": {"up": "scc_stairs", "in": "vet_center", "forward": "the_wedge"},
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "map": "math.png",
            "safe": True,
            "zombie": []
        },
        "vet_center": {
            "description": "There is a few other students in here, and they seem prepared... However one guy is looking for his backpack... you can choose to go out",
            "exits": {"out": "math_department"},
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "map": "vet.png",
            "safe": True,
            "zombie": []
        },
        "the_wedge": {
            "description": "The admissions wedge is full of zombies...",
            "exits": {"back": "math_department"},
            "items": [],
            "hide": "Nowhere to hide",
            "hide_result": 0,
            "map": "wedge.png",
            "safe": True,
            "zombie": ["boss"]
        }
    }
    current_location = "residence_dining_center"
    previous_location = "residence_dining_center"
    inventory = []
    set_time = datetime.time(17, 0, 0)
    current_time = datetime.datetime.combine(today, set_time)
    game_time = current_time.isoformat()
    # Converts all the needed data to one dictionary for JSON (easy to read)
    data_to_save = {
        "health": health,
        "current_location": current_location,
        "previous_location": previous_location,
        "current_time": game_time,
        "inventory": inventory,
        "locations": locations,
    }
    try:
        with open(file_name, 'x') as f:
            json.dump(data_to_save, f, indent=4)  # indent for human readability
        print("")
    except FileExistsError:
        print("")

#add time to current time
def add_time(time):
    global current_time
    current_time += datetime.timedelta(seconds=time)

#displays your current health to player
def display_health():
    global health
    print(f"Your current health: {BLUE}{health}{NORMAL}")

#displays current inventory to player
def display_inventory():
    if inventory:
        print("Your inventory:", ", ".join(inventory))
    else:
        print("Your inventory is empty.")

#displays location information for player
def display_location():
    print(f"You are currently in {current_location.replace("_"," ").title()}")
    print(locations[current_location]["description"])
    if locations[current_location]["items"]:
        items_in_location = locations[current_location]["items"]
        for item_name in items_in_location:
            print(items[item_name]["description"])
    if locations[current_location]["safe"] == False:
        print("There are zombies nearby, though you think you can get around them without fighting.")
    if locations[current_location]["zombie"]:
        zombies_in_location = locations[current_location]["zombie"]
        for zombie_name in zombies_in_location:
            print(f"{zombies[zombie_name]["description"]} Run or Fight")

#displays menu
def display_menu():
    print("\n--- Main Menu ---")
    print("1. Instructions")
    print("2. Play Game")
    print("3. Save the Game")
    print("4. Load the Game")
    print("5. Exit")

#displays rules
def display_instructions():
    print("Commands: Go, Fight, Take, Inventory, Drop, Hide, Time, Health, Examine, Run, Menu, Map")
    print("This game uses a Verb/Noun command system: go out, take knife, use knife, etc...")
    print("You have 30 minutes to get to safety. Changing locations, and hiding takes time so be careful not to take to long.")

#displays time to player
def display_time():
    global current_time
    print(f"You look at your phone, its currently {current_time}.")

#fight function for fighting zombies
def fight():
    global health, current_location, current_time

    # checks if location has a zombie
    if locations[current_location]["zombie"]:
        zombies_in_location = locations[current_location]["zombie"]

        #loop for zombies in location
        for zombie_name in zombies_in_location:
            zombie_health=zombies[zombie_name]["health"]
            damage=zombies[zombie_name]["strength"]

            #loops while zombie has health
            while zombie_health > 0:
                print("use fists")

                #prints commands for each item in inventory
                for item_name in inventory:
                    print(f"use {item_name}")

                fight = input("> ").lower().split()
                item = " ".join(fight[1:]) if len(fight) > 1 else ""

                #Fight with fists
                if item == "fists":
                    add_time(30)
                    zombie_health -= 20
                    print(f"You hit the {zombie_name} zombie for {BLUE}20 Damage{NORMAL}")
                    #check if zombie alive
                    if zombie_health > 0:
                        #have zombie do damage to you
                        health -= damage
                        print(f"The {zombie_name} zombie scratched you doing {RED}{damage} Damage{NORMAL}")
                        #check if you are still alive
                        if health <= 0:
                            #you died game over, reset and show menu
                            print(f"{RED}You died, GAME OVER{NORMAL}")
                            reset_game()
                            main_menu()
                    #zombie died
                    else:
                        locations[current_location]["zombie"].remove(zombie_name)
                        print(f"You defeated the {zombie_name} zombie")

                #fight with items in inventory
                elif item in inventory:
                    add_time(30)
                    zombie_health -= items[item]["damage"]
                    print(f"You hit the {zombie_name} zombie for {BLUE}{items[item]["damage"]} Damage{NORMAL}")
                    # check if zombie alive
                    if zombie_health > 0:
                        health -= damage
                        print(f"The {zombie_name} zombie scratched you doing {RED}{damage} Damage{NORMAL}")
                        #check if you are still alive
                        if health <= 0:
                            # you died game over, reset and show menu
                            print(f"{RED}You died, GAME OVER{NORMAL}")
                            reset_game()
                            main_menu()
                    #zombie died
                    else:
                        #remove zombie from location
                        locations[current_location]["zombie"].remove(zombie_name)
                        print(f"You defeated the {zombie_name} zombie")

                #Command not recognized or item not in inventory
                else:
                    print("Invalid command.")

def handle_command(command):
    global current_location, inventory, current_time, health, previous_location
    parts = command.lower().split()
    verb = parts[0]
    noun = " ".join(parts[1:]) if len(parts) > 1 else ""
    #change locations with go command
    if verb == "go":
        #check if zombie is in the way
        if locations[current_location]["zombie"]:
            zombies_in_location = locations[current_location]["zombie"]
            #display zombies blocking path
            for zombie_name in zombies_in_location:
                print(zombies[zombie_name]["description"], "\nYou cannot leave")
        #check to see that current location has that exit
        elif noun in locations[current_location]["exits"]:
            #check if location is unsafe, if not do damage
            if locations[current_location]["safe"] == False:
                print(f"{locations[current_location]["safe_result"]}, you take {RED}{locations[current_location]["damage"]} damage{NORMAL}")
                health -= locations[current_location]["damage"]

            previous_location = current_location
            current_location = locations[current_location]["exits"][noun]
            add_time(30)
        #Current location doesnt have that exit
        else:
            print("You can't go that way.")
    #Take items
    elif verb == "take":
        #check if location has that item
        if noun in locations[current_location]["items"]:
            #add to inventory
            inventory.append(noun)
            #remove from location
            locations[current_location]["items"].remove(noun)
            print(f"You took the {noun}.")
        #location does not have item
        else:
            print(f"There is no {noun} here.")
    #drop items
    elif verb == "drop":
        #check if item is in inventory
        if noun in inventory:
            #remove item from inventory
            inventory.remove(noun)
            #add item to location
            locations[current_location]["items"].append(noun)
            print(f"You dropped the {noun}.")
        #you do not have item
        else:
            print(f"You do not have a {noun}.")
    #examine items
    elif verb == "examine":
        #check if you have item
        if noun in inventory:
            print(f"{items[noun]["examine"]}")
        #you do not have item
        else:
            print(f"You do not have a {noun}.")
    #Run
    elif verb == "run":
        get_previous_location = current_location
        current_location = previous_location
        previous_location = get_previous_location
        add_time(30)
    #command wasn't recognized
    else:
        print("Invalid command.")
#function for hide command
def handle_hide():
    global health
    print(locations[current_location]["hide"])
    #location damages you for hiding
    if locations[current_location]["hide_result"] == "damage":
        add_time(30)
        health -= locations[current_location]["damage"]
        print(f"You take {RED}{locations[current_location]["damage"]} damage{NORMAL}")
    #location adds time and makes location safe
    elif locations[current_location]["hide_result"] >= 0:
        add_time(locations[current_location]["hide_result"])
        if locations[current_location]["safe"] == False:
            locations[current_location]["safe"] = True

def main_menu():
    global health, current_time
    #main menu loop
    while True:
        #display menu
        display_menu()
        choice = input("Enter your choice (1-6): ")
        #display rules
        if choice == '1':
            display_instructions()
        #play game
        elif choice == '2':
            while True:
                #prints location information
                display_location()
                #Handle Game Commands
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
                elif command == "fight":
                    fight()
                else:
                    handle_command(command)
                #died
                if health == 0:
                    print(f"You died\n{RED}Game Over!{NORMAL}")
                    reset_game()
                    break
                #took too long to get to safety
                if current_time >= target_time:
                    print(f"The zombies have overrun the school.\n{RED}Game Over!{NORMAL}")
                    reset_game()
                    break
        elif choice == '3':
            save_game()
        elif choice == '4':
            load_game()
        #exit program
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        #invalid choice
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def map():
    # Load the image
    image = cv2.imread(locations[current_location]["map"])
    # Display the image in a window
    cv2.imshow('Current Location', image)
    # Wait for a key press (0 means indefinitely, or specify milliseconds)
    cv2.waitKey(0)
    # Close all OpenCV windows
    cv2.destroyAllWindows()

#resets all game variables/tables/tuples/arrays and starts main menu loop
reset_game()
main_menu()
