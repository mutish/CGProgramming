import arcade
import random

# Game constants
WIDTH,HEIGHT = 1200, 720
WINDOW_TITLE = "Platformer"
TITLE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5



class GameView(arcade.Window):
    def walls_build(self):
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png",scale=TITLE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        coordinate_list = [[512, 96],[256,96], [768,96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=TITLE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)
            
        # for x in range(128,1000, 256):
        #     wall= arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=TITLE_SCALING)
        #     wall.center_x = x
        #     wall.center_y = 256
        #     self.wall_list.append(wall)
            
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE,resizable=False)
        self.player_texture = arcade.load_texture(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y =128
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True) # for collision detection
        # Spatial Hashing is a special algorithm which will make it much more performant, at the cost of being more expensive to move sprites. 
        # Often see this option enabled on SpriteLists which are not expected to move much, such as walls or a floor.

        self.walls_build()
        self.background_color = arcade.color.CYAN
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        
        
    def on_update(self, delta_time):
            self.physics_engine.update()
    
    def on_key_press(self, key, modifiers):
                if key == arcade.key.UP or key == arcade.key.W:
                    self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
                elif key == arcade.key.DOWN or key == arcade.key.S:
                    self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
                elif key == arcade.key.LEFT or key == arcade.key.A:
                    self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                elif key == arcade.key.RIGHT or key == arcade.key.D:
                    self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
            
    
    def setup(self):
        # game setup and call it to restart the game
        pass
    def on_draw(self):
        """Render the screen"""
        # ensures clean slate
        self.clear()
        # code to draw other things here
        self.player_list.draw()
        self.wall_list.draw()
        
def main():
    window = GameView()
    window.setup()
    arcade.run()
    
if __name__== "__main__":
    main()
