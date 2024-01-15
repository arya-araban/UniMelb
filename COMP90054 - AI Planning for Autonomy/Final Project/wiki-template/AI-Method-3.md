# AI Method 3 - MiniMax 

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

We used Minimax to find the best move for a player in the two-player Azul game, where each player tries to score more points than the other. Minimax looks at the possible moves and outcomes and chooses the best one based on a heuristic function.

In this game, the Minimax algorithm may in hindsight seem like a better choice than greedy search or Monte Carlo Tree Search (MCTS). This is because Greedy search only focuses on the current state and doesn't plan ahead, while MCTS relies on random sampling and simulations. In contrast, Minimax takes into account the entire game and anticipates the opponent's moves. To make Minimax even more effective, we've integrated alpha-beta pruning, which speeds up the search process and improves efficiency.

[Back to top](#table-of-contents)

### Application  

When using the Minimax algorithm in the two-player game Azul, we begin by reducing the action space for the current state the agent is in. We do this by filtering out actions that have no pattern line destination or that only add tiles to the floor. Next, for each tile type and pattern line destination pair, we keep only the action with the highest desirability, which is calculated as the difference between tiles added to the pattern line and tiles added to the floor. Finally, we sort the remaining actions by desirability from highest to lowest.

The depth of exploration for the current node (the current state of the game) is determined by the number of valid actions available to the agent. If there are only a few valid actions, we explore the game tree to a deeper depth before evaluating the outcome of each move. However, if there are many valid actions, we explore the game tree to a shallower depth before evaluating the moves. This approach enables us to balance the trade-off between accuracy and speed and make informed decisions efficiently.

To develop an accurate evaluation function for the Minimax algorithm, we have incorporated several factors that provide a better assessment of the game state. While using the score difference between the current player and the opponent is a good starting point, it may not provide a complete picture of the game state. Therefore, we have added more components to our evaluation function, such as analyzing the difference in the number of tiles in each player's grid and pattern lines, as well as comparing the tile counts for each type of tile between the current player and the opponent. By considering these additional factors, we can better determine which player is closer to achieving the "set" bonus, which can significantly impact the final score. We have also ensured that our evaluation function rewards adjacency between grid tiles, which is crucial for scoring in Azul. By combining these factors, we can make informed decisions and achieve a more accurate assessment of the game state.

Overall, our implementation of the Minimax algorithm for the game Azul involves reducing the action space, determining the depth of exploration, and developing an accurate evaluation function. By doing so, we can balance the trade-off between accuracy and speed and make informed decisions efficiently. Furthermore, our evaluation function considers multiple factors that provide a more comprehensive assessment of the game state, enabling us to predict the outcome of each move more accurately and achieve a higher score.

[Back to top](#table-of-contents)

### Solved Challenges

Our implementation of the Minimax algorithm for the game Azul has successfully addressed several challenges that were encountered: 

1. Reduction of the action space: Azul has a complex action space with many possible moves, which can make it difficult to determine the optimal move. Our approach of filtering out irrelevant moves and prioritizing the most desirable moves has significantly reduced the action space and enabled us to make informed decisions more efficiently.
2. Balancing accuracy and speed: In order to play Azul effectively, it is important to strike a balance between accuracy and speed. Our approach of adjusting the depth of exploration based on the number of available actions has allowed us to achieve this balance and make informed decisions efficiently.
3. Incorporating multiple factors into evaluation function: The evaluation function is a crucial component of the Minimax algorithm, as it determines the desirability of each move. Our approach of incorporating multiple factors into the evaluation function, such as tile counts and pattern line differences, has resulted in more accurate assessments of the game state and better predictions of the outcome of each move.
4. Handling complex game rules: Azul has several complex rules that can make it difficult to determine the optimal move. Our approach of reducing the action space and incorporating multiple factors into the evaluation function has helped us navigate these rules and play the game more effectively.

[Back to top](#table-of-contents)


### Trade-offs  
#### *Advantages*  

- Minimax provides a systematic and structured approach to playing Azul, which allows us to make informed decisions based on the game state.
- Incorporating alpha-beta pruning to the Minimax algorithm helps to reduce the search space and improve efficiency, making it more feasible to explore the game tree to a sufficient depth.
- Our approach of reducing the action space and incorporating multiple factors into the evaluation function has allowed us to play Azul more effectively and achieve higher scores

#### *Disadvantages*

- The Minimax approach does not fully take into account the element of randomness in Azul, which can influence the outcome of the game.
- Exploring the game tree to a deep depth can be challenging due to the large action space in Azul. As a result, the time required to explore the game tree can become too prohibitive, which limits our ability to explore the search space to its fullest extent. This may lead to suboptimal decisions being made by our algorithm 

[Back to top](#table-of-contents)

### Future improvements

There are several areas in which we could further improve our implementation of the Minimax algorithm for playing Azul. 

One potential area for improvement is the balance between the depth of exploration and the time required to make a decision. While we have developed an approach for adjusting the depth of exploration based on the number of available actions, there may be opportunities to improve this approach further. For example, we could investigate the use of machine learning techniques to predict the optimal depth of exploration for a given game state, which could help us make more informed decisions more efficiently.

Another area for improvement is the evaluation function. While our current evaluation function considers multiple factors, there may be additional information that we are not yet incorporating that could lead to more accurate assessments of the game state. For example, We could consider the color distribution of tiles in the bag, as this information could help us predict the likelihood of certain tiles being drawn in future rounds. By incorporating additional information into our evaluation function, we could achieve a more accurate assessment of the game state and make more informed decisions.

[Back to top](#table-of-contents)
