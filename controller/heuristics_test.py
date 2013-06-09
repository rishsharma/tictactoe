"""Tests that correspond to strategy."""

__author__ = "Rishi Sharma (rishsharma@gmail.com)"

import unittest

from controller import heuristics
from model import board


class HeuristicsTest(unittest.TestCase):
  """Class that tests heuristics functions."""

  def testGetCenterValue(self):
    play_board = board.Board(3)
    for position in xrange(9):
      if position == 4:
        self.assertEqual(heuristics.Heuristic.CENTER,
                         heuristics.GetCenterValue(position, play_board))
      else:
        self.assertEqual(heuristics.Heuristic.INVALID,
                         heuristics.GetCenterValue(position, play_board))

  def testGetCornerValue(self):
    play_board = board.Board(3)
    for position in xrange(9):
      if position in (0, 2, 6, 8):
        self.assertEqual(heuristics.Heuristic.CORNER,
                         heuristics.GetCornerValue(position, play_board))
      else:
        self.assertEqual(heuristics.Heuristic.INVALID,
                         heuristics.GetCornerValue(position, play_board))

  def testGetRelativeRowHeuristic(self):
    play_board = board.Board(3)
    self.assertEqual(heuristics.Heuristic.INVALID,
                     heuristics._GetRelativeRowHeuristic(
                         1, play_board, board.BoardValue.X))
    play_board.SetPosition(0, board.BoardValue.X)
    play_board.SetPosition(2, board.BoardValue.X)
    self.assertEqual(heuristics.Heuristic.INVALID,
                     heuristics._GetRelativeRowHeuristic(
                         1, play_board, board.BoardValue.O))
    self.assertEqual(4 + heuristics.Heuristic.LINE,
                     heuristics._GetRelativeRowHeuristic(
                         1, play_board, board.BoardValue.X))

  def testGetRelativeColumnHeuristic(self):
    play_board = board.Board(3)
    self.assertEqual(heuristics.Heuristic.INVALID,
                     heuristics._GetRelativeColumnHeuristic(
                         1, play_board, board.BoardValue.X))
    play_board.SetPosition(0, board.BoardValue.X)
    play_board.SetPosition(6, board.BoardValue.X)
    self.assertEqual(heuristics.Heuristic.INVALID,
                     heuristics._GetRelativeColumnHeuristic(
                         3, play_board, board.BoardValue.O))
    self.assertEqual(4 + heuristics.Heuristic.LINE,
                     heuristics._GetRelativeColumnHeuristic(
                         3, play_board, board.BoardValue.X))

  def testGetDiagonalHeuristic(self):
    play_board = board.Board(3)
    self.assertEqual(heuristics.Heuristic.INVALID,
                     heuristics._GetDiagonalHeuristic(
                         1, play_board, board.BoardValue.X))
    play_board.SetPosition(0, board.BoardValue.X)
    play_board.SetPosition(2, board.BoardValue.X)
    play_board.SetPosition(6, board.BoardValue.X)
    self.assertEqual(6,
                     heuristics._GetDiagonalHeuristic(
                         4, play_board, board.BoardValue.X))
    self.assertEqual(heuristics.Heuristic.INVALID,
                     heuristics._GetDiagonalHeuristic(
                         8, play_board, board.BoardValue.O))
    self.assertEqual(1,
                     heuristics._GetDiagonalHeuristic(
                         8, play_board, board.BoardValue.X))

  def testGetLocalityValue(self):
    play_board = board.Board(3)
    self.assertEqual(heuristics.Heuristic.INVALID,
                     heuristics.GetLocalityValue(
                         1, play_board, board.BoardValue.X))
    play_board.SetPosition(0, board.BoardValue.X)
    play_board.SetPosition(2, board.BoardValue.X)
    self.assertEqual(heuristics.Heuristic.LOCALITY * 2,
                     heuristics.GetLocalityValue(
                         1, play_board, board.BoardValue.O))
    self.assertEqual(heuristics.Heuristic.INVALID,
                     heuristics.GetLocalityValue(
                         1, play_board, board.BoardValue.X))


if __name__ == '__main__':
  unittest.main()
