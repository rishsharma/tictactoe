"""Tests for board functionality."""

__author__ = "rishisharma@gmail.com"


import unittest

from model import board


class BoardValueTest(unittest.TestCase):
  """Class that tests BoardValue functions."""

  def testStringConversion(self):
    self.assertEqual("X", board.BoardValue.ToString(board.BoardValue.X))
    self.assertEqual("O", board.BoardValue.ToString(board.BoardValue.O))
    self.assertEqual(" ", board.BoardValue.ToString(board.BoardValue.NONE))
    self.assertRaises(board.InvalidBoardSetting, board.BoardValue.ToString, "Z")


class UserSentinelTest(unittest.TestCase):
  """Class that tests the UserSentinel object."""

  def testIsWinner(self):
    win_map = (((0, 0), (0, 1), (0, 2)),
               ((1, 0), (1, 1), (1, 2)),
               ((2, 0), (2, 1), (2, 2)),
               ((0, 0), (1, 0), (2, 0)),
               ((1, 0), (1, 1), (1, 2)),
               ((2, 0), (2, 1), (2, 2)),
               ((0, 0), (1, 1), (2, 2)),
               ((0, 2), (1, 1), (2, 0)))

    for win_combo in win_map:
      user_sentinel = board.UserSentinel(3)
      for coordinate in win_combo:
        self.assertFalse(user_sentinel.IsWinner())
        user_sentinel.Update(*coordinate)
      self.assertTrue(user_sentinel.IsWinner())


class BoardTest(unittest.TestCase):
  """Class that tests board functions."""

  def testToPosition(self):
    play_board = board.Board(3)
    for position in xrange(9):
      self.assertEqual(position, play_board.ToPosition(
          int(position / 3), int(position % 3)))
    self.assertRaises(board.InvalidBoardPosition, play_board.ToPosition, -1, -1)
    self.assertRaises(board.InvalidBoardPosition, play_board.ToPosition, 10, 10)

  def testToCoordinates(self):
    play_board = board.Board(3)
    for position in xrange(9):
      self.assertEqual((int(position / 3), int(position % 3)),
                       play_board.ToCoordinates(position))
    self.assertRaises(board.InvalidBoardPosition, play_board.ToCoordinates, -1)
    self.assertRaises(board.InvalidBoardPosition, play_board.ToCoordinates, 9)

  def testInvalidSetPosition(self):
    play_board = board.Board(3)
    self.assertRaises(board.InvalidBoardPosition,
                      play_board.SetPosition, -1, board.BoardValue.X)
    self.assertRaises(board.InvalidBoardPosition,
                      play_board.SetPosition, 9, board.BoardValue.X)

  def testValidSetPosition(self):
    play_board = board.Board(3)
    play_board.SetPosition(1, board.BoardValue.X)
    self.assertEqual(board.BoardValue.X, play_board._board[0][1])

  def testInvalidSetCoordinates(self):
    play_board = board.Board(3)
    self.assertRaises(board.InvalidBoardPosition,
                      play_board.SetCoordinates, -1, -1, board.BoardValue.X)
    self.assertRaises(board.InvalidBoardPosition,
                      play_board.SetCoordinates, 9, 9, board.BoardValue.X)

  def testInvalidSetCoordinatesAlreadyTaken(self):
    play_board = board.Board(3)
    play_board.SetCoordinates(0, 0, board.BoardValue.X)
    self.assertRaises(board.InvalidBoardSetting,
                      play_board.SetCoordinates, 0, 0, board.BoardValue.O)

  def testValidSetCoordinates(self):
    play_board = board.Board(3)
    play_board.SetCoordinates(0, 1, board.BoardValue.X)
    self.assertEqual(board.BoardValue.X, play_board._board[0][1])

  def testInvalidGetFromPosition(self):
    play_board = board.Board(3)
    self.assertRaises(board.InvalidBoardPosition,
                      play_board.GetFromPosition, -1)
    self.assertRaises(board.InvalidBoardPosition,
                      play_board.GetFromPosition, 9)

  def testValidGetFromPosition(self):
    play_board = board.Board(3)
    play_board.SetPosition(1, board.BoardValue.X)
    self.assertEqual(board.BoardValue.X, play_board.GetFromPosition(1))

  def testInvalidGetFromCoordinates(self):
    play_board = board.Board(3)
    self.assertRaises(board.InvalidBoardPosition,
                      play_board.GetFromCoordinates, -1, -1)
    self.assertRaises(board.InvalidBoardPosition,
                      play_board.GetFromCoordinates, 9, 9)

  def testValidGetFromCoordinates(self):
    play_board = board.Board(3)
    play_board.SetPosition(1, board.BoardValue.X)
    self.assertEqual(board.BoardValue.X, play_board.GetFromCoordinates(0, 1))

  def testIsFull(self):
    play_board = board.Board(3)
    for position in xrange(9):
      self.assertFalse(play_board.IsFull())
      play_board.SetPosition(position, board.BoardValue.X)
    self.assertTrue(play_board.IsFull())

  def testIsValidMoveFromPosition(self):
    play_board = board.Board(3)
    self.assertTrue(play_board.IsValidMoveFromPosition(1))
    play_board.SetPosition(1, board.BoardValue.X)
    self.assertFalse(play_board.IsValidMoveFromPosition(1))

  def testIsValidMoveFromCoordinates(self):
    play_board = board.Board(3)
    self.assertTrue(play_board.IsValidMoveFromCoordinates(0, 1))
    play_board.SetCoordinates(0, 1, board.BoardValue.X)
    self.assertFalse(play_board.IsValidMoveFromCoordinates(0, 1))

  def testIsWinner(self):
    play_board = board.Board(3)
    self.assertEqual(board.BoardValue.NONE, play_board.IsWinner())

    # Test winner case.
    play_board.SetPosition(0, board.BoardValue.X)
    play_board.SetPosition(1, board.BoardValue.X)
    play_board.SetPosition(2, board.BoardValue.X)
    self.assertEqual(board.BoardValue.X, play_board.IsWinner())

    # Test a draw case.
    play_board = board.Board(3)
    play_board.SetPosition(0, board.BoardValue.X)
    play_board.SetPosition(1, board.BoardValue.O)
    play_board.SetPosition(2, board.BoardValue.X)
    play_board.SetPosition(3, board.BoardValue.X)
    play_board.SetPosition(4, board.BoardValue.O)
    play_board.SetPosition(5, board.BoardValue.X)
    play_board.SetPosition(6, board.BoardValue.O)
    play_board.SetPosition(7, board.BoardValue.X)
    play_board.SetPosition(8, board.BoardValue.O)
    self.assertIsNone(play_board.IsWinner())

  def testIsDescendingDiagonalPossible(self):
    play_board = board.Board(3)
    self.assertEqual(0, play_board.IsDescendingDiagonalPossible(
        board.BoardValue.X))
    play_board.SetPosition(0, board.BoardValue.O)
    self.assertEqual(-1, play_board.IsDescendingDiagonalPossible(
        board.BoardValue.X))
    self.assertEqual(1, play_board.IsDescendingDiagonalPossible(
        board.BoardValue.O))

  def testIsAscendingDiagonalPossible(self):
    play_board = board.Board(3)
    self.assertEqual(0, play_board.IsAscendingDiagonalPossible(
        board.BoardValue.X))
    play_board.SetPosition(2, board.BoardValue.O)
    self.assertEqual(-1, play_board.IsAscendingDiagonalPossible(
        board.BoardValue.X))
    self.assertEqual(1, play_board.IsAscendingDiagonalPossible(
        board.BoardValue.O))

  def testIsRowPossible(self):
    play_board = board.Board(3)
    self.assertEqual(0, play_board.IsRowPossible(0, board.BoardValue.X))
    play_board.SetPosition(2, board.BoardValue.O)
    self.assertEqual(-1, play_board.IsRowPossible(0, board.BoardValue.X))
    self.assertEqual(1, play_board.IsRowPossible(0, board.BoardValue.O))

  def testIsColumnPossible(self):
    play_board = board.Board(3)
    self.assertEqual(0, play_board.IsColumnPossible(0, board.BoardValue.X))
    play_board.SetPosition(2, board.BoardValue.O)
    self.assertEqual(-1, play_board.IsColumnPossible(2, board.BoardValue.X))
    self.assertEqual(1, play_board.IsColumnPossible(2, board.BoardValue.O))


if __name__ == '__main__':
  unittest.main()
