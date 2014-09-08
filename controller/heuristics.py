"""
Heuristics based approach to tic tac toe.  This is based on the work
of Philip S Tellis and as such does not use look ahead logic.
It is however modified from his approach in a few ways.  This approach
should be more efficient based on optimizations made to the board.
"""

__author__ = "Rishi Sharma (rishsharma@gmail.com)"


from model import board


class Heuristic(object):
  """Heuristic enumeration used as weighted values for the next move."""

  WIN = 40
  BLOCK = 20
  CENTER = 16
  CORNER = 4
  LINE = 10
  LOCALITY = 14
  INVALID = 0


def GetCenterValue(position, play_board):
  """Returns a score if the position represents the center.

  Args:
    position: The position on the board.
    play_board: The board.Board that is in play.
  """

  center = int(play_board.dimension * play_board.dimension / 2)
  if position == center and play_board.IsValidMoveFromPosition(position):
    return Heuristic.CENTER
  return Heuristic.INVALID


def GetCornerValue(position, play_board):
  """Returns a score if the position represents a corner value.

  Args:
    position: The position on the board.
    play_board: The board.Board that is in play.
  """

  if (play_board.IsValidMoveFromPosition(position)
      and position % (play_board.dimension - 1) == 0
      and position != int(play_board.dimension * play_board.dimension / 2)):
    return Heuristic.CORNER
  return Heuristic.INVALID


def _GetRelativeRowHeuristic(position, play_board, board_value):
  """Returns a score of based on the position in the row.

  The more and closer the same values are the better.

  Args:
    position: The position on the board.
    play_board: The board.Board that is in play.
    board_value: The board.BoardValue of the user.
  """

  row_num, col_num = play_board.ToCoordinates(position)
  if play_board.IsRowPossible(row_num, board_value) == -1:
    return Heuristic.INVALID

  # Calculate relative distances.  The closer values are the better.
  value = 0
  for col in xrange(play_board.dimension):
    if col == col_num:
      continue  # Skip the actual position.
    if play_board.GetFromCoordinates(row_num, col) == board_value:
      value += play_board.dimension - abs(col - col_num)

  if value:
    return value + Heuristic.LINE

  return 0


def _GetRelativeColumnHeuristic(position, play_board, board_value):
  """Returns a score of based on the position in the column.

  The more and closer the same values are the better.

  Args:
    position: The position on the board.
    play_board: The board.Board that is in play.
    board_value: The board.BoardValue of the user.
  """

  row_num, col_num = play_board.ToCoordinates(position)
  if play_board.IsColumnPossible(col_num, board_value) == -1:
    return Heuristic.INVALID

  # Calculate relative distances.  The closer values are the better.
  value = 0
  for row in xrange(play_board.dimension):
    if row == row_num:
      continue  # Skip the actual position.
    if play_board.GetFromCoordinates(row, col_num) == board_value:
      value += play_board.dimension - abs(row - row_num)

  if value:
    return value + Heuristic.LINE

  return 0


def _GetDiagonalHeuristic(position, play_board, board_value):
  """Returns a score of based on the position and the diagonals.

  The more and closer the same values are the better.

  Args:
    position: The position on the board.
    play_board: The board.Board that is in play.
    board_value: The board.BoardValue of the user.
  """

  if (play_board.IsDescendingDiagonalPossible(board_value) < 0 or
      play_board.IsAscendingDiagonalPossible(board_value) < 0):
    return Heuristic.INVALID

  row, col = play_board.ToCoordinates(position)
  if row != col and row != play_board.dimension - col - 1:
    return Heuristic.INVALID

  value = 0

  # Descending diagonal.
  if row == col:
    for index in xrange(play_board.dimension):
      if index == row and index == col:
        continue  # Skip the actual position.
      if play_board.GetFromCoordinates(index, index) == board_value:
        value += play_board.dimension - abs(index - row)

  # Ascending diagonal.
  if row == play_board.dimension - col - 1:
    for index in xrange(play_board.dimension):
      if index == row and col == play_board.dimension - index - 1:
        continue  # Skip the actual position.
      if (play_board.GetFromCoordinates(
          index, play_board.dimension - index - 1) == board_value):
        value += play_board.dimension - abs(index - row)

  return value


def GetLineValue(position, play_board, board_value):
  """Returns a consolidate score of row, column and diagonals.

  Args:
    position: The position on the board.
    play_board: The board.Board that is in play.
    board_value: The board.BoardValue of the user.
  """

  if play_board.IsValidMoveFromPosition(position):
    return (_GetRelativeRowHeuristic(position, play_board, board_value)
            + _GetRelativeColumnHeuristic(position, play_board, board_value)
            + _GetDiagonalHeuristic(position, play_board, board_value))

  return Heuristic.INVALID


def GetLocalityValue(position, play_board, board_value):
  """Returns a score based on the 8 blocks that surround the selected position.

  Args:
    position: The position on the board.
    play_board: The board.Board that is in play.
    board_value: The board.BoardValue of the user.
  """

  if not play_board.IsValidMoveFromPosition(position):
    return Heuristic.INVALID

  value = 0
  row, col = play_board.ToCoordinates(position)
  block_map = [
      (row - 1, col -1),
      (row - 1, col),
      (row - 1, col + 1),
      (row, col - 1),
      (row, col + 1),
      (row + 1, col -1),
      (row + 1, col),
      (row + 1, col + 1)]
  for crow, ccol in block_map:
    if (crow < 0 or ccol < 0
        or crow > play_board.dimension - 1
        or ccol > play_board.dimension - 1):
      continue  # Skip invalid positions.
    if (play_board.GetFromCoordinates(crow, ccol) not in
        (board_value, board.BoardValue.NONE)):
      value += Heuristic.LOCALITY

  return value


def GetBestPositionBasedOnHeuristics(play_board, board_value):
  """Determines the best move to make based on heuristics.

  Args:
    position: The position on the board.
    play_board: The board.Board that is in play.
    board_value: The board.BoardValue of the user.
  """

  best_position = 0
  best_value = 0
  for index in xrange(play_board.dimension * play_board.dimension):
    if play_board.IsValidMoveFromPosition(index):
      computed_value = (GetCenterValue(index, play_board)
                        + GetCornerValue(index, play_board)
                        + GetLineValue(index, play_board, board_value)
                        + GetLocalityValue(index, play_board, board_value))
      if computed_value >= best_value:
        best_value = computed_value
        best_position = index

  return best_position

