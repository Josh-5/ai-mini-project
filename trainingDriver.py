""" 
The main driver for training our approximate q learning agent. Later on there should also be 
features that help storing and loading the parameters.
"""

from pytience.cmd.klondike import KlondikeCmd
from qLearningAgent import QLearningAgent

class TrainingDriver:
  def __init__(self):
    self.cmd = KlondikeCmd()
    self.learningAgent = QLearningAgent()

  def run():
    pass
    
if __name__ == "__main__":
  driver = TrainingDriver()
  driver.run()
