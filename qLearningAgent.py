# follow to install pytience
# https://pypi.org/project/pytience/

# game.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import json
import random
import time
from pytience.cmd.klondike import KlondikeCmd, KlondikeGame
from pytience.cards import deck
from pytience.games.solitaire import tableau
from pytience.games.solitaire import CARD_VALUES

import util




class KlondikeController(KlondikeCmd):
    def __init__(self):
        KlondikeCmd.__init__(self)
        self.replenishFlag = 0  # Indicates how many times we have replenished the deck/stock
        self.stateCounts = util.Counter()
    
    """ Helper method to check whether we can move a source card to a destination card"""
    def canMove(self, src: deck.Card, dest: deck.Card, destIsFoundation=False) -> bool:
        if destIsFoundation:
            return CARD_VALUES[dest.pip] == CARD_VALUES[src.pip] - 1
        else:
            return (dest.color != src.color) and (CARD_VALUES[dest.pip] - 1 == CARD_VALUES[src.pip])
    
    """ Helper method to check whether a card is Ace """
    def isAce(self, card: deck.Card) -> bool:
        return CARD_VALUES[card.pip] == 1
    
    def isKing(self, card: deck.Card) -> bool:
        return CARD_VALUES[card.pip] == 13
    
    def getLegalActions(self: KlondikeCmd):
        legalActions: list[str] = []

        if self.klondike.is_solvable():
            legalActions.append("S")
            return legalActions
        
        # When there are still remaining cards in the stock or waste pile
        if self.klondike.stock.remaining > 0 or len(self.klondike.waste) > 0:
            legalActions.append("D")

        # When waste pile is not empty
        if len(self.klondike.waste) > 0:
            topWaste: deck.Card = self.klondike.waste[-1]

            # Tries putting card from waste to foundation
            foundationPile = self.klondike.foundation.piles[topWaste.suit]
         
            if self.isAce(topWaste) or foundationPile != [] and self.canMove(topWaste, foundationPile[-1], True):
                legalActions.append("W F")
        
            # Tries putting card from waste to tableu piles
            for i, tableauPile in enumerate(self.klondike.tableau.piles):
                if tableauPile == []:
                    if self.isKing(topWaste):
                        legalActions.append(f"W {i}")
                elif self.canMove(topWaste, tableauPile[-1], False):
                    legalActions.append(f"W {i}")

        # Moves cards from foundation piles 
        for suit, foundationPile in self.klondike.foundation.piles.items():
     
            if foundationPile == []:
                continue
            # Move to tableau piles if applicable
            for j, tableauPile in enumerate(self.klondike.tableau.piles):
                if tableauPile == []:
                    continue
                topFoundation: deck.Card = foundationPile[-1]
                topTableau: deck.Card = tableauPile[-1]
                if self.canMove(topFoundation, topTableau, False):
                    legalActions.append(f"F {suit} {j}")

        # Moves cards from tableau piles
        for i, tableauPile in enumerate(self.klondike.tableau.piles):
            if len(tableauPile) == 0:
                continue
            
            print(f"{i}: {tableauPile}")
            j = len(tableauPile) - 1
            while j >= 0:
                print(tableauPile)
                print(j)
                tableauCard = tableauPile[j]
                # Stops completely for the pile once a concealed card is hit
                if tableauCard.is_concealed:
                    break

                # Only when it is the top card do you try moving to foundation piles
                if j == len(tableauPile) - 1:
                    # Possible moves to foundation piles
                    foundationPile = self.klondike.foundation.piles[tableauCard.suit]
                    
                    if self.isAce(tableauCard) or foundationPile != [] and self.canMove(tableauCard, foundationPile[-1], True):
                        legalActions.append(f"T {i} {j} F")
                    

                # Possible moves to another tableau pile
                for k, tableauPile2 in enumerate(self.klondike.tableau.piles):
                    # Skips the same pile
                    if k == i or tableauPile2 == []:
                        continue
                    if self.canMove(tableauCard, tableauPile2[-1], False):
                        legalActions.append(f"T {i} {j} {k}")
                j -= 1
                    
        return legalActions

    def performAction(self, action, game=None):
        # this is for FeatureExtractor
        if game is not None:
            self.klondike = game
        parsedAction = action.split()

        if (parsedAction[0] == "D"):
            # The klondike replenishes when there are still waste cards but no cards in deck/stock
            if self.klondike.stock.remaining == 0 and len(self.klondike.waste) > 0:
                self.replenishFlag += 1
            self.klondike.deal()

        elif (parsedAction[0] == "F"):
            self.klondike.select_foundation(deck.Suit(parsedAction[1]), int(parsedAction[2]))
        elif (parsedAction[0] == "W"):
            if parsedAction[1] == "F":
                self.klondike.select_waste(None)
            else:
                self.klondike.select_waste(int(parsedAction[1]))
            self.replenishFlag = 0
        elif (parsedAction[0] == "T"):
            if parsedAction[3] == "F":
                self.klondike.select_tableau(int(parsedAction[1]), int(parsedAction[2]), None)
            else:
                self.klondike.select_tableau(int(parsedAction[1]), int(parsedAction[2]), int(parsedAction[3]))

        elif (parsedAction[0] == "S"):
            self.klondike.solve()

    def hasLost(self: KlondikeCmd, allowedRepetitions=300):
        if self.replenishFlag == 2:
            return True
        
        currentState = json.dumps(self.klondike.dump())
        
        if self.stateCounts[currentState] >= allowedRepetitions:
            return True
        self.stateCounts[currentState] += 1

        return False

    
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

    def getFeatures(self, state, action):
        gameUI = KlondikeController()
        game = KlondikeGame(game_dump=state)
        print("\n\nfeature extract\n")
        print(game.foundation.dump())
        print(game.tableau.dump())
        print(action)
        print("\n\n\n")
        gameUI.performAction(action, game)
        features = util.Counter()
        tableaus = game.tableau.piles
        features["bias"] = 1.0

        hiddenCardsPre = 0.0
        for tableau in tableaus:
            for card in tableau:
                if not card.is_revealed:
                    hiddenCardsPre += 1.0

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

        


        features.divideAll(10.0)
        return features


class QLearningAgent():
    def __init__(self, featExtractor=SimpleExtractor(), numTraining=100, epsilon=0.5, epsilonDecay=0.995, epsilonMin=0.01, alpha=0.5, gamma=1, legalActions=[]):
        """
        actionFn: Function which takes a state and returns the list of legal actions

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """

        # Training related variables 
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
       
        # Hyperparamters
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.epsilonDecay = float(epsilonDecay)
        self.epsilonMin = float(epsilonMin)
        self.featExtractor = featExtractor

        self.weights = util.Counter()
        self.legalActions = legalActions
  
    def setLegalActions(self, actions):
        self.legalActions = actions

    def getQValue(self, state, action):
        """
        Should return Q(state,action)
        """
        q = 0
        features = self.featExtractor.getFeatures(state, action)
        for feature in features:
            q += features[feature] * self.weights[feature]
        return q


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.legalActions

        # If there are no legal actions (terminal state), return 0.0
        if (len(legalActions) == 0):
            return 0.0
        
        # Loop through all legal actions, find and return the greatest Q value
        maxQ = -999999
        for action in legalActions:
            q = self.getQValue(state, action)
            if (q > maxQ):
                maxQ = q
        return maxQ

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.legalActions
        bestAction = None

        # If there are no legal actions (terminal state), return 0.0
        if (len(legalActions) == 0):
            return None
        
        # The best action has the greatest Q value. 
        # Loop through all legal actions, find and return the action with the greatest Q value
        bestQ = -999999
        for action in legalActions:
            q = self.getQValue(state, action)
            if (q > bestQ):
                bestAction = action
                bestQ = q
        return bestAction
        
    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.legalActions
        action = None
        "*** YOUR CODE HERE ***"
        # If there are no legal actions, return None
        if (len(legalActions) == 0):
            return None
        
        # Pick the best move
        action = self.computeActionFromQValues(state)

        # Epsilon chance of picking a random move
        if (util.flipCoin(self.epsilon)):
            action = random.choice(legalActions)
            
        return action
    #TODO verify
    def update(self, state, action, nextState, reward: float):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
        diff = (reward + (self.discount*self.computeValueFromQValues(nextState))) - self.getQValue(state, action)
        for feature in features:
            # Question for TAs: I had to move the diff calc outside of the loop. Why doesn't it work inside the loop?
            self.weights[feature] = self.weights[feature] + (self.alpha*diff*features[feature])

    def getPolicy(self):
        return self.computeActionFromQValues()
    def getValue(self):
        return self.computeValueFromQValues()


    # Training
    def observeTransition(self, state, action, nextState, deltaReward, legalActions):
        """
            Called by environment to inform agent that a transition has
            been observed. This will result in a call to self.update
            on the same arguments

            NOTE: Do *not* override or call this function
        """
        self.legalActions = legalActions
        self.episodeRewards += deltaReward
        self.update(state, action, nextState, deltaReward)

    def startEpisode(self):
        """
          Called by environment when new episode is starting
        """
        self.episodeRewards = 0.0

    def stopEpisode(self):
        """
          Called by environment when episode is done
        """
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            # Take off the training wheels
            self.epsilon = 0.0    # no exploration
            self.alpha = 0.0      # no learning

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()


def main():
    game = KlondikeController()
    print(game.klondike.dump())
    print(f"\n\n\n{game.getLegalActions()}")

if __name__ == "__main__":
    main()
