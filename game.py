#follow to install pytience
#https://pypi.org/project/pytience/
# Here's another option to run the solitaire game

#follow this to install pytorch
#https://pytorch.org/get-started/locally/

# Use subprocess to interact: https://docs.python.org/3/library/subprocess.html

# The game uses _dump to give a JSON representation of the game. https://docs.python.org/3/library/json.html

import subprocess
import os
import time
import json
import pytience.games.solitaire.klondike as klondike

# Move all cards to foundations if they're all face up
def solve(game):
    game.stdin.write("solve\n")
    delay(game)

# Move a card from the origin tableau to the (suit) foundation
def foundation(game, suit:str, origin:int):
    game.stdin.write("foundation " + suit + " " + str(origin) + "\n")
    delay(game)

# Draw a card from the stock
def deal(game):
    game.stdin.write("deal\n")
    delay(game)

# Move the top card from the stock to a destination tableau
def waste(game, destination:int):
    game.stdin.write("waste " + str(destination) + "\n")
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

def startup():
    solitaire = subprocess.Popen(["klondike"], stdin=subprocess.PIPE,text=True)
    # restart(solitaire)
    return solitaire

def shutdown(game):
    game.stdin.write("quit\n")
    game.stdin.close()
    game.wait()

def dump(game):
    # use _dump to get the game state
    # This shows hidden cards. Make sure to not use the cards with prefix |.
    # game.stdin.write("_dump\n")
    # delay(game)
    # json = process.stdout.readline()
    # delay(game)
    klondikeGame = klondike.KlondikeGame()
    return klondikeGame.dump()
    

def main():
    """
    https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate

    Moves can be written as long as stdin is open. 

    """
    # Startup
    game = startup()


    # Game
    json = dump(game)
    





    # Shutdown
    shutdown(game)


    print()
    print()
    print()
    print()
    print()
    print(json)

if __name__ == "__main__":
    main()