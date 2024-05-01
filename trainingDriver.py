""" 
The main driver for training our approximate q learning agent. Later on there should also be 
features that help storing and loading the parameters.
"""

import copy
from pytience.cmd.klondike import KlondikeCmd
from qLearningAgent import QLearningAgent
from qLearningAgent import KlondikeController
import time

class TrainingDriver:
    def __init__(self, episodesCount=1, testCount=1):
        
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
            
                # execute action
                self.control.performAction(action)
                deltaReward = self.control.klondike.score - prevScore
                # print(deltaReward)
                # observe the transition and learn
                self.agent.observeTransition(
                    prevState, action, self.control.klondike.dump(), deltaReward, self.control.getLegalActions())
                
                # check end game
                if self.control.hasLost():
                    print("LOST GAME")
                    break

                if self.control.klondike.is_solved():
                    winCount += 1
                    print("WON GAME")
                    break

            self.agent.stopEpisode()
            # Resets the game
            self.control.do_new("")
            self.agent.setLegalActions(self.control.getLegalActions())

        print(f"Training completed, won {winCount}/{self.episodesCount} games")
        print(self.agent.weights)
        
        self.testAgent()
        
        
    def testAgent(self):
        print("Testing trained agent...")
        winCount = 0
        for test in range(self.testCount):
            # do testing on fresh games without training (epsilon and alpha values should be 0)
            pass
        print("Testing completed, won {winCount}/{self.testCount} games")
        print("Final game\n\n")
        self.control.do_new("")
        self.control.print_game()
        while True:
            prevState = self.control.klondike.dump()
            self.agent.setLegalActions(self.control.getLegalActions())
            action = self.agent.getAction(prevState)
        
            # execute action
            self.control.performAction(action)
            time.sleep(1)
            self.control.print_game()
            # check end game
            if self.control.hasLost():
                print("LOST GAME")
                break

            if self.control.klondike.is_solved():
                winCount += 1
                print("WON GAME")
                break

    
if __name__ == "__main__":
    driver = TrainingDriver()
    driver.run()
