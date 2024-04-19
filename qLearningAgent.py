#follow to install pytience
#https://pypi.org/project/pytience/

from pytience.cmd.klondike import KlondikeCmd
#See game.py for comments about how to use this.

"""
Insert a notice that parts of this code comes from Berkeley
"""

class Counter(dict):
    """
    A counter keeps track of counts for a set of keys.

    The counter class is an extension of the standard python
    dictionary type.  It is specialized to have number values
    (integers or floats), and includes a handful of additional
    functions to ease the task of counting data.  In particular,
    all keys are defaulted to have value 0.  Using a dictionary:

    a = {}
    print a['test']

    would give an error, while the Counter class analogue:

    >>> a = Counter()
    >>> print a['test']
    0

    returns the default 0 value. Note that to reference a key
    that you know is contained in the counter,
    you can still use the dictionary syntax:

    >>> a = Counter()
    >>> a['test'] = 2
    >>> print a['test']
    2

    This is very useful for counting things without initializing their counts,
    see for example:

    >>> a['blah'] += 1
    >>> print a['blah']
    1

    The counter also includes additional functionality useful in implementing
    the classifiers for this assignment.  Two counters can be added,
    subtracted or multiplied together.  See below for details.  They can
    also be normalized and their total count and arg max can be extracted.
    """

    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        """
        Increments all elements of keys by the same count.

        >>> a = Counter()
        >>> a.incrementAll(['one','two', 'three'], 1)
        >>> a['one']
        1
        >>> a['two']
        1
        """
        for key in keys:
            self[key] += count

    def argMax(self):
        """
        Returns the key with the highest value.
        """
        if len(list(self.keys())) == 0:
            return None
        all = list(self.items())
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sortedKeys(self):
        """
        Returns a list of keys sorted by their values.  Keys
        with the highest values will appear first.

        >>> a = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> a['third'] = 1
        >>> a.sortedKeys()
        ['second', 'third', 'first']
        """
        sortedItems = list(self.items())

        def compare(x, y): return sign(y[1] - x[1])
        sortedItems.sort(key=functools.cmp_to_key(compare))
        return [x[0] for x in sortedItems]

    def totalCount(self):
        """
        Returns the sum of counts for all keys.
        """
        return sum(self.values())

    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(self.totalCount())
        if total == 0:
            return
        for key in list(self.keys()):
            self[key] = self[key] / total

    def divideAll(self, divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

    def __mul__(self, y):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['second'] = 5
        >>> a['third'] = 1.5
        >>> a['fourth'] = 2.5
        >>> a * b
        14
        """
        sum = 0
        x = self
        if len(x) > len(y):
            x, y = y, x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        """
        Adding another counter to a counter increments the current counter
        by the values stored in the second counter.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> a += b
        >>> a['first']
        1
        """
        for key, value in list(y.items()):
            self[key] += value

    def __add__(self, y):
        """
        Adding two counters gives a counter with the union of all keys and
        counts of the second added to counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a + b)['first']
        1
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__(self, y):
        """
        Subtracting a counter from another gives a counter with the union of all keys and
        counts of the second subtracted from counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a - b)['first']
        -5
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend

class QLearningAgent():

    def __init__(self, actionFn = None, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
        """
        actionFn: Function which takes a state and returns the list of legal actions

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        if actionFn == None:
            actionFn = lambda state: state.getLegalActions()
        self.actionFn = actionFn #Action fn gives the set of legal moves at the current state
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)

        self.cardValues = {
            "A":0,
            "1":1,
            "2":2,
            "3":3,
            "4":4,
            "5":5,
            "6":6,
            "7":7,
            "8":8,
            "9":9,
            "10":10,
            "J":11,
            "Q":12,
            "K":13
        }

        self.suits = ["♦","♥","♠","♣"]

        self.values = Counter()

        self.cmd = KlondikeCmd()
        self.game = self.cmd.klondike
        
        
        #States are tracked by GameState objects GameState (from either {pacman, capture, sonar}.py) ALT: get set of legal moves from pytience


    # red = true, black = false
    def color(self, card) -> bool:
        return card[len(card) - 1] == '♥' or card[len(card) - 1] == '♦'

    def cardValue(self, card) -> int:
        if card[0] == '|':
            return self.cardValues[card[1:len(card) - 1]]
        else:
            return self.cardValues[card[0:len(card) - 1]]

    def getDestinationActions(self, sourcePile, i, state):
        actions = []
        placeholderAction = ""
        sourceCard = sourcePile[i]

        # Check the tableau piles
        for destPile in state["tableau"]["piles"]:
            # make sure the source and destination pile aren't the same
            if sourcePile != destPile: 
                destCard = destPile[len(destPile) - 1]
                if color(sourceCard) != color(destCard) and cardValue(sourceCard) == cardValue(destCard) - 1:
                    #TODO: construct action
                    actions.append(placeholderAction)
        
        # Check the foundation piles
        for destPile in state["foundations"]["piles"]:
            # make sure the source and destination pile aren't the same
            if sourcePile != destPile: 
                destCard = destPile[len(destPile) - 1]
                if sourceCard[len(sourceCard) - 1] == destCard[len(destCard) - 1] and cardValue(sourceCard) == cardValue(destCard) + 1:
                    #TODO: construct action
                    actions.append(placeholderAction)

        return actions

    def getLegalActions(self,state):
        """
          Get the actions available for a given
          state. This is what you should use to
          obtain legal actions for a state
        """
        legalActions = self.getDestinationActions(state["stock"]["cards"][len(state["stock"]["cards"]) - 1])

        legalActions.append(self.getDestinationActions(state["waste"]["cards"][len(state["waste"]["cards"]) - 1]))

        for sourcePile in state["tableau"]["piles"]:
            for i in range(len(sourcePile)):
                # Check if the card is hidden
                if sourcePile[i][0] != '|': 
                    legalActions.append(self.getDestinationActions(sourcePile, i, state))
        
        for sourcePile in state["foundations"]["piles"]:
            legalActions.append(self.getDestinationActions(sourcePile, i, state))


        return legalActions


    def interpretAction(self, action):

        parse = action.split()

        if (action[0] == "D"):
            game.deal()
        elif (action[0] == "F"):
            self.game.select_foundation(self.game, int(parse[1]), int(parse[2]))
        elif (action[0] == "W"):
            self.game.select_waste(self.game, parse[1])
        elif (action[0] == "T"):
            self.game.select_tableau(self.game, int(parse[1]), int(parse[2]), int(parse[3]))
        elif (action[0] == "S"):
            self.game.solve(self.game)


    def getQValue(self, state, action):
        """
        Should return Q(state,action)
        """
        return self.values[(state,action)] # self.values should contain Q-values

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)

        # If there are no legal actions (terminal state), return 0.0
        if (len(legalActions) == 0):
            return 0.0
        
        # Loop through all legal actions, find and return the greatest Q value
        maxQ = -999999
        for action in legalActions:
            q = self.getQValue(state,action)
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
        legalActions = self.getLegalActions(state)
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
        legalActions = self.getLegalActions(state)
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

        sample = (reward + (self.discount*self.computeValueFromQValues(nextState)))
        self.values[(state,action)] = (1-self.alpha)*self.getQValue(state,action) + (self.alpha*sample)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


    def run(self):
        while (not self.game.is_solved() and not self.getLegalActions(self.game.dump()) == []):
            self.interpretAction(self.computeActionFromQValues(self.game.dump()))


        

    # Training


    def observeTransition(self, state,action,nextState,deltaReward):
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
    
    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setLearningRate(self, alpha):
        self.alpha = alpha

    def setDiscount(self, discount):
        self.discount = discount

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
