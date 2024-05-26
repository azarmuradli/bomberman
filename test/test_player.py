import unittest
from game import Player
from map import Map
from gameField import GameField

class TestGameField(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(1, 1, 2, 2, 2, [])

    def test_move_up(self):
        self.player1.move(-1, 0)
        self.assertEqual(self.player1.get_coordinates(), (0,2))

    def test_move_down(self):
        self.player1.move(1, 0)
        self.assertEqual(self.player1.get_coordinates(), (2,2))

    def test_move_left(self):
        self.player1.move(0, -1)
        self.assertEqual(self.player1.get_coordinates(), (1,1))

    def test_move_right(self):
        self.player1.move(0, 1)
        self.assertEqual(self.player1.get_coordinates(), (1,3))

if __name__ == '__main__':
    unittest.main()
