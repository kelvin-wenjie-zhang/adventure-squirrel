#
# main()
# PrintHeader()
# PrintText()
# ShowMenu()
# GetInput()
# AskWithConfirm()
# Ask(()

import curses
import useful
import Story
import pickle
import time

MENU_TOP = ["CREATE a new game", "EDIT a saved game", 
            "EXIT this program"]

MENU_WRITE_GAME = ["GAME", "ROOMS", "ITEMS", "SAVE STORY FILE", 
                  "SAVE AND EXIT", "EXIT WITHOUT SAVING"]

MENU_EDIT_GAME = ["CHANGE NAME", "WRITE HELP", "WRITE CREDITS", "BACK"]

MENU_ROOMS = ["ADD Room", "EDIT Room", "REMOVE Room", "BACK"]

MENU_ITEMS = ["ADD Item", "EDIT Item", "REMOVE Item", "BACK"]

MENU_EDIT_ITEM = ["NAME", "DESCRIPTION", "INVENTORY BEHAVIOR",
             "AVAILABLE ACTIONS", "BACK"]

MENU_CONFIRM = ["YES", "NO"]


def main(screen):

    # Initialize curses
    screen = curses.initscr()
    curses.curs_set(False) # Removes blinking cursor

    screen.clear()

    header = "Adventure Squirrel"

    # TOP MENU #     
    screen = PrintHeader(header, screen, 0, 0) 
    screen = PrintText("A text-based adventure game engine", screen, 4, 0)   
    selection = ShowMenu(MENU_TOP, screen, 6, 0)
    # End TOP MENU #
    
    # BEGIN Create a new game #
    if selection[0] == MENU_TOP[0]:
        screen.clear()
        
        # Initialize the Game
        GAME = Story.GameStory()
        
        # Ask for the name of the game
        question = "What is the name of your game?"
        GAME.name = AskWithConfirm(header, question, screen)

        WriteGame(GAME, screen)
    # END Create a new game#

    # BEGIN EDIT a saved game #
    elif selection[0] == MENU_TOP[1]:
        screen.clear()
       
        question = "What is name of the pickle file that contains the game information? (e.g. \"Game_Info.pickle\")"
        # Ask for the name of the pickle file
        while True:
            filename = Ask(header, question, screen)
            GAME = LoadStory(filename)
            if GAME == -1:
                question = "The file '" + filename + "' was not found. Try again."
            else: 
                break 
        WriteGame(GAME, screen)
    # END EDIT a saved game #                 

    # BEGIN EXIT THIS PROGRAM #
    else:
        screen.clear()
        screen = PrintHeader(header, screen, 0, 0)
        screen = PrintText("It was good to have you around!", screen, 4, 0)
        screen.refresh()
        time.sleep(2)
    # END EXIT this program#
    curses.endwin()

def WriteGame(GAME, screen):
    while True:
        screen.clear()
        # WRITE GAME MENU # 
        header = GAME.name
        screen = PrintHeader(header, screen, 0, 0) 
        screen = PrintText("What do you want do edit?", screen, 4, 0)   
        selection = ShowMenu(MENU_WRITE_GAME, screen, 6, 0)
        # END WRITE GAME MENU #

        # GAME #
        if selection[0] == MENU_WRITE_GAME[0]:
            EditGame(GAME, screen)
        # END GAME #        

        # ROOMS #
        if selection[0] == MENU_WRITE_GAME[1]:
            WriteRooms(GAME, screen)
        # END ROOMS #

        # ITEMS #
        if selection[0] == MENU_WRITE_GAME[2]:
            WriteItems(GAME, screen)
        # END ITEMS #
        
        # SAVE STORY FILE #
        if selection[0] == MENU_WRITE_GAME[3]:
            SaveStory(GAME, screen)
        # END SAVE STORY FILE #

        # SAVE AND EXIT #
        if selection[0] == MENU_WRITE_GAME[4]:
            SaveStory(GAME, screen)
            break
        # END SAVE AND EXIT #

        # EXIT WITHOUT SAVING #
        if selection[0] == MENU_WRITE_GAME[5]:
            break
        # END EXIT WITHOUT SAVING #

def EditGame(GAME, screen):
    while True: 
        screen.clear()

        # GAME MENU #
        header = GAME.name
        screen = PrintHeader(header, screen, 0, 0)
        screen = PrintText("What do you want to do?", screen, 4, 0)
        selection = ShowMenu(MENU_EDIT_GAME, screen, 6, 0)
        # END GAME MENU #

        # CHANGE NAME #
        if selection[0] == MENU_EDIT_GAME[0]:
            screen.clear()
            question = "What is the new name of your game?"
            GAME.name = AskWithConfirm(header, question, screen)
        # END CHANGE NAME #

        # WRITE HELP #
        if selection[0] == MENU_EDIT_GAME[1]:
            question = "Write the HELP information."
            GAME.instructions = AskWithConfirm(header, question, screen)
        # END WRITE HELP "
        
        # WRITE CREDITS #
        if selection[0] == MENU_EDIT_GAME[2]:
            question = "Write the CREDITS."
            GAME.credits = AskWithConfirm(header, question, screen)
        # END WRITE CREDITS "

        # BACK #
        if selection[0] == MENU_EDIT_GAME[3]:
            break
        # END BACK #
        

def WriteRooms(GAME, screen):
    while True:
        screen.clear()

        # ROOMS MENU #
        header = GAME.name
        screen = PrintHeader(header, screen, 0, 0)
        screen = PrintText("What do you want to do?", screen, 4, 0)
        selection = ShowMenu(MENU_ROOMS, screen, 6, 0)
        # END ROOMS MENU #

        # ADD ROOM #
        if selection[0] == MENU_ROOMS[0]:
            AddRoom(GAME, screen)
        # END ADD ROOM #

        # EDIT ROOM #
        if selection[0] == MENU_ROOMS[1]:
            EditRoom(GAME, screen)
        # END EDIT ROOM "
        
        # REMOVE ROOM #
        if selection[0] == MENU_ROOMS[2]:
            RemoveRoom(GAME, screen)
        # END REMOVE ROOM "

        # BACK #
        if selection[0] == MENU_ROOMS[3]:
            break
        # END BACK #

def AddRoom(GAME, screen): 
    screen.clear()

    # Get the name of the room
    header = GAME.name
    question = "What is the name of this room?"
    name = AskWithConfirm(header, question, screen)

    Room = Story.RoomStory()
    Room.name = name
    GAME.rooms.append(Room)

def EditRoom(GAME, screen): 
    while True:
        screen.clear()

        # Chose Room to Edit
        header = GAME.name
        question = "Which room would you like to edit?"
        screen = PrintHeader(header, screen, 0, 0)
        screen = PrintText(question, screen, 4, 0)
        
        RoomMenu = [(r.name) for r in GAME.rooms]
        RoomMenu.append("BACK")
        selection = ShowMenu(RoomMenu, screen, 6, 0)
    
        if selection[0] == "BACK":
            break

        else:
            GAME.editRoom(selection[0])

def RemoveRoom(GAME, screen):
    while True:
        screen.clear()

        # Chose Room to Remove
        header = GAME.name
        question = "Which room would you like to remove?"
        screen = PrintHeader(header, screen, 0, 0)
        screen = PrintText(question, screen, 4, 0)
        
        RoomMenu = [(r.name) for r in GAME.rooms]
        RoomMenu.append("BACK")
        selection = ShowMenu(RoomMenu, screen, 6, 0)
     
        if selection[0] == "BACK":
            break

        else:            
            screen.clear()
            
            header = GAME.name
            question = "Are you sure you want to REMOVE " + selection[0] + "?"
            screen = PrintHeader(header, screen, 0, 0)
            screen = PrintText(question, screen, 4, 0)
            if ShowMenu(MENU_CONFIRM, screen, 6, 0)[0] == "YES":
                del GAME.rooms[selection[1]]
  
def WriteItems(GAME, screen):
    while True:    
        screen.clear()

        # ITEMS MENU #
        header = GAME.name
        screen = PrintHeader(header, screen, 0, 0)
        screen = PrintText("What do you want to do?", screen, 4, 0)
        selection = ShowMenu(MENU_ITEMS, screen, 6, 0)
        # END ITEMS MENU #
    
        # ADD ITEM #
        if selection[0] == MENU_ITEMS[0]:
            AddItem(GAME, screen)
        # END ADD ITEM #

        # EDIT ITEM #
        elif selection[0] == MENU_ITEMS[1]:
            EditItem(GAME, screen)
        # END EDIT ITEM "
        
        # REMOVE ITEM #
        elif selection[0] == MENU_ITEMS[2]:
            RemoveItem(GAME, screen)
        # END REMOVE ITEM "

        # BACK #
        elif selection[0] == MENU_ITEMS[3]:
            break
        # END BACK #

def AddItem(GAME, screen):

        # Ask for the name of the item
        screen.clear()
        header = GAME.name
        question = "What is the name of this item?"
        name = AskWithConfirm(header, question, screen)

        # Ask for the description of the item
        screen.clear()
        header = name
        question = "What is the description of this item?"
        description = AskWithConfirm(header, question, screen)

        # Pickable?
        screen.clear()
        question = "Can the user pick this item up?";
        screen = PrintHeader(header, screen, 0, 0)
        screen = PrintText(question, screen, 4, 0)
        if ShowMenu(MENU_CONFIRM, screen, 6, 0)[0] == "YES":
            isPickable = True
 
            # Droppable? 
            screen.clear()
            question = "Can the user drop this item from his inventory?";
            screen = PrintHeader(header, screen, 0, 0)
            screen = PrintText(question, screen, 4, 0)
            if ShowMenu(MENU_CONFIRM, screen, 6, 0)[0] == "YES":
                isDroppable = True
            else: 
                isDroppable = False
        else:
            isPickable = False
            isDroppable = False

        newItem = Story.ItemStory(name, description, isPickable, isDroppable)
        GAME.items.append(newItem)
        
         

def EditItem(GAME, screen):
        while True:
            screen.clear()
            # Chose Item to Edit
            header = GAME.name
            question = "Which item would you like to edit?"
            screen = PrintHeader(header, screen, 0, 0)
            screen = PrintText(question, screen, 4, 0)
            
            ItemMenu = [(i.name) for i in GAME.items]
            ItemMenu.append("BACK")
            itemselection = ShowMenu(ItemMenu, screen, 6, 0)
        
            if itemselection[0] == "BACK":
                break

            else:
            
                while True:
                    screen.clear()
                    item = GAME.items[itemselection[1]]
                    header = item.name
                    name = "Name: " + item.name
                    description = "Description: " + item.description
                    pickable = "Is Pickable: " + str(item.isPickable)
                    droppable = "Is Droppable: " + str(item.isDroppable)
                     
                    screen = PrintHeader(header, screen, 0, 0)
                    screen = PrintText(name, screen, 4, 0)
                    screen = PrintText(description, screen, 5, 0)
                    screen = PrintText(pickable, screen, 6, 0)
                    screen = PrintText(droppable, screen, 7, 0)
                    question = "What would you like to change??"            
                    screen = PrintText(question, screen, 9, 0)
                    
                    selection = ShowMenu(MENU_EDIT_ITEM, screen, 11, 0)

                    # EDIT NAME #
                    if selection[0] == MENU_EDIT_ITEM[0]:
                        screen.clear()
                        question = "What is the new name of this item?"
                        name = AskWithConfirm(header, question, screen)
                        GAME.items[itemselection[1]].name = name
                        header = name                
                    # END EDIT NAME #

                    # EDIT DESCRIPTION #
                    elif selection[0] == MENU_EDIT_ITEM[1]:
                        screen.clear()
                        question = "What is the new description of this item?"
                        description = AskWithConfirm(header, question, screen)
                        GAME.items[itemselection[1]].description = description                    
                    # END EDIT DESCRIPTION #

                    # INVENTORY BEHAVIOR #
                    elif selection[0] == MENU_EDIT_ITEM[2]:
                        # Pickable?
                        screen.clear()
                        question = "Can the user pick this item up?";
                        screen = PrintHeader(header, screen, 0, 0)
                        screen = PrintText(question, screen, 4, 0)
                        if ShowMenu(MENU_CONFIRM, screen, 6, 0)[0] == "YES":
                            isPickable = True
                 
                            # Droppable? 
                            screen.clear()
                            question = "Can the user drop this item from his inventory?";
                            screen = PrintHeader(header, screen, 0, 0)
                            screen = PrintText(question, screen, 4, 0)
                            if ShowMenu(MENU_CONFIRM, screen, 6, 0)[0] == "YES":
                                isDroppable = True
                            else: 
                                isDroppable = False
                        else:
                            isPickable = False
                            isDroppable = False
                        GAME.items[itemselection[1]].isPickable = isPickable
                        GAME.items[itemselection[1]].isDroppable = isDroppable
                            
                    # END INVENTORY BEHAVIOR #
           
                    # AVAILABLE ACTIONS # 
                    elif selection[0] == MENU_EDIT_ITEM[3]:
                        print("NOT YET IMPLEMENTED")
                    # END AVAILABLE ACTIONS

                    elif selection[0] == MENU_EDIT_ITEM[4]:
                        break
            
def RemoveItem(GAME, screen):
    while True:
        screen.clear()

        # Chose Item to Remove
        header = GAME.name
        question = "Which item would you like to remove?"
        screen = PrintHeader(header, screen, 0, 0)
        screen = PrintText(question, screen, 4, 0)
        
        ItemMenu = [(i.name) for i in GAME.items]
        ItemMenu.append("BACK")
        selection = ShowMenu(ItemMenu, screen, 6, 0)
     
        if selection[0] == "BACK":
            break

        else:            
            screen.clear()
            
            header = GAME.name
            question = "Are you sure you want to REMOVE " + selection[0] + "?"
            screen = PrintHeader(header, screen, 0, 0)
            screen = PrintText(question, screen, 4, 0)
            if ShowMenu(MENU_CONFIRM, screen, 6, 0)[0] == "YES":
                del GAME.items[selection[1]]
    
# Save pickle Story File
def SaveStory(GAME, screen):
        screen.clear()
        header = "Adventure Squirrel"
        question = "What will be the name of the pickle file that contains the game information? (e.g. \"Game_Info.pickle\")"
        while True:
            filename = Ask(header, question, screen) 
            if filename.endswith(".pickle"):
                break
            else:
                question = "The file must be a pickle file."

        with open(filename,'wb') as f:
            pickle.dump(GAME, f)

        print("\nThe game has been saved.")
        time.sleep(2)

# Loads a story file and returns a game or -1 in case of file not found
def LoadStory(filename):
    try:
        with open(filename,'rb') as f:
            GAME = pickle.load(f)
            return GAME

    except FileNotFoundError:
        return -1
    

# Function that prints the header in the given coordinates
# nice header messages all around
def PrintHeader(header_msg, screen, line, col):
    length = len(header_msg)\

    # First line of the header
    header1 = "/--"
    for i in range(length):
        header1 += "-"
    header1 += "--\\"
    screen.addstr(line, col, header1)
    
    # Second line of the header
    header2 = "|  " + header_msg + "  |"
    screen.addstr(line+1, col, header2)

    # Third line of the header    
    header3 = "\\--"
    for i in range(length):
        header3 += "-"
    header3 += "--/"
    screen.addstr(line+2, col, header3)

    return screen

def PrintText(text, screen, line, col):
    text = useful.formatLinebreak(text)
    screen.addstr(line, col, text)
    return screen

# Function That turns on Echo for getting input
def GetInput(screen, line, col):
    curses.echo(True)
    curses.curs_set(True)
    text = screen.getstr(line, col).decode(encoding="utf-8")
    curses.echo(False)
    curses.curs_set(False)
    return text


#This is a function that creates a menu for easier selection of options
#and returns the highlighted item. 
def ShowMenu(menu, screen, lin, col):
    
    #Checks if there is at least one eelement in the list.
    if len(menu) == 0 :
        return -1

    #Cursor position is an integer initially at the first element
    cursor = 0; 

    #This is the loop that prints the menu
    while True:
        current = 0;
        for item in menu:
            if cursor == current:
                screen.addstr(lin+current, col, '> ' + item)
            else:
                screen.addstr(lin+current, col, item + "  ")
            current += 1    
 
        key = screen.getch()
        if key == curses.KEY_UP:
            cursor = cursor-1 if cursor > 1 else 0
        
        if key == curses.KEY_DOWN:
            cursor = cursor+1 if cursor < len(menu)-1 else cursor

        if key == 10:
            return (menu[cursor], cursor) 

# Function that stays in the loop until the user confirms the input
def AskWithConfirm(header, question, screen):
    screen.clear()
    # Asks for it's name
    screen = PrintHeader(header, screen, 0, 0) 
    screen = PrintText(question, screen, 4, 0) 
    userInput = GetInput(screen, 6, 0)

    # Asks for confirmation 
    while True:
        screen.clear()
        screen = PrintHeader(header, screen, 0, 0) 
        checkText = "Is the following correct?  ---  " + userInput
        screen = PrintText(checkText, screen, 4, 0) 
        if ShowMenu(MENU_CONFIRM, screen, 6, 0 )[0] == "NO":
            screen.clear()
            # Asks for it's name again
            screen = PrintHeader(header, screen, 0, 0) 
            screen = PrintText(question, screen, 4, 0) 
            userInput = GetInput(screen, 6, 0)
        else:
            break 
    return userInput

# Ask without confirmation
def Ask(header, question, screen):
    screen.clear()
    # Asks for it's name
    screen = PrintHeader(header, screen, 0, 0) 
    screen = PrintText(question, screen, 4, 0) 
    userInput = GetInput(screen, 6, 0)
    return userInput

# Wraps the curses changes to the terminal to prevent errors
curses.wrapper(main)
