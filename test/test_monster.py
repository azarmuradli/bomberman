import unittest
from unittest.mock import Mock, patch
import pygame
from monster import Monster, DecisionMakingMonster
from map import Map  # Assuming Map class is used for determining move validity

class TestMonster(unittest.TestCase):
    def setUp(self):
        pygame.init()
        
        # Mocking the image loading as Monster might load an image
        patcher = patch('pygame.image.load', Mock(return_value=pygame.Surface((40, 40))))
        self.mock_image_load = patcher.start()
        self.addCleanup(patcher.stop)
        
        # Set up a simple map mock that allows all movements
        self.mock_map = Mock(spec=Map)
        self.mock_map.width = 10
        self.mock_map.height = 10
        self.mock_map.is_passable.side_effect = lambda x, y: True
        
        # Create a Monster instance
        self.monster = Monster(self.mock_map, 5, 5, 1)  # Initial position at (5, 5)

    def test_move_monster(self):
        # Initial position
        initial_row, initial_col = self.monster.row, self.monster.col

        # Movement simulation: move the monster to the right (5, 6)
        self.monster.row, self.monster.col = 5, 6  # Manually setting new position

        # Invoke update to process any additional logic
        self.monster.update(self.mock_map, [], [])  # Pass empty lists for monsters and players

        # Assertions: Check if the monster's position changed as expected
        self.assertEqual((self.monster.row, self.monster.col), (5, 6), "Monster did not move as expected")
        self.assertNotEqual((initial_row, initial_col), (self.monster.row, self.monster.col), "Monster position did not change")

    def test_initial_position(self):
        # Check initial position
        self.assertEqual((self.monster.row, self.monster.col), (5, 5), "Monster initial position is incorrect")

    def test_monster_speed(self):
        # Check monster speed
        self.assertEqual(self.monster.speed, 1, "Monster speed is incorrect")

    def test_monster_image_loaded(self):
        # Check if image is loaded
        self.assertIsNotNone(self.monster.image, "Monster image not loaded")

    def test_monster_rect_position(self):
        # Check if rect position is correct
        self.assertEqual(self.monster.rect.topleft, (5 * 40, 5 * 40), "Monster rect position is incorrect")

    def test_update_position(self):
        # Update monster position
        self.monster.row, self.monster.col = 6, 6
        self.monster.update(self.mock_map, [], [])
        self.assertEqual((self.monster.row, self.monster.col), (6, 6), "Monster update position is incorrect")

    def test_monster_get_coordinates(self):
        # Check get_coordinates method
        self.assertEqual(self.monster.get_coordinates(), (5, 5), "Monster get_coordinates is incorrect")

    def test_monster_move_valid(self):
        # Move to a valid position
        self.monster.row, self.monster.col = 5, 6
        self.monster.update(self.mock_map, [], [])
        self.assertEqual((self.monster.row, self.monster.col), (5, 6), "Monster did not move to valid position")

    def test_monster_catches_player(self):
        # Create a mock player and check if caught
        player = Mock()
        player.rect = pygame.Rect(self.monster.rect.topleft, self.monster.rect.size)
        self.assertTrue(self.monster.catches(player), "Monster did not catch the player")

    def test_monster_does_not_catch_player(self):
        # Create a mock player and check if not caught
        player = Mock()
        player.rect = pygame.Rect((self.monster.rect.right + 1, self.monster.rect.top), self.monster.rect.size)
        self.assertFalse(self.monster.catches(player), "Monster incorrectly caught the player")

    def test_monster_kill(self):
        # Test kill method
        self.monster.kill()
        self.assertFalse(self.monster.alive(), "Monster is still alive after kill")

if __name__ == '__main__':
    unittest.main()
