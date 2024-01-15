import time, random

import numpy as np

from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque

THINKTIME = 0.9
NUM_PLAYERS = 2


# Defines this agent.
class myAgent():
    def __init__(self, _id):
        self.id = _id
        self.game_rule = GameRule(NUM_PLAYERS)

        # Generates actions from this state.

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)

    # Carry out a given action on this state and return True if goal is reached received.
    def DoAction(self, state, action):
        score = state.agents[self.id].score
        state = self.game_rule.generateSuccessor(state, action, self.id)

        # Use a variable to store the agent object
        agent = state.agents[self.id]

        # Use a variable to store the opponent object
        opponent = state.agents[1 - self.id]

        # goal conditions ordered based on importance
        goal_reached = (agent.score > opponent.score and agent.GetCompletedRows() > 0) or \
                       (agent.GetCompletedColumns() > 0 or agent.GetCompletedSets()) or \
                       (agent.floor_tiles == [])

        return goal_reached

    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        frontier = deque([(0, deepcopy(rootstate), [])])  # priority, state, path
        costs = [0]  # estimated cost to reach each state in the frontier

        # Conduct A* search starting from rootstate.
        while len(frontier) and time.time() - start_time < THINKTIME:
            # Sort the indices of the frontier based on their estimated costs.
            sorted_indices = sorted(range(len(frontier)), key=lambda i: costs[i])
            frontier = deque([frontier[i] for i in sorted_indices])
            costs = [costs[i] for i in sorted_indices]

            _, state, path = frontier.popleft()
            new_actions = self.GetActions(state)

            for a in new_actions:

                next_state = deepcopy(state)
                next_path = path + [a]
                goal = self.DoAction(next_state, a)  # next state is updated from running code in here
                if goal:
                    return next_path[0]
                else:
                    # Calculate the cost of the next path.
                    next_cost = self.CostFunction(state, next_state)

                    # Calculate the heuristic value of the next state.
                    heuristic = self.Heuristic(next_state)

                    # Add the next state to the frontier with its priority based on estimated cost.
                    priority = next_cost + heuristic
                    frontier.append((priority, next_state, next_path))
                    costs.append(priority)

        return random.choice(actions)

    def CostFunction(self, old_state, next_state):  # cost function of doing action leading old state to next state

        cost = 1

        current_num_floor = old_state.agents[self.id].floor.count(1)  # current amount of penalty tiles

        next_num_floor = next_state.agents[self.id].floor.count(1)

        cost += (next_num_floor - current_num_floor)

        return cost

    def Heuristic(self, state):

        # Calculate the number of empty spaces in the current player's pattern lines

        completed_rows = state.agents[self.id].GetCompletedRows()
        completed_cols = state.agents[self.id].GetCompletedColumns()
        completed_sets = state.agents[self.id].GetCompletedSets()

        empty_spaces = np.count_nonzero(state.agents[self.id].grid_state == 0)

        return empty_spaces - (completed_cols + completed_rows + completed_sets)
