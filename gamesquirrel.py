import useful

import playersquirrel
import roomsquirrel
import itemsquirrel
 

# Master Class to store all the game information
class GameSquirrel():

    # Constructor
    def __init__(self):
        self.name = ""
        self.instructions = ""
        self.credits = ""
        self.rooms = []
        self.items = []
        self.player = playersquirrel.Player()
        
    def EditConnection(self, fromRoom, toRoom, direction):
        self.rooms[fromRoom].edit_connection(direction, toRoom)

    def removeRoom(self, room_index):
        for r in self.rooms: #remove connections
            if room_index in r.connections:
                indices = [i for i,val in enumerate(r.connections)
                           if val==room_index]
                for ind in indicies:
                    r.connections[ind] = -1
        
        for item in self.items: #remove item info from room
            if room_index == item.location:
                item.location = None
        
        self.rooms.remove(self.rooms[room_index])

    def PlaceItem(self, itemIndex, where):
        self.items[itemIndex].PlaceAt(where)
        if where == -2: # PLAYER INVENTORY
            self.player.AddToInventory(itemIndex)
        elif where >= 0: # IN A ROOM
            self.rooms[where].AddItem(itemIndex)
            
  
    def removeItem(self, itemIndex):
        # possibly don't need this function

        # remove it from the room
        room_index = self.items[itemIndex].whereIs
        self.rooms[room_index].RemoveItem(itemIndex)

        # remove it from the game
        del self.items[itemIndex]
