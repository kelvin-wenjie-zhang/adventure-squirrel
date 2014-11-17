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
        
        for i in range(len(self.items)): #remove item info from room
            if room_index == self.items[i].whereIs:
                self.items[i].whereIs = -1
        
        del self.rooms[room_index]

        # update the room index in all the items
        for j in range(len(self.items)):
            if self.items[j].whereIs > room_index:
                self.items[j].whereIs -= 1

    def PlaceItem(self, itemIndex, where):
        self.items[itemIndex].PlaceAt(where)
        if where == -2: # PLAYER INVENTORY
            self.player.AddToInventory(itemIndex)
        elif where >= 0: # IN A ROOM
            self.rooms[where].AddItem(itemIndex)
            
  
    def RemoveItem(self, itemIndex):
        # possibly don't need this function

        # remove it from the room and inventory
        # then we adjust the other item index in the rooms
        # -->decrement item index by 1 
        room_index = self.items[itemIndex].whereIs
        
        if room_index == -1:
            del self.items[itemIndex]

        elif room_index == -2:
            self.player.RemoveInventory(itemIndex)
            for i in range(len(self.player.RemoveInventory)):
                if self.player.RemoveInventory[i] > itemIndex:
                    self.player.RemoveInventory[i] -= 1
            del self.items[itemIndex]

        elif room_index >= 0:
            self.rooms[room_index].RemoveItem(itemIndex)
            for j in range(len(self.rooms)):
                for k in range(len(self.rooms[j].items)):
                    if self.rooms[j].items[k] > itemIndex:
                        self.rooms[j].items[k] -= 1
            del self.items[itemIndex]


