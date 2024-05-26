import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    def __init__(self, game_field, row, col,delay):  # move_delay in milliseconds
        """
        Initialize the Explosion object.

        This class represents an explosion in the game. The explosion is visible for a certain duration and can affect 
        the game field.

        :param game_field: The game field where the explosion occurs.
        :param row: The row position of the explosion on the grid.
        :param col: The column position of the explosion on the grid.
        :param delay: The delay before the explosion is added to the game field in milliseconds.
        """
        super().__init__()
        self.game_field = game_field
        self.image = pygame.image.load("images/explosion_image.png")  # Make sure the image path is correct
        self.rect = self.image.get_rect(topleft=(col * 40, row * 40))  # Assuming tile size is 40x40
        self.row = row
        self.col = col
        self.reference_time = 0
        self.creation_time = pygame.time.get_ticks()  # Record creation time
        self.duration = 500  # Explosion visible for 1000 milliseconds (1 second)s
        self.delay = delay


    def add(self,explosions,explosion_tiles,effect):
        """
        Add the explosion to the game field after the specified delay.

        :param explosions: A group of active explosions in the game.
        :param explosion_tiles: A list of tiles affected by explosions.
        :param effect: The effect to remove from explosion_tiles after adding the explosion.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.reference_time > self.delay and not self.is_explosion_present(explosions, self.row, self.col):
            explosions.add(self)
            explosion_tiles.remove(effect)
        self.reference_time = current_time

    def is_explosion_present(self,explosions, row, col):
        """
        Check if there is already an explosion at the given position.

        :param explosions: A group of active explosions in the game.
        :param row: The row position to check.
        :param col: The column position to check.
        :return: True if an explosion is present at the position, False otherwise.
        """
        for explosion in explosions:
            if explosion.row == row and explosion.col == col:
                return True
        return False

    def draw(self, screen):
        """
        Draw the explosion on the given screen.

        :param screen: The screen surface to draw the explosion on.
        """
        screen.blit(self.image, self.rect)

    def is_expired(self):
        """
        Check if the explosion has expired.

        :return: True if the explosion duration has passed, False otherwise.
        """
        # Check if the explosion has expired
        return pygame.time.get_ticks() - self.creation_time > self.duration


    def kill(self):
        self.kill()

    def kill(self):
        """
        Remove the explosion from all groups.

        This method correctly calls the `kill` method from the parent class to ensure the explosion is properly removed.
        """
        pygame.sprite.Sprite.kill(self)  # Correctly call the kill method from the parent class
