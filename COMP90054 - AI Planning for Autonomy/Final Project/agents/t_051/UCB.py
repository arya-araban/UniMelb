# REFERENCE -------------------------------------------------------------------------------------------- #


# Author:  University of Melbourne
# Date:    19/05/2023
# Purpose: UCB MAB..

import math
import random


class UpperConfidenceBounds():
    def __init__(self):
        self.total = 0
        # number of times each action has been chosen
        self.times_selected = {}

    def getMaxAction(self):
        return max(self.times_selected, key = self.times_selected.get)

    def select(self, state, actions, qfunction):

        # First execute each action one time
        for action in actions:
            if action not in self.times_selected.keys():
                self.times_selected[action] = 1
                self.total += 1
                return action

        max_actions = []
        max_value = float("-inf")
        for action in actions:
            value = qfunction.get_q_value(state, action) + math.sqrt(
                (2 * math.log(self.total)) / self.times_selected[action]
            )
            if value > max_value:
                max_actions = [action]
                max_value = value
            elif value == max_value:
                max_actions += [action]

        # if there are multiple actions with the highest value
        # choose one randomly
        result = random.choice(max_actions)
        self.times_selected[result] = self.times_selected[result] + 1
        self.total += 1
        return result