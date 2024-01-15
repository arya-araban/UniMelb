# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import math
import random
from cmath import inf
from itertools import accumulate
from queue import PriorityQueue
from queue import Queue
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    print("chane")
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


# Please DO NOT change the following code, we will use it later
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    startNode = (startState, '', 0, [])
    myPQ.push(startNode, heuristic(startState, problem))
    visited = set()
    best_g = dict()
    while not myPQ.isEmpty():
        node = myPQ.pop()
        state, action, cost, path = node
        if (not state in visited) or cost < best_g.get(state):
            visited.add(state)
            best_g[state] = cost
            if problem.isGoalState(state):
                path = path + [(state, action)]
                actions = [action[1] for action in path]
                del actions[0]
                return actions
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                myPQ.push(newNode, heuristic(succState, problem) + cost + succCost)
    util.raiseNotDefined()


def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    def improve(node):  # this function gets a node as input and returns the successor which has a better heuristic val
        q = util.Queue()
        q.push(node)
        visited = set()

        original_state = node[0]

        while not q.isEmpty():
            cur_node = q.pop()
            cur_state = cur_node[0]

            if cur_state not in visited:
                visited.add(cur_state)
                if heuristic(cur_state, problem) < heuristic(original_state, problem):
                    return cur_node
                for succ_node in problem.getSuccessors(cur_state):
                    succState, succAction, _ = succ_node
                    new_node = (succState, succAction, 0, cur_node)
                    q.push(new_node)

    currentNode = (problem.getStartState(), '', 0, [])
    while True:
        currentNode = improve(currentNode)

        if problem.isGoalState(currentNode[0]):
            path = []
            while currentNode[1]:
                path.append(currentNode[1])
                currentNode = currentNode[3]

            return path[::-1]


def bidirectionalAStarEnhanced(problem, heuristic=nullHeuristic, backwardsHeuristic=nullHeuristic):
    fwd_open = util.PriorityQueue()
    bwd_open = util.PriorityQueue()

    start_state = problem.getStartState()
    goal_state = problem.getGoalStates()[0]

    fwd_open.push((start_state, [], 0), heuristic(start_state, problem))
    bwd_open.push((goal_state, [], 0), backwardsHeuristic(goal_state, problem))

    fwd_visited = set()
    bwd_visited = set()

    lb = 0
    ub = float('inf')

    sol = []
    cur_node_direction = 'forward'

    while not fwd_open.isEmpty() and not bwd_open.isEmpty():

        fwd_bmin = fwd_open.getMinimumPriority()
        bwd_bmin = bwd_open.getMinimumPriority()

        lb = (fwd_bmin + bwd_bmin) / 2

        (cur_open, cur_closed, other_open) = (fwd_open, fwd_visited, bwd_open) if cur_node_direction == 'forward' else (
            bwd_open, bwd_visited, fwd_open)

        node = cur_open.pop()

        cur_state, cur_path, cur_cost = node

        cur_closed.add(cur_state)

        other_open_nodes = [pqs[-1] for pqs in other_open.heap]

        for node in other_open_nodes:
            other_state, other_path, other_cost = node
            if other_state == cur_state:  # found node from the other way

                possible_ub = cur_cost + other_cost

                if possible_ub < ub:

                    ub = possible_ub
                    sol = cur_path + other_path[::-1]
                    if cur_node_direction == 'backward':
                        sol = sol[::-1]


        if lb >= ub:  # Terminate if the lower bound is greater than or equal to the upper bound.
            return sol

        successors = problem.getSuccessors(
            cur_state) if cur_node_direction == 'forward' else problem.getBackwardsSuccessors(cur_state)

        for scs in successors:
            succ_state, succ_action, succ_cost = scs
            if succ_state not in cur_closed:
                new_cost = cur_cost + succ_cost
                new_path = cur_path + [succ_action]

                if cur_node_direction == 'forward':
                    dx = new_cost - backwardsHeuristic(succ_state, problem)
                    priority = new_cost + heuristic(succ_state, problem) + dx
                else:
                    dx = new_cost - heuristic(succ_state, problem)
                    priority = new_cost + backwardsHeuristic(succ_state, problem) + dx

                cur_open.push((succ_state, new_path, new_cost), priority)

        cur_node_direction = 'forward' if cur_node_direction == 'backward' else 'backward'

    return sol


def reconstruct_path(parents_f, parents_b, meeting_point):
    path = []
    current_node = meeting_point

    # Reconstruct the forward path
    while parents_f[current_node] is not None:
        previous_node, action = parents_f[current_node]
        path.insert(0, action)
        current_node = previous_node

    # Reconstruct the backward path
    current_node = meeting_point
    while parents_b[current_node] is not None:
        previous_node, action = parents_b[current_node]
        path.append(action)  # You may need to reverse the action if your problem requires it
        current_node = previous_node

    # The problem passed in going to be BidirectionalPositionSearchProblem

    # put the below line at the end of your code or remove it
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

ehc = enforcedHillClimbing
bae = bidirectionalAStarEnhanced
