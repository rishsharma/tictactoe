"""String resources for the tic tac toe game."""


__author__ = "Rishi Sharma (rishsharma@gmail.com)"


from model import board


class StringResources(object):

  # TODO(rishsharma): Use gettext for i18n.

  YOU_STRING = "You have put an X in position %03d."
  I_STRING = "I will put an O in position %03d."


  WHERE_TO = ("Please make your move selection by "
              "entering a number corresponding to the place on the board: ")

  YOU_WIN = "You have beaten my poor AI!"
  I_WIN = "I have beaten you with my poor AI!"
  DRAW = "It was a draw!"

  WELCOME = "Welcome to Tic-Tac-Toe."
  DIMENSION = "Please enter the dimensions of the board: "

  PLAY_AGAIN = "Would you like to play again (y/n): "

  SUMMARY = "X Wins: %s, O Wins: %s, Draws: %s"

  def GetYouString(self, position):
    """Retrieves the corresponding you string.

    Args:
      position: The position the user place their move.
    """

    return StringResources.YOU_STRING % position

  def GetIString(self, position):
    """Retrieves the corresponding you string.

    Args:
      position: The position the user place their move.
    """

    return StringResources.I_STRING % position

  def GetWinnerString(self, board_value):
    """Returns a string that indicates the winner.

    Args:
      board_value: A model.board.BoardValue.
    """

    if board_value == board.BoardValue.X:
      return StringResources.YOU_WIN
    if board_value == board.BoardValue.O:
      return StringResources.I_WIN
    return StringResources.DRAW
