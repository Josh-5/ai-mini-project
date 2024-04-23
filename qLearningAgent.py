# follow to install pytience
# https://pypi.org/project/pytience/

# game.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import random
import time
from pytience.cmd.klondike import KlondikeCmd
from pytience.cards import deck
from pytience.games.solitaire import tableau
from pytience.games.solitaire import CARD_VALUES

import util




class KlondikeController(KlondikeCmd):
    def __init__(self):
        KlondikeCmd.__init__(self)
        self.replenishFlag = 0  # Indicates how many times we have replenished the deck/stock
    
    def getLegalActions(self):
        legalActions = []
        if (self.klondike.stock.remaining > 0) or (len(self.klondike.waste) > 0) :
            legalActions.append(["D"])
        if (len(self.klondike.waste) > 0) :
            for suit in self.klondike.foundation.piles.keys() :
                pile = self.klondike.foundation.piles[suit]
                if len(pile) > 0 :
                    #Check if card in pile is one less than one in waste
                else :
                    #Check if card in waste is ace of correct suit
            #Cycle through Tableau piles
                # Check all moves from waste to tableau (Cycle through each deck, suit must be opposite and
                # number must be one less than card in deck)
        # Check Tableau to Tableau combos (Can move more than one card)
        # Kings start new tableau decks
            #Check Tableau to Foundation combos
            #Check Foundation to Tableau moves
        # Check if solve is available.

        return legalActions

    def performAction(self, action):
        parsedAction = action.split()

        if (parsedAction[0] == "D"):
            # The klondike replenishes when there are still waste cards but no cards in deck/stock
            if len(self.klondike.stock.remaining) == 0 and len(self.klondike.waste) > 0:
                self.replenishFlag += 1
            self.klondike.deal()

        elif (parsedAction[0] == "F"):
            self.klondike.select_foundation(self.klondike, int(parsedAction[1]), int(parsedAction[2]))
        elif (parsedAction[0] == "W"):
            self.klondike.select_waste(self.klondike, parsedAction[1])
            self.replenishFlag = 0
        elif (parsedAction[0] == "T"):
            self.klondike.select_tableau(self.klondike, int(parsedAction[1]), int(parsedAction[2]), int(parsedAction[3]))
        elif (parsedAction[0] == "S"):
            self.klondike.solve(self.klondike)

    def hasLost(self):
        if (self.replenishFlag == 2):
            return True

    
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

    def getFeatures(self, gameUI: KlondikeController):

        features = util.Counter()
        tableaus = gameUI.game.tableau.piles
        features["bias"] = 1.0


        hiddenCardsPre = 0.0
        for tableau in tableaus:
            for card in tableau:
                if not card.is_revealed:
                    hiddenCardsPre += 1.0

        # util.doAction(, action)

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

        # if (action[0] == "D"):
        #     state.undo_deal()
        # elif (action[0] == "F"):
        #     features["origin"] = int(parse[1])
        #     features["foundation"] += 1.0
        #     state.undo_select_foundation()
        # elif (action[0] == "W"):
        #     state.undo_select_waste()
        # elif (action[0] == "T"):
        #     features["origin"] = parse[1]
        #     state.undo_select_tableau()


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
  
    def getQValue(self, state):
        """
        Should return Q(state,action)
        """
        q = 0
        features = self.featExtractor.getFeatures(state)
        for feature in features:
            q += features[feature] * self.weights[feature]
        return q


    def computeValueFromQValues(self):
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
            q = self.getQValue(action)
            if (q > maxQ):
                maxQ = q
        return maxQ

    #TODO verify
    def computeActionFromQValues(self):
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
            q = self.getQValue(action)
            if (q > bestQ):
                bestAction = action
                bestQ = q
        return bestAction
        
    def getAction(self):
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
        action = self.computeActionFromQValues()

        # Epsilon chance of picking a random move
        if (util.flipCoin(self.epsilon)):
            action = random.choice(legalActions)
            
        return action
    #TODO verify
    def update(self, state, nextState, reward: float):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(nextState)
        diff = (reward + (self.discount*self.computeValueFromQValues(nextState))) - self.getQValue(state)
        for feature in features:
            # Question for TAs: I had to move the diff calc outside of the loop. Why doesn't it work inside the loop?
            self.weights[feature] = self.weights[feature] + (self.alpha*diff*features[feature])

    def getPolicy(self):
        return self.computeActionFromQValues()
    def getValue(self):
        return self.computeValueFromQValues()


    # Training
    def observeTransition(self, state, nextState, deltaReward, legalActions):
        """
            Called by environment to inform agent that a transition has
            been observed. This will result in a call to self.update
            on the same arguments

            NOTE: Do *not* override or call this function
        """
        self.legalActions = legalActions
        self.episodeRewards += deltaReward
        self.update(state, nextState, deltaReward)

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
    print(f"{game.getLegalActions()}")

if __name__ == "__main__":
    main()
