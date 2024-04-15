#follow to install pytience
#https://pypi.org/project/pytience/
# Here's another option to run the solitaire game

#follow this to install pytorch
#https://pytorch.org/get-started/locally/

# Use subprocess to interact: https://docs.python.org/3/library/subprocess.html

import subprocess
import time

def foundation(game, suit:str, origin:int):
    game.stdin.write("foundation " + suit + " " + str(origin))
    delay(game)

def deal(game):
    game.stdin.write("deal")
    delay(game)

def waste(game, destination:int):
    game.stdin.write("waste " + str(destination))
    delay(game)

def undo(game):
    game.stdin.write("undo\n")
    delay(game)

def restart(game):
    game.stdin.write("new\n")
    delay(game)

def move(game, origin:int, card:int, destination:int):
    game.stdin.write("t " + str(origin) + " " + str(card) + " " + str(destination) + "\n")
    delay(game)

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