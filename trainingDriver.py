""" 
The main driver for training our approximate q learning agent. Later on there should also be 
features that help storing and loading the parameters.
"""

from pytience.cmd.klondike import KlondikeCmd
from qLearningAgent import QLearningAgent
import util

class TrainingDriver:
    def __init__(self, episodesCount):
        self.cmd = KlondikeCmd()
        self.game = self.cmd.klondike
        self.agent = QLearningAgent(numTraining=episodesCount)
        self.episodesCount = episodesCount

    

        

    def run(self):
        for i in range(self.episodesCount):
            self.agent.startEpisode()
            action = self.agent.getAction()

            self.agent.stopEpisode()

    
if __name__ == "__main__":
    driver = TrainingDriver()
    driver.run()
