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
from featureExtractors import SimpleExtractor


class KlondikeController(KlondikeCmd):
    def __init__(self: KlondikeCmd):
        super.__init__()
        self.game = self.klondike
    
    def getLegalActions(self):
        pass

    

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

    # Check whether the agent has lost the game
    def hasLost() -> bool:
        # TODO implement
        util.raiseNotDefined()

    def getDestinationActions(self, sourceTableau, cardIndex):
        actions = []
        placeholderAction = ""

        if not isinstance(sourceTableau,deck.Suit):
            sourceCard:deck.Card = sourceTableau[cardIndex]
            # Check the tableau piles. destTableau is type tableau.Tableau
            for destTableau in self.game.tableau.piles:
                # make sure the source and destination pile aren't the same
                if sourceTableau != destTableau: 
                    destCard:deck.Card = destTableau[len(destTableau) - 1]
                    # If the colors alternate, and the source card is one more than the last card
                    if sourceCard.suit.color != destCard.suit.color \
                    and CARD_VALUES[sourceCard.pip] == CARD_VALUES[destCard.pip] + 1:
                        # TODO: construct action
                        actions.append(placeholderAction)
        

            # Check the foundation pile
            destFoundation = self.game.foundation.piles[sourceCard.suit]
            if sourceCard.pip == deck.Pip.Ace:
                actions.append(placeholderAction)
            elif len(destFoundation) != 0 \
            and CARD_VALUES[sourceCard.pip] == CARD_VALUES[destFoundation[ len(destFoundation) - 1 ].pip]:
                actions.append(placeholderAction)

        return actions

    # TODO add legal actions for stock and waste.
    def getLegalActions(self):
        """
          Get the actions available for a given
          state. This is what you should use to
          obtain legal actions for a state
        """
        # legalActions = self.getDestinationActions(self.game.stock.cards len(state["stock"]["cards"]) - 1)

        # legalActions.append(self.getDestinationActions(state["waste"]["cards"], len(state["waste"]["cards"]) - 1))

        legalActions = []
        for sourcePile in self.game.tableau.piles:
            for i in range(len(sourcePile)):
                # Check if the card is hidden
                if not sourcePile[i].is_revealed:
                    legalActions.append(self.getDestinationActions(sourcePile, i))
        
        for sourcePile in self.game.foundation.piles:
            legalActions.append(self.getDestinationActions(sourcePile, i))

        return legalActions



    #TODO verify
    def getQValue(self, state, action):
        """
        Should return Q(state,action)
        """
        q = 0
        features = self.featExtractor.getFeatures(state, action)
        for feature in features:
            q += features[feature] * self.weights[feature]
        return q

    #TODO verify
    def computeValueFromQValues(self):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions()

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
        legalActions = self.getLegalActions()
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
        legalActions = self.getLegalActions()
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
    def update(self, state, action, nextState, reward: float):
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

        features = self.featExtractor.getFeatures(state,action)
        diff = (reward + (self.discount*self.computeValueFromQValues(nextState))) - self.getQValue(state,action)
        for feature in features:
            # Question for TAs: I had to move the diff calc outside of the loop. Why doesn't it work inside the loop?
            self.weights[feature] = self.weights[feature] + (self.alpha*diff*features[feature])

    def getPolicy(self):
        return self.computeActionFromQValues()
    def getValue(self):
        return self.computeValueFromQValues()


    def run(self):
        while (not self.game.is_solved() and not self.getLegalActions() == []):
            self.interpretAction(self.computeActionFromQValues())


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
    agent = QLearningAgent()
    agent.run()

if __name__ == "__main__":
    main()
