# REFERENCE -------------------------------------------------------------------------------------------- #


# Author:  University of Melbourne
# Date:    19/05/2023
# Purpose: Q table..

from collections import defaultdict

class QTable():
    def __init__(self, default=0.0):
        self.qtable = defaultdict(lambda: default)

    def update(self, state, action, delta):
        self.qtable[(state, action)] = self.qtable[(state, action)] + delta

    def get_q_value(self, state, action):
        return self.qtable[(state, action)]
    
    
