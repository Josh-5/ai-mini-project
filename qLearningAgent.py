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
    def __init__(self, featExtractor=SimpleExtractor(), numTraining=100, epsilon=0.5, epsilonDecay=0.995, epsilonMin=0.01, alpha=0.5, gamma=1):
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
  
    def getQValue(self, gameUI: KlondikeController, action):
        """
        Should return Q(state,action)
        """
        q = 0
        features = self.featExtractor.getFeatures(gameUI, action)
        for feature in features:
            q += features[feature] * self.weights[feature]
        return q

    #TODO verify
    def computeValueFromQValues(self, gameUI: KlondikeController):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameUI.getLegalActions()

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
    def computeActionFromQValues(self, gameUI: KlondikeController):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameUI.getLegalActions()
        print(legalActions)
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
            
    # TODO verify
    def getAction(self, gameUI:KlondikeController):
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
        legalActions = gameUI.getLegalActions()
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
    def update(self, prevGameUI: KlondikeController, action, gameUI: KlondikeController, reward: float):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # Apply the update formula for TD Q-learning:
        # Q(s,a)updated = (1-alpha)Q(s,a) + alpha(sample)
        # sample = R(s,a,s') + gamma*max(Q(s',a') of all a' in actions)

        features = self.featExtractor.getFeatures(prevGameUI,action)
        diff = (reward + (self.discount*self.computeValueFromQValues(gameUI))) - self.getQValue(state,action)
        for feature in features:
            # Question for TAs: I had to move the diff calc outside of the loop. Why doesn't it work inside the loop?
            self.weights[feature] = self.weights[feature] + (self.alpha*diff*features[feature])

    def getPolicy(self):
        return self.computeActionFromQValues()
    def getValue(self):
        return self.computeValueFromQValues()


    # Training
    def observeTransition(self, state, action, nextState, deltaReward):
        """
            Called by environment to inform agent that a transition has
            been observed. This will result in a call to self.update
            on the same arguments

            NOTE: Do *not* override or call this function
        """
        self.episodeRewards += deltaReward
        self.update(state,action,nextState,deltaReward)

    def startEpisode(self):
        """
          Called by environment when new episode is starting
        """
        self.lastState = None
        self.lastAction = None
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
    
    
    def doAction(self,state,action):
        """
            Called by inherited class when
            an action is taken in a state
        """
        self.lastState = state
        self.lastAction = action

    def final(self, state):
        """
          Called by Pacman game at the terminal state
        """
        deltaReward = state.getScore() - self.lastState.getScore()
        self.observeTransition(self.lastState, self.lastAction, state, deltaReward)
        self.stopEpisode()

        # Make sure we have this var
        if not 'episodeStartTime' in self.__dict__:
            self.episodeStartTime = time.time()
        if not 'lastWindowAccumRewards' in self.__dict__:
            self.lastWindowAccumRewards = 0.0
        self.lastWindowAccumRewards += state.getScore()

        NUM_EPS_UPDATE = 100
        if self.episodesSoFar % NUM_EPS_UPDATE == 0:
            print('Reinforcement Learning Status:')
            windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
            if self.episodesSoFar <= self.numTraining:
                trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
                print('\tCompleted %d out of %d training episodes' % (
                       self.episodesSoFar,self.numTraining))
                print('\tAverage Rewards over all training: %.2f' % (
                        trainAvg))
            else:
                testAvg = float(self.accumTestRewards) / (self.episodesSoFar - self.numTraining)
                print('\tCompleted %d test episodes' % (self.episodesSoFar - self.numTraining))
                print('\tAverage Rewards over testing: %.2f' % testAvg)
            print('\tAverage Rewards for last %d episodes: %.2f'  % (
                    NUM_EPS_UPDATE,windowAvg))
            print('\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime))
            self.lastWindowAccumRewards = 0.0
            self.episodeStartTime = time.time()

        if self.episodesSoFar == self.numTraining:
            msg = 'Training Done (turning off epsilon and alpha)'
            print('%s\n%s' % (msg,'-' * len(msg)))

    # Pacman specifically hasmore functions to track the current state/observation, initial state, and final state.

    

def main():
    game = KlondikeController()
    print(f"{game.getLegalActions()}")

if __name__ == "__main__":
    main()
