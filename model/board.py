"""Model that represents a Tic Tac Toe board."""

__author__ = "Rishi Sharma (rishisharma@gmail.com)"


class InvalidBoardSetting(Exception):
  """Thrown when an invalid setting is attempted on the Board."""


class InvalidBoardPosition(Exception):
  """Thrown when an invalid position is found on the Board."""


class BoardValue(object):
  """Defines the valid board values."""

  NONE, O, X = xrange(3)
  ALL_VALUES = (NONE, O, X)

  @staticmethod
  def ToString(board_value):
    """Converts an enumeration value into its string counterpart.

    Args:
      board_value: A BoardValue to be converted into a string representation.

    Returns:
      A string representation of the board value.

    Raises:
      InvalidBoardSetting if the value is not a BoardValue.
    """

    if board_value == BoardValue.NONE:
      return " "
    if board_value == BoardValue.O:
      return "O"
    if board_value == BoardValue.X:
      return "X"

    raise InvalidBoardSetting()


class UserSentinel(object):
  """Object structure used for determination of winner in O(1) time."""

  def __init__(self, dimension):
    """Initializes the sentinel.

    Args:
      dimension: The dimension of the Board object.
    """

    self.dimension = dimension
    self.row_counter = [0] * dimension
    self.col_counter = [0] * dimension
    self.diagonal_desc_counter = 0
    self.diagonal_asc_counter = 0
    self.is_winner = False

  def Update(self, row, col):
    """Updates the various trackers with the result of a move on the board.

    Note: This does not validate the row/col pair.

    Args:
      row: The row the play was made in.
      col: The column the play was made in.
    """

    self.row_counter[row] += 1
    self.col_counter[col] += 1
    if row == col:
      self.diagonal_desc_counter += 1
    if self.dimension - col - 1 == row:
      self.diagonal_asc_counter += 1

    self.is_winner = self.dimension in (self.row_counter[row],
                                        self.col_counter[col],
                                        self.diagonal_desc_counter,
                                        self.diagonal_asc_counter)

  def IsWinner(self):
    """Indicates whether this user has won.

    Returns:
      True if the user has won, False otherwise.
    """

    return self.is_winner


class Board(object):
  """A Tic Tac Toe Board."""

  DEFAULT_DIMENSION = 3

  def __init__(self, dimension=None):
    """Initialize the tic tac toe board.

    Args:
      dimension: The length of the board to be played.  If None the default
          value of Board.DEFAULT_DIMENSION is used.
    """

    self._board = []
    self._set_counter = 0
    self._user_x_sentinel = UserSentinel(dimension)
    self._user_o_sentinel = UserSentinel(dimension)

    if dimension is None:
      dimension = Board.DEFAULT_DIMENSION

    if dimension < 1:
      raise RuntimeError("Dimension must be greater than 0.")

    self.dimension = dimension

    # Pre-fill the board with the proper values
    for i in xrange(self.dimension):
      row = [BoardValue.NONE] * self.dimension
      self._board.append(row)

  def ToPosition(self, row, col):
    """Converts the row/col coordinate into an absolute one.

    Args:
      row: The row of the board.
      col: the column of the board.

    Returns:
      An integer representation of the row, col pair if the top row is started
      with a 0 representation and each row below begins with
      self.dimension * row value.

    Raises:
      InvalidBoardPosition if the row, column pair are invalid.
    """

    if 0 <= row < self.dimension or 0 <= col < self.dimension:
      return self.dimension * row + col
    raise InvalidBoardPosition()

  def ToCoordinates(self, position):
    """Converts an absolute position into a valid row, column pair.

    Args:
      position: A 0 based integer position on the board.

    Returns:
      A tuple containing the row, column equivalent of the position
      on the board.

    Raises:
      InvalidBoardPosition if the position is invalid.
    """

    if 0 <= position <= self.dimension * self.dimension - 1:
      row = int(position / self.dimension)
      col = int(position % self.dimension)
      return row, col
    raise InvalidBoardPosition()

  def SetPosition(self, position, board_value):
    """Sets the position on the board with the given board_value.

    Args:
      position: The position to set on the board.
      board_value: A BoardValue to set on that position.

    Raises:
      InvalidBoardPosition if the position is invalid.
      InvalidBoardSetting if the position is already taken.
    """

    row, col = self.ToCoordinates(position)
    self.SetCoordinates(row, col, board_value)

  def SetCoordinates(self, row, col, board_value):
    """Sets the row, column coordinates with the given value.

    The board is represented as row, col coordinates such that
    0, 0 is the top left and 2, 2 is the bottom right.

    For a 3x3 board this looks like:

    0,0 | 0,1 | 0,2
    1,0 | 1,1 | 1,2
    2,0 | 2,1 | 2,2

    Args:
      row: The row coordinate on the board to set the value to.
      col: The col coordinate on the board to set the value to.
      board_value: A BoardValue to set in position x,y.

    Raises:
      InvalidBoardSetting if the position is already taken.
    """

    if board_value not in BoardValue.ALL_VALUES:
      raise InvalidBoardSetting("board_value parameter is not of expected type")

    if (not (0 <= row < self.dimension)
        or not (0 <= row < self.dimension)):
      raise InvalidBoardPosition()

    if self._board[row][col] != BoardValue.NONE:
      raise InvalidBoardSetting("row: %s, col: %s" % (row, col))

    self._board[row][col] = board_value
    self._set_counter += 1
    if board_value == BoardValue.X:
      self._user_x_sentinel.Update(row, col)
    elif board_value == BoardValue.O:
      self._user_o_sentinel.Update(row, col)

  def GetFromPosition(self, position):
    """Retrieves a board value from the position.

    Args:
      position: The position on the board to retrieve the board value of.

    Returns:
      A BoardValue associated with the inputted position.

    Raises:
      InvalidBoardPosition if the position is invalid.
    """

    row, col = self.ToCoordinates(position)
    return self.GetFromCoordinates(row, col)

  def GetFromCoordinates(self, row, col):
    """Retrieves a board value from the row and column.

    Args:
      row: The row coordinate on the board to get the value of.
      col: The col coordinate on the board to get the value of.

    Raises:
      InvalidBoardPosition if the row, col is invalid.
    """

    if 0 <= row < self.dimension or 0 <= col < self.dimension:
      return self._board[row][col]
    raise InvalidBoardPosition()

  def IsFull(self):
    """Returns True if no further moves can be made on the board."""

    return self._set_counter == (self.dimension * self.dimension)

  def IsValidMoveFromPosition(self, position):
    """Determines if the spot referred to by a given position is available.

    Args:
      position: The position on the board to check.

    Returns:
      True if a move can be made at that position, False otherwise.

    Raises:
      InvalidBoardPosition if the position is invalid.
    """

    return self.GetFromPosition(position) == BoardValue.NONE

  def IsValidMoveFromCoordinates(self, row, col):
    """Determines if the spot referred to by a given position is available.

    Args:
      row: The row coordinate on the board.
      col: The col coordinate on the board.

    Returns:
      True if a move can be made at that position, False otherwise.

    Raises:
      InvalidBoardPosition if the row, col pair is invalid.
    """

    return self.GetFromCoordinates(row, col) == BoardValue.NONE

  def IsWinner(self):
    """Determines if the board has a winner.

    Returns:
      The winner as represented by BoardValue. None if it is a draw, and
      BoardValue.NONE if moves can still be made.
    """

    if self._user_x_sentinel.IsWinner():
      return BoardValue.X
    if self._user_o_sentinel.IsWinner():
      return BoardValue.O
    if self.IsFull():
      return None

    # Check to see if we can short circuit
    # if a draw (i.e no winners can be had).
    threshold_check = self.dimension * 2
    if self._set_counter >= threshold_check:
      for board_value in (BoardValue.X, BoardValue.O):
        for index in xrange(self.dimension):
          row_val = self.IsRowPossible(index, board_value)
          col_val = self.IsColumnPossible(index, board_value)
          if row_val > -1 or col_val > -1:
            return BoardValue.NONE
        if (self.IsAscendingDiagonalPossible(board_value) > -1
            or self.IsDescendingDiagonalPossible(board_value) > -1):
          return BoardValue.NONE
      return None

    return BoardValue.NONE

  def IsDescendingDiagonalPossible(self, board_value):
    """Determines if the user can still win the descending diagonal.

    Args:
      board_value: The BoardValue that represents the user.

    Returns:
      Number of positions occupied by the user.  -1 if the user cannot win.
    """

    if (board_value == BoardValue.X
        and self._user_o_sentinel.diagonal_desc_counter == 0):
      return self._user_x_sentinel.diagonal_desc_counter
    if (board_value == BoardValue.O
        and self._user_x_sentinel.diagonal_desc_counter == 0):
      return self._user_o_sentinel.diagonal_desc_counter

    return -1

  def IsAscendingDiagonalPossible(self, board_value):
    """Determines if the user can still win the ascending diagonal.

    Args:
      board_value: The BoardValue that represents the user.

    Returns:
      Number of positions occupied by the user.  -1 if the user cannot win.
    """

    if (board_value == BoardValue.X
        and self._user_o_sentinel.diagonal_asc_counter == 0):
      return self._user_x_sentinel.diagonal_asc_counter
    if (board_value == BoardValue.O
        and self._user_x_sentinel.diagonal_asc_counter == 0):
      return self._user_o_sentinel.diagonal_asc_counter

    return -1

  def IsRowPossible(self, row, board_value):
    """Determines if the user can still win the row.

    Args:
      board_value: The BoardValue that represents the user.

    Returns:
      Number of positions occupied by the user.  -1 if the user cannot win.
    """

    if (board_value == BoardValue.X
        and self._user_o_sentinel.row_counter[row] == 0):
      return self._user_x_sentinel.row_counter[row]
    if (board_value == BoardValue.O
        and self._user_x_sentinel.row_counter[row] == 0):
      return self._user_o_sentinel.row_counter[row]

    return -1

  def IsColumnPossible(self, col, board_value):
    """Determines if the user can still win the row.

    Args:
      board_value: The BoardValue that represents the user.

    Returns:
      Number of positions occupied by the user.  -1 if the user cannot win.
    """

    if (board_value == BoardValue.X
        and self._user_o_sentinel.col_counter[col] == 0):
      return self._user_x_sentinel.col_counter[col]
    if (board_value == BoardValue.O
        and self._user_x_sentinel.col_counter[col] == 0):
      return self._user_o_sentinel.col_counter[col]

    return -1

  def __str__(self):
    """String override to pretty print the board."""

    rv = ""
    index = 0
    for row in self._board:
      for col in row:
        if col == BoardValue.NONE:
          rv += "%03d | " % index
        else:
          rv += " " + BoardValue.ToString(col) + "  | "
        index += 1
      rv = rv[:-2] + "\n"
    return rv
