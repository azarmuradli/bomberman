import pygame
from pygame.sprite import Sprite
from monster import PathfindingMonster
class PowerUp(Sprite):
    """
    Base class for all power-ups in the game.

    Attributes:
        image (Surface): The image representing the power-up.
        rect (Rect): The rectangle representing the position and size of the power-up.
    """
    def __init__(self, x, y, image_path):
        """
        Initializes the power-up with a position and image.

        Args:
            x (int): The x-coordinate for the power-up position.
            y (int): The y-coordinate for the power-up position.
            image_path (str): The path to the image file for the power-up.
        """
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x * 40, y * 40))

    def apply_effect(self, player,monsters):
        """
        Applies the effect of the power-up to the player and monsters.
        This method is meant to be overridden in child classes.

        Args:
            player: The player object to which the effect is applied.
            monsters (list): The list of monster objects.
        """
        # This method will be overridden in child classes
        pass


class BombPowerUp(PowerUp):
    """
    A power-up that increases the player's bomb limit.
    """
    def __init__(self, x, y):
        super().__init__(x, y, "images/powerup_image.png")
        

    def apply_effect(self, player,monsters):
        """
        Increases the player's bomb limit by 1.

        Args:
            player: The player object to which the effect is applied.
            monsters (list): The list of monster objects (not used in this power-up).
        """
        player.bombs_limit += 1
        print("Increased number of bombs!")

class RangePowerUp(PowerUp):
    """
    A power-up that increases the player's bomb blast range.
    """
    def __init__(self, x, y):
        super().__init__(x, y, "images/range_powerup_image.png")

    def apply_effect(self, player,monsters):
        """
        Increases the player's bomb blast range by 1.

        Args:
            player: The player object to which the effect is applied.
            monsters (list): The list of monster objects (not used in this power-up).
        """
        player.blast_range += 1
        print("Increased blast range!")

class DetonatorPowerUp(PowerUp):
    """
    A power-up that gives the player a detonator to manually detonate bombs.
    """
    def __init__(self, x, y):
        super().__init__(x, y, "images/detonator_powerup_image.png")

    def apply_effect(self, player,monsters):
        """
        Grants the player a detonator.

        Args:
            player: The player object to which the effect is applied.
            monsters (list): The list of monster objects (not used in this power-up).
        """
        player.has_detonator = True
        print("Detonator acquired! Press bomb placement to detonate.")


class GhostPowerUp(PowerUp):
    """
    A power-up that activates ghost mode for the player, allowing them to move through obstacles.
    """
    def __init__(self, x, y):
        super().__init__(x, y, "images/ghost_powerup_image.png")

    def apply_effect(self, player,monsters):
        """
        Activates ghost mode for the player.

        Args:
            player: The player object to which the effect is applied.
            monsters (list): The list of monster objects (not used in this power-up).
        """
        player.activate_ghost_mode()
        print("Ghost mode activated!")


class InvincibilityPowerUp(PowerUp):
    """
    A power-up that makes the player invincible for a period of time.
    """
    def __init__(self, x, y):
        super().__init__(x, y, "images/invincibility_powerup_image.png")

    def apply_effect(self, player,monsters):
        """
        Activates invincibility for the player.

        Args:
            player: The player object to which the effect is applied.
            monsters (list): The list of monster objects (not used in this power-up).
        """
        player.activate_invincibility()
        print("Invincibility activated!")

class ObstaclePowerUp(PowerUp):
    """
    A power-up that increases the player's capacity to place obstacles.
    """
    def __init__(self, x, y):
        super().__init__(x, y, "images/obstacle_powerup_image.png")

    def apply_effect(self, player,monsters):
        """
        Increases the player's obstacle placement capacity.

        Args:
            player: The player object to which the effect is applied.
            monsters (list): The list of monster objects (not used in this power-up).
        """
        player.increase_obstacle_capacity()
        print("Obstacle placement capacity increased!")

class MonsterPowerUp(PowerUp):
    """
    A power-up that temporarily disables intelligent pathfinding for monsters.
    """
    def __init__(self, x, y):
        super().__init__(x, y, "images/monster_powerup_image.png")

    def apply_effect(self, player, monsters):
        """
        Pauses the pathfinding behavior of intelligent monsters.

        Args:
            player: The player object to which the effect is applied.
            monsters (list): The list of monster objects.
        """
        for monster in monsters:
            if isinstance(monster, PathfindingMonster):  
                monster.pause()
        print("Intelligent monster is not following player anymore!")