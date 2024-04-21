""" 
The main driver for training our approximate q learning agent. Later on there should also be 
features that help storing and loading the parameters.
"""

from pytience.cmd.klondike import KlondikeCmd
from qLearningAgent import QLearningAgent
from util import doAction, raiseNotDefined

class TrainingDriver:
    def __init__(self, episodesCount=5000, testCount=1000):
        self.cmd = KlondikeCmd()
        self.game = self.cmd.klondike
        self.agent = QLearningAgent(numTraining=episodesCount)
        self.episodesCount = episodesCount
        self.testCount = testCount

    def run(self):
        for i in range(self.episodesCount):
            self.agent.startEpisode()
            while True:
                # execute action
                action = self.agent.getAction()
                doAction(self.game, action)

                # observe the transition and learn

                # check if done or not
                if self.game.is_solved() or self.agent.hasLost():
                    break

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
