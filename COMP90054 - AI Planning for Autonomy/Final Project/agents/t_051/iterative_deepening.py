import math
import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque

THINKTIME = 0.9
NUM_PLAYERS = 2


# Defines this agent.
class myAgent():
    def __init__(self, _id):
        self.id = _id  # Agent needs to remember its own id.
        self.game_rule = GameRule(NUM_PLAYERS)  # Agent stores an instance of GameRule, from which to obtain functions.

    # Generates actions from this state.
    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)

    # Carry out a given action on this state and return True if goal is reached received.
    def DoAction(self, state, action):

        old_agent = deepcopy(state).agents[self.id]
        state = self.game_rule.generateSuccessor(state, action, self.id)

        agent = state.agents[self.id]
        opponent = state.agents[1 - self.id]

        # goal conditions ordered based on importance
        goal_reached = (agent.score > opponent.score and agent.GetCompletedRows()) or \
                       (agent.GetCompletedColumns() > old_agent.GetCompletedColumns()) or \
                       (agent.GetCompletedSets() > old_agent.GetCompletedSets()) or \
                       (agent.floor_tiles == [])

        return goal_reached

    # Take a list of actions and an initial state, and perform iterative deepening search within a time limit.
    # Return the first action that leads to goal, if any was found.
    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        depth_limit = 0
        best_action = random.choice(actions)  # Choose a random action as default

        while time.time() - start_time < THINKTIME:
            queue = deque(
                [(deepcopy(rootstate), [], 0)])  # Initialize the queue with the root state and empty path and depth
            visited = set()  # Initialize a set to store the visited states

            while len(queue):
                state, path, depth = queue.popleft()
                new_actions = self.GetActions(state)  # Get the legal actions for the state

                for a in new_actions:
                    next_state = deepcopy(state)
                    next_path = path + [a]
                    next_depth = depth + 1
                    goal = self.DoAction(next_state, a)  # Apply the action and check if it reaches the goal
                    if goal:
                        return next_path[0]
                    elif next_depth <= depth_limit and next_state not in visited:
                        # Checking if the depth limit is not exceeded and the state is not visited
                        queue.append((next_state, next_path, next_depth))
                        visited.add(next_state)

            depth_limit += 1

        return best_action  # Return the best action found so far
