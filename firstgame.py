import arcade

WIDTH, HEIGHT = 800, 600
class MyGame(arcade.Window):  # this is the window/application class
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "My first game using Python Arcade")
        def on_draw(self):
            self.clear()
            
game = MyGame() # application object
arcade.run() #starts the event game loop
