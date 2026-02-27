try:
    from tkinter import *
    import random
except ImportError:
    print("Import error occurred.")

root_ui = Tk()
root_ui.geometry("1000x1000")

row_width = 10
row_height = 10
increment_x = 80
increment_y = 70

total_rheight = 800
total_rwidth = 800

class Tile:
    def __init__(self, parent_frame, x, y):
        # Intakes the object and the parent frame which it will be a child of
        self.enabled = True
        self.x = x
        self.y = y
        self.goal = False
        self.start = False
        self.color = "green"

        self.tile = Button(parent_frame, width=10, height=4, bg=self.color, command=self.ChangeStatus)
        self.tile.place(x=self.x, y=self.y)

    def ChangeStatus(self):
        self.enabled = not self.enabled

        if (self.enabled):
            self.color = "green"
        else:
            self.color = "red"

        self.tile.config(bg=self.color)
    
class MainFrame:
    def __init__(self, master):
        self.origin_x = 0
        self.origin_y = 0

        self.x = self.origin_x
        self.y = self.origin_y

        self.tiles = []
        self.main_frame = Frame(master, width=1500, height=1500)

        # Create the rows
        for x in range(row_width * row_height):
            # Make sure the rows don't go off-screen
            if self.x >= total_rwidth:
                self.x = self.origin_x
                self.y += increment_y

            # Create a new tile, append it to a list and increment
            new_tile = Tile(self.main_frame, self.x, self.y)
            self.tiles.append(new_tile)
            self.x += increment_x

        # Goal Tile
        goal_tile = RandomTile(self.tiles)
        goal_tile.goal = True
        goal_tile.color = "orange"
        goal_tile.tile.config(bg=goal_tile.color)

        # Start Tile
        start_tile = RandomTile(self.tiles)
        start_tile.start = True
        start_tile.color = "red"
        start_tile.tile.config(bg=start_tile.color)

        # Get all the possible moves and then graph them visually
        possible_moves = SurroundingTiles((start_tile.x, start_tile.y))

        for t in possible_moves:
            target_tile = self.FindTileByPos(t)
            target_tile.color = "blue"
            target_tile.tile.config(bg=target_tile.color)
        

        self.main_frame.place(x=0, y=0)
    
    def FindTileByPos(self, target_pos):
        for tile in self.tiles:
            if tile.enabled:
                if (tile.x == target_pos[0] and tile.y == target_pos[1]):
                    return tile
            
        raise Exception("Couldn't find tile! {}".format(target_pos))

def RandomTile(tiles: list):
    tile = tiles[random.randint(0, len(tiles))]

    if not tile.start and not tile.goal:
        return tile
    else:
        RandomTile(tiles)

# ALGORITHM FUNCTIONS

def astar_algorithm():
    pass

def calculate_distance(pos1, pos2):
    return ((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1]))

def SurroundingTiles(position) -> list:
    # Returns every possible move from a current position, including moves that may not be legal.
    current_x, current_y = position
    moves = []

    if current_x <= total_rwidth - increment_x:
        moves.append((current_x + increment_x, current_y))  # Right
    if current_x >= increment_x:
        moves.append((current_x - increment_x, current_y))  # Left
        
    if current_y <= total_rheight - increment_y:
        moves.append((current_x, current_y + increment_y)) # Down
    if current_y >= increment_y:
        moves.append((current_x, current_y - increment_y)) # Top
    
    if current_x >= increment_x and current_y >= increment_y:
        moves.append((current_x - increment_x, current_y - increment_y)) # Top left
    
    if current_x <= total_rwidth - increment_x and current_y <= total_rheight - increment_y:
        moves.append((current_x + increment_x, current_y - increment_y)) # Top right
    """     
    if current_x >= increment_x and current_y <= total_rheight - increment_y:
        moves.append((current_x - increment_x, current_y - increment_y)) # Bottom left

    if current_x <= total_rwidth - increment_x and current_x <= total_rwidth - increment_x:
        moves.append((current_x + increment_x, current_y - increment_y)) # Bottom right """
    """ 
    moves = [
        (current_x + 1, current_y), (current_x - 1, current_y), # Left and Right
        (current_x, current_y + 1), (current_x, current_y - 1) # Up and Down
        (current_x + 1, current_y + 1), (current_x - 1, current_y - 1) # Top Right and Top Left
        (current_x + 1, current_y - 1), (current_x - 1, current_y - 1) # Bottom right and Bottom left
    ] """
    
    print("Leaving with: ", moves)
    return moves

# Create the frame objects
new_frame = MainFrame(root_ui)

# Keep the UI running
root_ui.mainloop()