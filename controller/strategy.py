"""Strategies for the tic tac toe game."""

__author__ = "Rishi Sharma (rishsharma@gmail.com)"

import random

from controller import heuristics
from model import board


class StrategyError(Exception):
  """Thrown when a strategy error occurs."""


class Strategy(object):
  """Strategy to use to play."""

  RANDOM, HEURISTICS = xrange(2)


def GetNextMove(play_board, board_value, strategy=Strategy.HEURISTICS):
  """Returns the next move in absolute positioning given a board.

  Args:
    play_board: The board.Board being played.
    board_value: The board.BoardValue representing the user.
    strategy: The Strategy to use to generate the next move.

  Returns:
    An absolute position for the next move that should be made.

  Raises:
    StrategyError if no move can be made.
  """

  if play_board.IsFull():
    raise StrategyError("Play board is full. No moves can be made.")

  # Can I win?
  position = CanWin(play_board, board_value)
  if position >= 0:
    return position

  # Can I block?
  other_board_value = (board.BoardValue.X
                       if board_value == board.BoardValue.O
                       else board.BoardValue.O)
  position = CanWin(play_board, other_board_value)
  if position >= 0:
    return position

  if strategy == Strategy.RANDOM:
    return _RandomStrategy(play_board)

  return heuristics.GetBestPositionBasedOnHeuristics(play_board, board_value)


def _RandomStrategy(play_board):
  """Picks a random valid spot to make a move.

  Args:
    play_board: The board.Board that is in play.

  Returns:
    An absolute position for the next move that should be made.
  """

  while 1:
    num = int(random.random() * play_board.dimension * play_board.dimension)
    if play_board.IsValidMoveFromPosition(num):
      return num


def CanWin(play_board, board_value):
  """Determines if the user represented by the board_value can win.

  Args:
    play_board: The board.Board that is in play.
    board_value: The board.BoardValue representing the user.

  Returns:
    A position that will allow the user to win. -1 if the user cannot win yet.
  """

  # Check if we can win by examining the rows.
  for row in xrange(play_board.dimension):
    num_set = play_board.IsRowPossible(row, board_value)
    if num_set == play_board.dimension - 1:
      # Found the row, now find the column and win the game.
      for col in xrange(play_board.dimension):
        if play_board.IsValidMoveFromCoordinates(row, col):
          return play_board.ToPosition(row, col)

  # Check if we can win by examining the cols.
  for col in xrange(play_board.dimension):
    num_set = play_board.IsColumnPossible(col, board_value)
    if num_set == play_board.dimension - 1:
      # Found the column, now find the row and win the game.
      for row in xrange(play_board.dimension):
        if play_board.IsValidMoveFromCoordinates(row, col):
          return play_board.ToPosition(row, col)

  # Check descending diagonal.
  num_set = play_board.IsDescendingDiagonalPossible(board_value)
  if num_set == play_board.dimension - 1:
    for index in xrange(play_board.dimension):
      if play_board.IsValidMoveFromCoordinates(index, index):
        return play_board.ToPosition(index, index)

  # Check ascending diagonal.
  num_set = play_board.IsAscendingDiagonalPossible(board_value)
  if num_set == play_board.dimension - 1:
    for index in xrange(play_board.dimension):
      if play_board.IsValidMoveFromCoordinates(
          play_board.dimension - index - 1, index):
        return play_board.ToPosition((play_board.dimension - index - 1), index)

  return -1
