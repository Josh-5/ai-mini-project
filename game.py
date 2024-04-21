#follow to install pytience
#https://pypi.org/project/pytience/

from pytience.cmd.klondike import KlondikeCmd


def main():
    """
    Useful functions for game:
        game.deal() - deals a card into waste
        game.adjust_score(self, points: int) - could be useful for qlearning
        game.select_foundation(self, suit: Suit, tableau_destination_pile)
            move a card from the suited foundation to the tableau
        game.select_waste(self, destination pile) - Move the top waste card to the destination
        game.select_tableau(self, pile_num, card_num, destination_pile_num)
            takes a pile index, card index, and a destination index. Moves the card at card_num
            from source to destination
        game.is_solvable() - checks if all cards are face up
        game.solve() if is solvable, moves all cards to foundations
        game.dump() returns a json object representing the game:
            {
                "score": self.score,
                "stock": self.stock.dump(),
                "waste": list(map(str, self.waste)),
                "foundation": self.foundation.dump(),
                "tableau": self.tableau.dump(),
                "undo_stack": self.dump_undo_stack()
            }
    
    Useful functions for cmd:
        cmd.print_game() - prints game to gui
    

    NOTE: If your klondike game is the same after running python game.py multiple times, delete the save file in .pytience.
    NOTE 2: game.dump() is a json. Treat it like a dict. Doing print(dump["tableau"]["piles"][0]) gets you the 0th pile in the piles in the tableau.
    """

    # Startup
    cmd = KlondikeCmd()
    game = cmd.klondike

    
    cmd.print_game()
    dump = game.dump()
    print(dump)


if __name__ == "__main__":
    main()





