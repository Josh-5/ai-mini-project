#follow to install pytience
#https://pypi.org/project/pytience/
# Here's another option to run the solitaire game

#follow this to install pytorch
#https://pytorch.org/get-started/locally/

# Use subprocess to interact: https://docs.python.org/3/library/subprocess.html

import subprocess
import time

def delay(game):
    game.stdin.flush()
    time.sleep(1)

def main():
    """
    https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate

    Moves can be written as long as stdin is open. 

    """
    game = subprocess.Popen(["klondike"], stdin=subprocess.PIPE, text=True)
    game.stdin.write("t 1 0 0\n")
    delay(game)
    game.stdin.write("t 0 0 1\n")
    delay(game)
    game.stdin.close()
    game.wait()


if __name__ == "__main__":
    main()