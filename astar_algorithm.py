try:
    from tkinter import *
    import random
    import heapq
    import math
except ImportError:
    print("Import error occurred.")

""" 
To do list 


1. Fix grid mis-match
2. Fix A* Search
3. Add UI for settings
 """
root_ui = Tk()
root_ui.geometry("1000x1000")

increment_x = 80
increment_y = 80

total_rwidth = 800
total_rheight = 800

class Hog:
    def __init__(self, x, y):
        self.steps_taken = 0
        self.x = x 
        self.y = y
        self.g = 0

def new_frame():
    # Destroy the children in the current frame
    # Re-load the frame
    global new_frame
    print("Creating new frame!")

    for child in new_frame.main_frame.winfo_children():
        child.destroy()

    new_frame.x = new_frame.origin_x
    new_frame.y = new_frame.origin_y
    new_frame.CreateScene(root_ui)


class Tile:
    def __init__(self, parent_frame, x, y):
        # Intakes the object and the parent frame which it will be a child of
        self.enabled = random.choice([True, False])
        self.x = x
        self.y = y
        self.goal = False
        self.start = False
        self.color = "green"

        self.tile = Button(parent_frame, width=10, height=4, bg=self.color, command=self.ChangeStatus)
        self.tile.place(x=self.x, y=self.y)
        self.UpdateStatus()

    def ChangeStatus(self):
        self.enabled = not self.enabled

        self.UpdateStatus()

    def UpdateStatus(self):
        # Colors tile according to the tile type

        if (self.enabled):
            self.color = "green"
        else:
            self.color = "red"

        if self.start:
            self.color = "blue"
        if self.goal:
            self.color = "orange"

        self.tile.config(bg=self.color)
    
class MainFrame:
    def __init__(self, master):
        self.origin_x = 0
        self.origin_y = 0

        self.x = self.origin_x
        self.y = self.origin_y
        self.restart_button = Button(master, text="Create New Scene", bg="red", width=500, height=500, command=new_frame)
        self.restart_button.place(relx=0, rely=0, anchor=CENTER)

        self.CreateScene(master)

    def CreateScene(self, master):
        self.tiles = []
        self.main_frame = Frame(master, width=1500, height=1500)

        # Create the rows
        for x in range(110):
            # Make sure the rows don't go off-screen
            if self.x >= total_rwidth:
                self.x = self.origin_x
                self.y += increment_y

            # Create a new tile, append it to a list and increment
            
            new_tile = Tile(self.main_frame, self.x, self.y)
            self.tiles.append(new_tile)
            self.x += increment_x

            print("Currently at: {}".format((x, (self.x, self.y))))

        # Goal Tile 
        goal_tile = RandomTile(self.tiles)
        goal_tile.goal = True
        goal_tile.color = "orange"
        goal_tile.tile.config(bg=goal_tile.color)

        # Start Tile
        start_tile = RandomTile(self.tiles)
        start_tile.start = True
        start_tile.color = "blue"
        start_tile.tile.config(bg=start_tile.color)

        # Get all the possible moves and then graph them visually
        new_hog = Hog(start_tile.x, start_tile.y)
        hog_path = []
        safe_tiles = []
        t_path = []

        # Make only x amount of moves
        for move in range(10):

            # Get the surrounding tiles
            possible_moves = SurroundingTiles((new_hog.x, new_hog.y))

            for t in possible_moves:

                # Get the tile information
                target_tile = self.FindTileByPos(t)
                smallest_cost = math.inf

                # If there is a real tile
                if target_tile:

                    # Get heurestics data
                    g = new_hog.steps_taken * math.sqrt(increment_x**2 + increment_y**2)
                    h = math.sqrt((goal_tile.x - target_tile.x)**2 + (goal_tile.y - target_tile.y)**2)
                    tile_cost = g + h

                    if tile_cost < smallest_cost and target_tile.enabled:
                        smallest_cost = target_tile

                    heapq.heappush(safe_tiles, (tile_cost, new_hog))
                    t_path.append(t)
                    
                    if smallest_cost not in hog_path and smallest_cost != math.inf:
                        hog_path.append((smallest_cost.x, smallest_cost.y))
                        new_hog.x, new_hog.y = (smallest_cost.x, smallest_cost.y)

                    new_hog.steps_taken += 1
                    
                stepped_tile = self.FindTileByPos((new_hog.x, new_hog.y))


                if stepped_tile and not stepped_tile.goal:
                    stepped_tile.tile.config(bg="purple")
        
                else:
                    pass
                
        print("Goal is located at: {} \n"
            "Start is located at: {} \n"
            "Path taken: {}".format((goal_tile.x, goal_tile.y), (start_tile.x, start_tile.y), hog_path))
        
        self.main_frame.place(x=0, y=0)
    
    def FindTileByPos(self, target_pos):
        # Go through each tile, check if its our target tile, return.

        for tile in self.tiles:
            if (tile.x == target_pos[0] and tile.y == target_pos[1]):
                return tile

            
        raise Exception("Couldn't find tile! {}".format(target_pos))

def RandomTile(tiles: list):
    # Choose a random tile, if it isn't special, return it. If it, re-run the function until its normal.

    tile = tiles[random.randint(0, len(tiles))]

    if not tile.start and not tile.goal:
        return tile
    else:
        RandomTile(tiles)

# ALGORITHM FUNCTIONS

def astar_algorithm():
    pass

def calculate_distance(pos1, pos2):
    return (((pos2[0] - pos1[0]) / 80)**2 + ((pos2[1] - pos1[1]) / 70))

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
    
    if current_x <= total_rwidth - increment_x and current_y >= increment_y:
        moves.append((current_x + increment_x, current_y - increment_y)) # Top right

    if current_x >= increment_x and current_y <= total_rheight - increment_y:
        moves.append((current_x - increment_x, current_y + increment_y)) # Bottom left

    if current_x <= total_rwidth - increment_x and current_y <= total_rheight - increment_y:
        moves.append((current_x + increment_x, current_y + increment_y)) # Bottom right
    return moves

# Create the frame objects
new_frame = MainFrame(root_ui)

# Keep the UI running
root_ui.mainloop()