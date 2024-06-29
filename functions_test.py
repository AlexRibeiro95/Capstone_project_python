import time
import threading
from datetime import datetime

def linebreak():
    """
    Print 2 new empty line break
    """
    print("\n\n")

def start_game(game_state, object_relations):

    """
    Start the game by:
    - Asking for the player's name.
    - Welcoming the player to the game.
    - Providing an initial description of the game scenario.
    - Asking for the first room interaction.
    """

    player_name = input("What is your name?\n").strip()
    global start_time
    print("Welcome to the game", player_name, "!")

    print("\033[91mYou wake up on a couch and find yourself in a strange house with no windows which you have never been to before.")
    print("You don't know what happened but you feel that something dangerous is approaching and you must get out of the house.")
    print("Try to find something that might help you leave the house, and FAST!\033[0m")
    linebreak()
    play_room(game_state["current_room"], game_state, object_relations)

def play_room(room, game_state, object_relations):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        linebreak()
        print("Congrats! You escaped are now FREE!")
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'inspect'?\n").strip()
        if intended_action == "explore":
            explore_room(room, object_relations)
            play_room(room, game_state, object_relations)
        elif intended_action == "inspect":
            inspect_item(input("What would you like to inspect?").strip(), object_relations, game_state)
        else:
            print("Not sure what you mean. Type 'explore' or 'inspect'.")
            play_room(room, game_state, object_relations)
        linebreak()

def explore_room(room, object_relations):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [f"*\033[1m{i['name']}\033[0m*" for i in object_relations[room["name"]]]
    print(" ")
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room, object_relations):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    next_room = [room for room in connected_rooms if current_room != room]
    return next_room[0]





def inspect_item(item_name, object_relations, game_state):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You inspect " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "\033[You unlock it with a key you have.\033[0m"
                    next_room = get_next_room_of_door(item, current_room, object_relations)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "\033[92mYou find " + item_found["name"] + ".\033[0m"
                else:
                    output += "\033[91mThere isn't anything interesting about it.\033[0m"
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        linebreak()
        play_room(next_room, game_state, object_relations)
    else:
        play_room(current_room,game_state, object_relations)

def countdown_timer(duration):
    global timer_thread_running
    timer_thread_running = True
    while duration > 0 and timer_thread_running:
        mins, secs = divmod(duration, 60)
        timer_display = f'{mins:02d}:{secs:02d}'
        print(f"\rTime left: {timer_display}", end="")
        time.sleep(1)
        duration -= 1
    if timer_thread_running:
        print("\nTime's up! You couldn't escape in time.")
        exit()

def display_remaining_time(start_time, TIMER_DURATION):
    elapsed_time = (datetime.now() - start_time).total_seconds()
    remaining_time = max(0, TIMER_DURATION - int(elapsed_time))
    mins, secs = divmod(remaining_time, 60)
    timer_display = f'{mins:02d}:{secs:02d}'
    print(f"Time left: {timer_display}")