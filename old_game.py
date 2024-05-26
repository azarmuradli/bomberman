import pygame
import random
from map import Map
from player import Player
from gameField import GameField
from monster import Monster

# Initialize Pygame
pygame.init()

# Set up display parameters
tile_size = 40
screen_width = tile_size * 13
screen_height = tile_size * 11
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bomberman Game")

# Load the map
map_filename = 'map1.txt'
game_map = Map(map_filename, tile_size)

# Initialize the game field
game_field = GameField(game_map)

# Utility function to find a valid starting position
def get_random_position(game_map):

    """
    Finds a valid starting position on the game map.

    Args:
        game_map (Map): The game map object.

    Returns:
        tuple: A tuple containing the row and column of a valid starting position.
    """
    while True:
        row = random.randint(0, game_map.height - 1)
        col = random.randint(0, game_map.width - 1)
        if game_map.isFloor(row, col):  # Checks if the tile is a floor
            return row, col

# Player Group - Single for now
player = Player(0,0,2,2)

# Initialize monsters at valid positions
monsters = pygame.sprite.Group()
for _ in range(3):  # Adjust number of monsters as needed
    row, col = get_random_position(game_map)
    monster = Monster(game_field, row, col, 1)  # Speed parameter is set to 1
    monsters.add(monster)

# Main game loop
running = True

# For controlling the frame rate
clock = pygame.time.Clock() 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            player_coords = player.get_coordinates()
            if event.key == pygame.K_w:
                if game_field.is_valid_move(player_coords, (-1,0)):
                    player.move(-1, 0)  # Move up (decrement row)
            elif event.key == pygame.K_s:
                if game_field.is_valid_move(player_coords, (1,0)):
                    player.move(1, 0)  # Move down (increment row)   
            elif event.key == pygame.K_a:
                if game_field.is_valid_move(player_coords, (0,-1)):
                    player.move(0, -1)  # Move left (decrement column)
            elif event.key == pygame.K_d:
                if game_field.is_valid_move(player_coords, (0,1)):
                    player.move(0, 1)  # Move right (increment column)

    for monster in monsters:
        monster.update(game_map, monsters)

    # Drawing
    screen.fill((0, 0, 0))  # Clear the screen
    
    # Render the map
    game_map.draw(screen)

    # Draw the monsters
    monsters.draw(screen)  

    # Draw the player
    player.draw(screen)  

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

    collisions = pygame.sprite.spritecollide(player, monsters, False)
    if collisions:
        print("The player has been caught by a monster!")
        running = False

pygame.quit()