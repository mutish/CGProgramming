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
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)
        # Variable to hold our texture for our player
        self.player_texture = None
        # Separate variable that holds the player sprite
        self.player_sprite = None 
        self.tile_map = None
        self.scene =  None
        self.camera = None  
        self.gui_camera = None
        self.score = 0
        self.score_text = None
        self.reset_score = True
        
        self.end_of_map=0 # right edge of map
        self.level=1 # level number to load
        
        
        # these are static assests, so no need to set them to None
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
          
    def setup(self):
        # game setup and call it to restart the game
        layout_options = {
            "Platforms":{
                "use_spatial_hash": True
            }
        }
        self.tile_map = arcade.load_tilemap(f":resources:tiled_maps/map2_level_{self.level}.json", scaling=TITLE_SCALING, layer_options=layout_options)
        self.end_of_map = (self.tile_map.width * self.tile_map.tile_width) * self.tile_map.scaling
        # Create scene from tilemap 
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list_after("Player","Foreground")
        self.player_texture = arcade.load_texture(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        # for collision detection
        # Spatial Hashing is a special algorithm which will make it much more performant, at the cost of being more expensive to move sprites. 
        # Often see this option enabled on SpriteLists which are not expected to move much, such as walls or a floor.
        # self.player_list.append(self.player_sprite)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, walls=self.scene["Platforms"], 
                                                             gravity_constant=GRAVITY)
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        self.score = 0
        self.score_text =  arcade.Text(f"Score:{self.score}", x=16, y=HEIGHT-32, color=arcade.color.BLACK, font_size=18)
        self.background_color = arcade.color.CORNFLOWER_BLUE
    
    
    def on_draw(self):
        """Render the screen"""
        # ensures clean slate
        self.clear()
        # code to draw other things here
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        self.score_text.draw()
    
    def on_update(self, delta_time):
        """Movement and Game Logic"""
        self.physics_engine.update()
        
            
        # for the player to interact with the coins in the game
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Coins"])
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 75
            self.score_text.text = f"Score: {self.score}"
        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1
            self.setup()
        self.camera.position = self.player_sprite.position
        
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["Don't Touch"]):
            arcade.play_sound(self.gameover_sound)
            self.setup()
    
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
            
    
    

        
def main():
    window = GameView()
    window.setup()
    arcade.run()
    
if __name__== "__main__":
    main()
