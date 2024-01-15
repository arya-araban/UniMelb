# AI Method 1 - Computational Approach

Your notes about this part of the project, including acknowledgement, comments, strengths and limitations, etc.

You **do not** need to explain the algorithm. Please tell us how you used it and how you applied it in your team.

If you use greed best first search, then, you can explain about what is the problem (state space model, especially how you define the state, how your define the goal), and heuristic function (as specific as possible) that you used. 

If you use MCTS, then, you can explain about what tree policy/simulation policy you used, how many iteration did you run, what is your reward function, the depth of each simulation etc.

# Table of Contents
- [Governing Strategy Tree](#governing-strategy-tree)
  * [Motivation](#motivation)
  * [Application](#application)
  * [Solved challenges](#solved-challenges)
  * [Trade-offs](#trade-offs)     
     - [Advantages](#advantages)
     - [Disadvantages](#disadvantages)
  * [Future improvements](#future-improvements)

## Governing Strategy Tree  

### Motivation  

We used UCB1 MAB algorithm to select the best action at each state. The reason that we chose UCB1 MAB is that it shows a better balance on the exploration and exploitation than other MAB approaches, such as Epsilon-Greedy, softmax etc. In other words UCB1 MAB can select the action that has the potential to provide the highest score after the simulation process.


[Back to top](#table-of-contents)

### Application  

We assign random probability for each action we have for each state. In addition, for each episode, we simulate the actions that we could take from only the view of ourselves, untill until all the tiles in this round are clear. The length of the episode depends on the actions we choose. At the end of each episode, we would have a reward based on the score we have. Our UCB1 MAB will make sure that we would select the policy that would provide us with the best reward, and we store the policy in a list. Then we randomly choose one of the action from the policy. Everytime we execute an action, or the opponent execute an action, the state will change and we will first check if the actions in our previous policy is still available. If so, we execute one of the actions from the previous policy. If not, we remove all the policies from the past, and we recalculate the policy based on the current state and repeat the process.

[Back to top](#table-of-contents)

### Solved Challenges

This is our second version of the agent design process. Comparing to the first BFS agent, we solved two major issues. 

Firstly, we have to design a goal for the BFS agent. This goal could be anything. In other words, we could set it to complete at least one row or we could set to to complete at least one column. The decision of what the goal should be is totally based on the human decisions. The problem is that there might be a better goal that our BFS agent could achieve, but since we have already set the goal, our BFS agent will not look at that direction. Our UCB agent solved this challenge by finding the best reward, we do not look for specific goals, we only look for a series of actions that would lead us to the best rewards that we can have at a specific state. In this way, the goal could be dynamic at any given states, and the UCB agent can change its goal automatically based on the policy that could provide the best reward for it.

Secondly, the BFS agent typically take a long time to find a path to the goal that we set at the beginning of the game, because of the large amount of nodes it has to expand. This cause a BFS agent act as a random agent at the first couple of rounds, even the whole game. In other words, our BFS agent might only provide a little help at the very end of the game, sometimes even no help at all, due to the time limitation. This problem does not exist in our UCB agent, because it will provide the action that would provide the best reward within the time limit. This means our UCB agent will break the episode immediately if the time is up. Even the whole episode has not finished yet, it can still have a estimation for the actions it has simulated up to the time that it stopped. This way, the action it provides will have the highest probability that would lead us to win the game at that state.  

|  | BFS_Agent | UCB_Agent |
| --- | --- | --- |
| `average score` | 17.66 | 29.10 |
| `win rate` | 10% | 85% |

[Back to top](#table-of-contents)


### Trade-offs  
#### *Advantages*  

1. **Goal could be automatically defined in every state:** There will be no specific goal such as `complte one column`, UCB agent only care about which actions can help us to get more scores and less penalties.
2. **Optimistic action within the time limitation:** Even the time is run out, UCB can also choose the actions that would have the highest potential to lead us to the winning state during the simulation phase. 

#### *Disadvantages*

1. **Optimistic action might not be the best action:** The action that provides the highest potential during the simulation phase does not mean it is the **best** action that would lead us to the winning state. It only means that this action is the best action that we found within the time restriction. In other words, the action we did not choose might be the **true** action that could lead us to the winning state.
2. **Opponent actions:** We did not take the **actual** opponent actions into account when during the simulation process. Instead, we only simulated the opponent actions by the random distribution. This might mislead our UCB agent to conclude with a less accurate result.


[Back to top](#table-of-contents)

### Future improvements  

There are several adaptions that could be made on our UCB agent. Firstly, we could embed our UCB MAB into a MCTS in the simulation stage. Since MCTS could take the other opponent's actual action into account, our policy would be more accurate. It will also generate a tree policy which could be used for the calculation in the next round after one of the action in the MCTS has been executed. In other words, MCTS will continue from the previous generated policy tree. This will speed up the calculation process, and consequently provide us a better action to lead us to the winning state.

[Back to top](#table-of-contents)
