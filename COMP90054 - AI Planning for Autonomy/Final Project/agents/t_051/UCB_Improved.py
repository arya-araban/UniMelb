
import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import defaultdict
import random
from agents.t_051.qtable import QTable
from agents.t_051.UCB import UpperConfidenceBounds
from agents.t_051.Bowen_Priority_Queue import PriorityQueue

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
        self.UCBBanditList = []

    # Generates actions from this state.
    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
    
    # Carry out a given action on this state and return True if goal is reached received.
    def DoAction(self, state, action):
        
        state = self.game_rule.generateSuccessor(state, action, self.id)
        score = state.agents[self.id].score
        
        return score
    
    def rowGoalCountingHeuristic(self, state):
        
        goals_to_be_achieved = 5

        gridState = state.agents[self.id].grid_state

        rowGoalCountList = []

        for i in range(5):
            rowGoalCount = 0
            for j in range(5):
                if gridState[i][j] == 1:
                    rowGoalCount += 1
                    
            rowGoalCountList.append(rowGoalCount)

        # max row achieved..
        goals_to_be_achieved -= max(rowGoalCountList)

    # Take a list of actions and an initial state, and perform breadth-first search within a time limit.
    # Return the first action that leads to goal, if any was found.
    def SelectAction(self, actions, rootstate):
        
        simulated_rewards = self.Simulation(rootstate)
        
        best_episode_idx = simulated_rewards.index(max(simulated_rewards))
        
        best_action = self.UCBBanditList[best_episode_idx].getMaxAction()
        
        return best_action
        
        
    
    # REFERENCE -------------------------------------------------------------------------------------------- #


    # Author:  University of Melbourne
    # Date:    19/05/2023
    # Purpose: Simulation..
    def Simulation(self, rootstate, episodes=500, episode_length=100):

        start_time = time.time()
        self.UCBBanditList = []
         # get all the actions at this state
        actions = self.GetActions(rootstate)
        bowenPQ = PriorityQueue()
        # initiate a state for simulation purpose only..
        next_state = deepcopy(rootstate)
        bowenPQ.push(startNode, self.rowGoalCountingHeuristic(startState))
        rewards = []

        for _ in range(0, episodes):
            
            ucb = UpperConfidenceBounds()
            self.UCBBanditList.append(ucb)
            
            probabilities = []

            # assign random prob dist..
            for action in actions:
                probabilities.append(random.random())

            # The number of times each arm has been selected
            times_selected = defaultdict(lambda: 0)
            qtable = QTable()

            episode_rewards = []
            for step in range(0, episode_length):

                # Always the root state or could be sequencial state
                action = ucb.select(next_state, actions, qtable)
                

                # do action then get a score.. 
                reward = self.DoAction(next_state, action)

                episode_rewards += [reward]

                times_selected[action] = times_selected[action] + 1
                qtable.update(
                    rootstate,
                    action,
                    (reward / times_selected[action])
                    - (qtable.get_q_value(rootstate, action) / times_selected[action]),
                )

                if time.time()-start_time < THINKTIME:
                    # get the current average reward if time is restricted..
                    average_episode_rewards = sum(episode_rewards) / (step + 1)
                    rewards += [average_episode_rewards]

                    return rewards

            average_episode_rewards = sum(episode_rewards) / episodes
            rewards += [average_episode_rewards]

            
        
        return rewards
        



    