""" 
The main driver for training our approximate q learning agent. Later on there should also be 
features that help storing and loading the parameters.
"""

from pytience.cmd.klondike import KlondikeCmd
from qLearningAgent import QLearningAgent
from qLearningAgent import KlondikeController
from util import doAction, raiseNotDefined

class TrainingDriver:
    def __init__(self, episodesCount=5000, testCount=1000):
        self.cmd = KlondikeCmd()
        self.game = self.cmd.klondike
        self.agent = QLearningAgent(numTraining=episodesCount)
        self.control = KlondikeController(self.cmd)
        self.episodesCount = episodesCount
        self.testCount = testCount

    def run(self):
        for episode in range(self.episodesCount):
            self.agent.startEpisode()
            while not self.game.is_solved() and not self.agent.hasLost():
                prevState = self.game
                prevScore = self.control.game.score
                action = self.agent.getAction()

                # execute action
                self.control.performAction(action)
                deltaReward = self.control.game.score - prevScore

                # observe the transition and learn
                self.agent.observeTransition(prevState, action, self.game, deltaReward)

            self.agent.stopEpisode()

        self.testAgent()

    # TODO implement
    def testAgent(self):
        for i in range(self.testCount):
            # do testing on fresh games without training (epsilon and alpha values should be 0)
            pass

    
if __name__ == "__main__":
    driver = TrainingDriver()
    driver.run()
