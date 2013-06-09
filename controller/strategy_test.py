"""Tests that correspond to strategy."""

__author__ = "Rishi Sharma (rishsharma@gmail.com)"

import unittest

from model import board
from controller import strategy


class StrategyTest(unittest.TestCase):
  """Class that tests strategy functions."""

  def testCanWinRow(self):
    play_board = board.Board(3)
    self.assertEqual(-1, strategy.CanWin(play_board, board.BoardValue.X))
    play_board.SetPosition(0, board.BoardValue.X)
    play_board.SetPosition(2, board.BoardValue.X)
    self.assertEqual(1, strategy.CanWin(play_board, board.BoardValue.X))

  def testCanWinColumn(self):
    play_board = board.Board(3)
    self.assertEqual(-1, strategy.CanWin(play_board, board.BoardValue.X))
    play_board.SetPosition(0, board.BoardValue.X)
    play_board.SetPosition(6, board.BoardValue.X)
    self.assertEqual(3, strategy.CanWin(play_board, board.BoardValue.X))

  def testCanWinDescendingDiagonal(self):
    play_board = board.Board(3)
    self.assertEqual(-1, strategy.CanWin(play_board, board.BoardValue.X))
    play_board.SetPosition(0, board.BoardValue.X)
    play_board.SetPosition(8, board.BoardValue.X)
    self.assertEqual(4, strategy.CanWin(play_board, board.BoardValue.X))

  def testCanWinAscendingDiagonal(self):
    play_board = board.Board(3)
    self.assertEqual(-1, strategy.CanWin(play_board, board.BoardValue.X))
    play_board.SetPosition(2, board.BoardValue.X)
    play_board.SetPosition(6, board.BoardValue.X)
    self.assertEqual(4, strategy.CanWin(play_board, board.BoardValue.X))


if __name__ == '__main__':
  unittest.main()
