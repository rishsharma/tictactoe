"""Tic Tac Toe"""

__author__ = "Rishi Sharma (rishsharma@gmail.com)"


import sys
import traceback

from controller import strategy
from model import board
from view import interact


def Main():
  """Execution block.

  Returns:
    An integer that represents the exit_code the application exits with.
  """

  x_wins = 0
  o_wins = 0
  draws = 0

  user_exit = False

  interact.Welcome()

  try:

    while not user_exit:
      dimension = int(interact.GrabDimension())
      play_board = board.Board(dimension)
      has_won = board.BoardValue.NONE
      while 1:
        interact.DisplayBoard(play_board)
        you_next_move = interact.GrabMove(play_board)
        play_board.SetPosition(you_next_move, board.BoardValue.X)
        interact.DisplayYouMove(you_next_move)

        # Check if won:
        has_won = play_board.IsWinner()
        if has_won != board.BoardValue.NONE:
          break

        i_next_move = strategy.GetNextMove(play_board, board.BoardValue.O)
        play_board.SetPosition(i_next_move, board.BoardValue.O)
        interact.DisplayIMove(i_next_move)

        # Check if won:
        has_won = play_board.IsWinner()
        if has_won != board.BoardValue.NONE:
          break

      interact.DisplayBoard(play_board)
      interact.DisplayWinner(has_won)
      if has_won == board.BoardValue.X:
        x_wins += 1
      elif has_won == board.BoardValue.O:
        o_wins += 1
      else:
        draws += 1

      user_exit = not interact.PlayAgain()

    interact.Summarize(x_wins, o_wins, draws)

  except Exception as ex:
    print "Unexpected Exception has occurred: %s" % ex
    traceback.print_exc()
    return 1
  return 0


if __name__ == "__main__":
  exit_code = Main()
  sys.exit(exit_code)
