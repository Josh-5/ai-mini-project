#follow to install pytience
#https://pypi.org/project/pytience/
# Here's another option to run the solitaire game

#follow this to install pytorch
#https://pytorch.org/get-started/locally/

# Use subprocess to interact: https://docs.python.org/3/library/subprocess.html

import subprocess
import time

# Move all cards to foundations if they're all face up
def solve(game):
    game.stdin.write("solve")
    delay(game)

# Move a card from the origin tableau to the (suit) foundation
def foundation(game, suit:str, origin:int):
    game.stdin.write("foundation " + suit + " " + str(origin))
    delay(game)

# Draw a card from the stock
def deal(game):
    game.stdin.write("deal")
    delay(game)

# Move the top card from the stock to a destination tableau
def waste(game, destination:int):
    game.stdin.write("waste " + str(destination))
    delay(game)

# Undo the most recent move
def undo(game):
    game.stdin.write("undo\n")
    delay(game)

# Creates a new game
def restart(game):
    game.stdin.write("new\n")
    delay(game)

# Move the card at the index "card" from the origin tableau to the destination tableau
def move(game, origin:int, card:int, destination:int):
    game.stdin.write("t " + str(origin) + " " + str(card) + " " + str(destination) + "\n")
    delay(game)

# Internal sleeping to show the moves more clearly
def delay(game):
    game.stdin.flush()
    time.sleep(1)

def main():
    """
    https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate

    Moves can be written as long as stdin is open. 

    """
    # Startup
    game = subprocess.Popen(["klondike"], stdin=subprocess.PIPE, text=True)
    restart(game)


    move(game, 1,0,0)
    move(game, 0,0,1)





    # Shutdown
    game.stdin.close()
    game.wait()


if __name__ == "__main__":
    main()