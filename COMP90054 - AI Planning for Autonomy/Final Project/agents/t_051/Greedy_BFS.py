# INFORMATION ------------------------------------------------------------------------------------------------------- #


# Author:  Steven Spratley
# Date:    04/01/2021
# Purpose: Implements an example breadth-first search agent for the COMP90054 competitive game environment.


# IMPORTS AND CONSTANTS ----------------------------------------------------------------------------------------------#


import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#


# Defines this agent.
class myAgent():
    def __init__(self, _id):
        self.id = _id # Agent needs to remember its own id.
        self.game_rule = GameRule(NUM_PLAYERS) # Agent stores an instance of GameRule, from which to obtain functions.
        # More advanced agents might find it useful to not be bound by the functions in GameRule, instead executing
        # their own custom functions under GetActions and DoAction.

    # Generates actions from this state.
    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
    
    # Carry out a given action on this state and return True if goal is reached received.
    def CheckGoal(self, state, action):
        state = self.game_rule.generateSuccessor(state, action, self.id)
        goal_reached = False
        h = 0
        # Confirmed Success scenario
        if state.agents[self.id].GetCompletedRows() > 0 and state.agents[self.id].score > state.agents[1-self.id].score:
            goal_reached = True
        else:
            line_tiles = sum(state.agents[self.id].lines_number)
            floor_tiles = len(state.agents[self.id].floor_tiles)
            h = floor_tiles + (15 - line_tiles)

        return (goal_reached,h)
    


    # Take a list of actions and an initial state, and perform breadth-first search within a time limit.
    # Return the first action that leads to goal, if any was found.
    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        # queue      = deque([ (deepcopy(rootstate),[]) ]) # Initialise queue. First node = root state and an empty path.
        
        # Conduct BFS starting from rootstate.
        while time.time()-start_time < THINKTIME:
            new_actions = self.GetActions(rootstate) # Obtain new actions available to the agent in this state.
            best_h = None
            least_tiles = 23

            for a in new_actions: # Then, for each of these actions...
                next_state = deepcopy(rootstate)  
                g = self.CheckGoal(next_state, a)
                if g[0] == True:
                    return a
                elif g[1] < least_tiles:
                    least_tiles = g[1]
                    best_h = a
            break
        return best_h
        # return random.choice(actions) # If no goal was found in the time limit, return a random action.

                # next_state = deepcopy(state)              # Copy the state.
                # next_path  = path + [a]                   # Add this action to the path.
                # goal     = self.DoAction(next_state, a) # Carry out this action on the state, and check for goal
                # if goal:
                #     return next_path[0] # If the current action reached the goal, return the initial action that led there.
                # else:
                #     queue.append((next_state, next_path)) # Else, simply add this state and its path to the queue.
        
    
# END FILE -----------------------------------------------------------------------------------------------------------#