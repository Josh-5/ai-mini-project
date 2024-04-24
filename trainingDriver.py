""" 
The main driver for training our approximate q learning agent. Later on there should also be 
features that help storing and loading the parameters.
"""

import copy
from pytience.cmd.klondike import KlondikeCmd
from qLearningAgent import QLearningAgent
from qLearningAgent import KlondikeController
# from util import doAction, raiseNotDefined

class TrainingDriver:
    def __init__(self, episodesCount=5000, testCount=1000):
        
        self.control = KlondikeController()
        self.agent = QLearningAgent(numTraining=episodesCount, legalActions=self.control.getLegalActions())
        self.episodesCount = episodesCount
        self.testCount = testCount

    def run(self):
        print("Training approximate Q agent to play Klondike...")
        winCount = 0
        for episode in range(self.episodesCount):
            

            self.agent.startEpisode()
            while True:
                prevState = self.control.klondike.dump()
                prevScore = self.control.klondike.score
                action = self.agent.getAction(prevState)
                print(prevState)
                print("\n\n\n")
                print(action)
                print("\n\n\n")
                # execute action
                self.control.performAction(action)
                deltaReward = self.control.klondike.score - prevScore

                # observe the transition and learn
                self.agent.observeTransition(
                    prevState, action, self.control.klondike.dump(), deltaReward, self.control.getLegalActions())
                
                # check end game
                if self.control.hasLost():
                    break

                if self.control.klondike.is_solved():
                    winCount += 1
                    break

            self.agent.stopEpisode()
            # Resets the game
            self.control.do_new("")

        print(f"Training completed, won {winCount}/{self.episodesCount} games")

        
        self.testAgent()
        

    # TODO implement
    def testAgent(self):
        print("Testing trained agent...")
        winCount = 0
        for test in range(self.testCount):
            # do testing on fresh games without training (epsilon and alpha values should be 0)
            pass
        print("Testing completed, won {winCount}/{self.testCount} games")

    
if __name__ == "__main__":
    driver = TrainingDriver()
    driver.run()
