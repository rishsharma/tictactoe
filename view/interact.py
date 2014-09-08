"""Interaction module that interfaces with the user."""

__author__ = "Rishi Sharma (rishsharma@gmail.com)"


from i18n import string_resources
from model import board


def GrabMove(play_board):
  """Returns an integer validated move from the user."""

  try:
    value = int(raw_input(string_resources.StringResources.WHERE_TO))
    if not play_board.IsValidMoveFromPosition(value):
      return GrabMove(play_board)
    return value
  except (ValueError, board.InvalidBoardPosition):
    return GrabMove(play_board)


def GrabDimension():
  """Returns am integer valid inputted dimension from the user."""

  try:
    value = int(raw_input(string_resources.StringResources.DIMENSION))
    if value < 2:
      return GrabDimension()
    return value
  except ValueError:
    return GrabDimension()


def Welcome():
  """Welcomes the user to the game."""

  print string_resources.StringResources.WELCOME


def DisplayBoard(play_board):
  """Displays the board to the user.

  Args:
    play_board: A model.board.Board object to display.
  """

  print play_board


def DisplayYouMove(next_move):
  """Displays the first player's move.

  Args:
    next_move: The next move the first player had made.
  """

  print string_resources.StringResources().GetYouString(next_move)


def DisplayIMove(next_move):
  """Displays the second player's move.

  Args:
    next_move: The next move the second player will make.
  """

  print string_resources.StringResources().GetIString(next_move)


def DisplayWinner(has_won):
  """Displays the winner.

  Args:
    has_won: A board.BoardValue indicating the winner.  X indicates the first
        player has won, O indicates the second player has won, and a NONE
        indicates the game was a draw.
  """

  print string_resources.StringResources().GetWinnerString(has_won)


def Summarize(x_wins, o_wins, draws):
  """Displays a message that indicates the full set of wins/losses/draws.

  Args:
    x_wins: The number of times the X player has won.
    o_wins: The number of times the O player has won.
    draws: The number of times a draw has occurred.
  """

  print string_resources.StringResources.SUMMARY % (x_wins, o_wins, draws)


def PlayAgain():
  """Displays a message asking if the user would like to play again.

    Returns:
      A boolean indicating True if yes, False if no.
  """

  value = raw_input(string_resources.StringResources.PLAY_AGAIN).lower()
  if value == "y":
    return True
  if value == "n":
    return False
  return PlayAgain()
