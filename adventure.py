import sys
import game_inventory
import time

player = {
    'room': 'outside',
    'inventory': {"strawberry cake": 1}
}

rooms = {
    "outside": {
        "title": "Outside",
        "description": "You are standing outside of a huge cave entrance. You can feel the warm, vibrating air coming from it.",
        "exits": {
            "north": {
                "to_room": "cave", 
                "unlocked": True
            }
        },
        "items":{
            "sword": 1,
            "some useless herbs": 1
        } 
    },
    "cave": {
        "title": "Cave",
        "description": "You're in a dark, dusty cave. The weird smell seems to be announcing something disturbing",
        "exits": {
            "east": {
                "to_room": "treasury", 
                "unlocked": True
            },
            "west": {
                "to_room": "burial ground", 
                "unlocked": True
            },
            "south": {
                "to_room": "outside", 
                "unlocked": True
            }
        }
    },
    "burial ground": {
        "title": "Burial ground",
        "description": "The small stream of sunlight coming from the hole in the ceiling reveals a pile of dead bodies laying on the floor." 
                       "\nSmell is unbearable. It's the last place on earth you want to be.",
        "exits": {   
            "east": {
                "to_room": "cave", 
                "unlocked": True
            }
        },
        "items": {
            "mysterious key": 1,
            "bones": 1
        }
    },
    "treasury": {
        "title": "Treasury",
        "description": "You see a huge pile of shiny gold in the center of the room. "
                       "There is also a dragon sleeping on the top of it.",
        "exits": {
            "north": {
                "to_room": "secret exit", 
                "unlocked": False,
                "item_to_unlock": "mysterious key"
            },
            "west": {
                "to_room": "cave", 
                "unlocked": True
            }
        },
        "items": {
            "gold": 3
        },
        "npc": "dragon"
    },
    "secret exit": {
        "title": "Secret Exit",
        "description": "You leave the dungeon and win the game!"
    }
}

command_list = [('look', 'l', 'look around'),
                ('quit', 'q', 'quit'),
                ('north', 'n', 'go north'),
                ('south', 's', 'go south'),
                ('east', 'e', 'go east'),
                ('west', 'w', 'go west'),
                ('inventory', 'i', 'view your items'),
                ('search', 'se', 'search the room'),
                ('get', 'g', 'pick up the item')]


def get_correct_direction(command):
    abbreviated_directions = ["n", "s", "e", "w"]
    directions = ["north", "south", "east", "west"]
    if command in abbreviated_directions:
        command = directions[abbreviated_directions.index(command)]
    return command


def main():
    print("Type \"help\" for a list of command")
    describe_room()
    playing = True
    while playing:
        command = get_command()
        if command in ['look', 'l']:
            describe_room()
        elif command in ['north', 'south', 'east', 'west', 'n', 's', 'w', 'e']:
            command = get_correct_direction(command)
            if command in rooms[player['room']]["exits"]:
                move(command)
                check_if_won()
                describe_room()
            else:
                print("There is no such exit.")
        elif command in ['help', 'h']:
            display_help()
        elif command in ['inventory', 'i']:
            display_inventory()
        elif command in ['search', 'se']:
            search()
        elif command in ['get', 'g']:
            get_item()
        elif command in ['talk', 't']:
            chit_chat()
        elif command in ['quit', 'q']:
            print('Bye!')
            playing = False
        else:
            print(f'Unrecognized command: {command}')


def check_if_won():
    if player['room'] == "secret exit":
        print("YOU WON! CONGRATULATIONS!")
        sys.exit(0)


def get_command():
    print()
    return input('> ')


def print_directions():
    room = rooms[player['room']]
    for direction in room["exits"]:
        next_room = room["exits"][direction]["to_room"]
        print("There are following exits: " + direction + " -> " + next_room.capitalize())


def describe_room():
    room = rooms[player['room']]
    print()
    print(room['title'])
    print()
    print(room['description'])
    print()
    print_directions()


def move(command):
    current_room = player["room"]
    chosen_exit = rooms[current_room]["exits"][command]
    if chosen_exit["unlocked"]:
        player["room"] = chosen_exit["to_room"]
    elif chosen_exit["item_to_unlock"] not in player['inventory']:
        print("The gate is closed. You need to find a key to open it.")
    else:
        player["room"] = chosen_exit["to_room"]


def display_help():
    print("The main goal of the game is to safely leave the dungeon with gold.")
    for command in command_list:
        print("Press \"{}\", or type \"{}\" to {}.".format(command[1], command[0], command[2]))


def display_inventory():
    game_inventory.print_table(player['inventory'])


def search():
    current_room = player["room"]
    if 'items' in rooms[current_room]:
        items_in_room = show_items_in_room(current_room)
        items_str = ' and '.join(items_in_room)
        print("You find {}.".format(items_str))
    else:
        print("There's nothing here.")


def show_items_in_room(current_room):
    items_in_room = []
    for item in rooms[current_room]["items"]:
        for i in range(rooms[current_room]["items"][item]):
            items_in_room.append(item)
    return items_in_room


def get_item():
    current_room = player["room"]
    if "items" in rooms[current_room]:
        items_to_get = []
        for item in rooms[current_room]["items"]:
            for i in range(rooms[current_room]["items"][item]):
                items_to_get.append(item)
        game_inventory.add_to_inventory(player['inventory'], items_to_get)
        del rooms[current_room]["items"]
        print("You picked up all the items in the room.")
    else:
        print("There's nothing here. Duh...")


def chit_chat():
    if 'npc' in rooms[player['room']]:
        if rooms[player['room']]['npc'] == 'dragon':
            chit_chat_with_dragon()
    else:
        print("There is no one to talk to in this room.")


def chit_chat_with_dragon():
    print('Dragon whispers: "How dare you wake me up from my slumber?"')
    print("Type '1' if your response is: 'I want your gold, give it to me.' "
          "\nType '2' if your response is: 'I have something valuable, too. Let's trade.'"
          "\nType '3' if yur response is: 'Shut up and fight me, you disgusting beast!'")
    answer = input('> ')
    if answer == "1":
        print('Dragon says: "I will kill you weakling"')
        fight()
        del rooms[player['room']]['npc']
    elif answer == "2":
        print('Dragon says: "I doubt that you posess anything worth ')
        time.sleep(1)
        print('You say: "I have a cake my nana made for me before I left. I bet you\'ve never eaten anything like this."')
        time.sleep(2)
        print('Dragon says: "Hmmmmmmmm... I accept your offer. Take as much gold as you can carry.')
        time.sleep(1)
        game_inventory.remove_from_inventory(player['inventory'], ['strawberry cake'])
        items = ' and '.join(rooms[player['room']]['items'].keys())
        print("You have traded with the dragon and obtained {}.".format(items))
        game_inventory.add_to_inventory(player['inventory'], rooms[player['room']]['items'].keys())
    elif answer == "3":
        fight()
    else:
        print("Chose a valid answer to the dragon.")


def fight():
    if 'sword' in player['inventory']:
        time.sleep(1)
        print("***battle noises***")
        time.sleep(1)
        print("***more battle noises***")
        time.sleep(2)
        print("You have slayed the dragon.")
        rooms[player['room']]['description'] = "You see a pile of shiny gold in the center of the room. There is also a dead dragon on the top of it."
    else:
        time.sleep(1)
        print("What do you think happens when unarmed man provokes a deadly beast?")
        time.sleep(1)
        print("You guessed it. The dragon used his fire breath and burned you dead.")
        time.sleep(1)
        print("GAME OVER")
        sys.exit()


if __name__ == '__main__':
    main()
