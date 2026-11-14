import arcade
import random

# Game constants
WIDTH,HEIGHT = 1200, 720
WINDOW_TITLE = "Platformer"
TITLE_SCALING = 0.5
COIN_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20



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
        
    def coins_build(self):
        for x in range(128, 1250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)
            
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE,resizable=False)

        self.player_texture = None
        self.player_sprite = None
        self.player_list = None
        
        self.wall_list = None   
        self.camera = None  
        self.coin_list = None
        
        # these are static assests, so no need to set them to None
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        
        self.gui_camera = None
        self.score = 0
        self.score_text = None
        
    def on_update(self, delta_time):
            self.physics_engine.update()
            self.camera.position = self.player_sprite.position
            
            # for the player to interact with the coins in the game
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)
                self.score += 75
                self.score_text.text = f"Score: {self.score}"
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.setup()
            
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        
        
                    
                
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
            
    
    def setup(self):
        # game setup and call it to restart the game
        self.player_texture = arcade.load_texture(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list = arcade.SpriteList() 
        # for collision detection
        # Spatial Hashing is a special algorithm which will make it much more performant, at the cost of being more expensive to move sprites. 
        # Often see this option enabled on SpriteLists which are not expected to move much, such as walls or a floor.
        self.player_list.append(self.player_sprite)
        
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.walls_build()
        self.camera = arcade.Camera2D()
        self.coin_list = arcade.SpriteList(use_spatial_hash=True) # whether coins move or not.
        self.coins_build()
        
        self.gui_camera = arcade.Camera2D()
        self.score = 0
        self.score_text =  arcade.Text(f"Score:{self.score}", x=16, y=HEIGHT-32, color=arcade.color.BLACK, font_size=18)
        
         
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, walls=self.wall_list, 
                                                             gravity_constant=GRAVITY)
        self.background_color = arcade.color.CYAN
        
    def on_draw(self):
        """Render the screen"""
        # ensures clean slate
        self.clear()
        # code to draw other things here
        self.camera.use()
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.gui_camera.use()
        self.score_text.draw()
        
def main():
    window = GameView()
    window.setup()
    arcade.run()
    
if __name__== "__main__":
    main()
