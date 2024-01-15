
import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque

THINKTIME   = 0.9
NUM_PLAYERS = 2

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
    def DoAction(self, state, action):
        score = state.agents[self.id].score
        state = self.game_rule.generateSuccessor(state, action, self.id)
        
        #goal_reached = state.agents[self.id].GetCompletedColumns() > 0
        goal_reached = state.agents[self.id].GetCompletedRows() > 0
        
        return goal_reached
    
    def hAddHeuristic(self, state):

        return len(self.game_rule.getLegalActions(state, self.id))
    
    def nullHeuristic(self, state):

        return 0
    
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
        
        

        return goals_to_be_achieved
    
    # Take a list of actions and an initial state, and perform breadth-first search within a time limit.
    # Return the first action that leads to goal, if any was found.
    def SelectAction(self, actions, rootstate):
        # Start time..
        start_time = time.time()
        
        # A* PQ.. 
        # UNC - COMPARE PQ with [] DEQUE..
        bowenPQ = PriorityQueue()
        # start Node - (state, action, cost, path) 
        # UNC - 

        startState = deepcopy(rootstate)
        startNode = (startState, 0, [])
        
        # push to PQ..
        bowenPQ.push(startNode, self.rowGoalCountingHeuristic(startState))
        
        # visited set..
        # UNC
        visited = set()
        # best g dict..
        # UNC
        best_g = dict()

        # Conduct A* from the initial root state..

        # a while loop to search whenever the PQ is not empty..
        while not bowenPQ.isEmpty() and time.time()-start_time < THINKTIME:
            
            # pop the lowest g = h + c first..
            node = bowenPQ.pop()
            
            # cost is the action or tiles that you need to grab to get to the column..
            # UNC - action and cost and node design..
            state, cost, path = node
            
            # if this state has not been visited or the cost is smaller than the best 
            # g we have currently then 
            # UNC
            if (not state in visited) or cost < best_g.get(state):

                visited.add(state)
                best_g[state] = cost

                # start with successors..
                succ_actions = self.GetActions(state) 
                

                # update the state for each successors after each actions
                for succ_action in succ_actions:
                    # update the succ_state - succ_action - succ_cost - succ_path
                    # UNC - cost, action and maybe move pop to here????
                    succ_state = deepcopy(state)
                    succ_cost = 1
                    succ_path  = path + [succ_action]

                    # combine with goal checking process..
                    # UNC
                    is_goal = self.DoAction(succ_state, succ_action) # Carry out this action on the state, and check for goal

                    if is_goal:
                        print(f'A* Path found:', succ_path)  # DEL for competition..
                        return succ_path[0] # initial action to get there
                    else:
                        # add this node to the PQ and keep searching within 1s - (state, action, cost, path) 
                        # UNC - how heuristic works - succ_cost
                        newNode = (succ_state, cost + succ_cost, succ_path)

                        bowenPQ.push(newNode, self.rowGoalCountingHeuristic(state) + cost + succ_cost) 
                    
        
        return random.choice(actions) # If no goal was found in the time limit, return a random action.
        
    
