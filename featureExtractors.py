"""
This file is adapted from the Pacman AI project developed at UC Berkeley.
"""

import util 
from pytience.cmd.klondike import KlondikeGame
from pytience.cards import deck
from pytience.games.solitaire import tableau
from pytience.games.solitaire import CARD_VALUES

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class SimpleExtractor(FeatureExtractor):
    """
    Returns features:
        - number of hidden cards in each pile after the move
        - greatest number of hidden cards in a pile
        - If the move reveals a hidden card ***************
        - If the move ends in a foundation
        - Origin of the move
    """

    def getFeatures(self, game:KlondikeGame, action):
        features = util.Counter()
        tableaus = game.tableau.piles
        features["bias"] = 1.0

        parse = action.split()

        hiddenCardsPre = 0.0
        for tableau in tableaus:
            for card in tableau:
                if not card.is_revealed:
                    hiddenCardsPre += 1.0

        util.doAction(game, action)

        hiddenCards = 0.0
        maxHiddenCards = 0.0
        for tableau in tableaus:
            pileHiddenCards = 0.0
            for card in tableau:
                if not card.is_revealed:
                    hiddenCards += 1.0
                    pileHiddenCards += 1.0
            if maxHiddenCards < pileHiddenCards:
                maxHiddenCards = pileHiddenCards

        features["total hidden cards"] = hiddenCards
        features["max hidden cards"] = maxHiddenCards
        features["reveal hidden cards"] = hiddenCards < hiddenCardsPre

        if (action[0] == "D"):
            game.undo_deal()
        elif (action[0] == "F"):
            features["origin"] = int(parse[1])
            features["foundation"] += 1.0
            game.undo_select_foundation()
        elif (action[0] == "W"):
            game.undo_select_waste()
        elif (action[0] == "T"):
            features["origin"] = parse[1]
            game.undo_select_tableau()


        features.divideAll(10.0)
        return features
