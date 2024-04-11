#follow to install pytience
#https://pypi.org/project/pytience/
# Here's another option to run the solitaire game

#follow this to install pytorch
#https://pytorch.org/get-started/locally/

# Use subprocess to interact: https://docs.python.org/3/library/subprocess.html

import subprocess
import time

def move(game, origin:int, card:int, pile:int):
    game.stdin.write("t " + str(origin) + " " + str(card) + " " + str(pile) + "\n")

def delay(game):
    game.stdin.flush()
    time.sleep(1)

def main():
    """
    https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate

    Moves can be written as long as stdin is open. 

    """
    game = subprocess.Popen(["klondike"], stdin=subprocess.PIPE, text=True)
    move(game, 1,0,0)
    delay(game)
    move(game, 0,0,1)
    delay(game)
    game.stdin.close()
    game.wait()


if __name__ == "__main__":
    main()