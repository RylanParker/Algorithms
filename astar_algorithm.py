try:
    from tkinter import *
except ImportError:
    print("Import error occurred.")

root_ui = Tk()
root_ui.geometry("1000x900")

class Tile:
    def __init__(self, parent_frame, x, y):
        # Intakes the object and the parent frame which it will be a child of
        self.enabled = True
        self.x = x
        self.y = y
        self.color = "green"

        print("Placing at: {}".format( (x, y)))
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
        self.x = 0
        self.y = 50

        self.tiles = []
        self.main_frame = Frame(master, width=800, height=800)

        # Create the rows
        for x in range(110):
            # Make sure the rows don't go off-screen
            if self.x >= 800:
                self.x = 0
                self.y += 70

            # Create a new tile, append it to a list and increment
            new_tile = Tile(self.main_frame, self.x, self.y)
            self.tiles.append(new_tile)
            self.x += 80

        self.main_frame.place(x=0, y=0)

# Create the frame objects
new_frame = MainFrame(root_ui)

# Keep the UI running
root_ui.mainloop()