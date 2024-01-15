import time, random, math, collections, numpy
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
import Azul.azul_utils as utils

THINKTIME = 0.9
NUM_PLAYERS = 2


# Defines this agent.
class myAgent():
    def __init__(self, _id):
        self.id = _id
        self.game_rule = GameRule(NUM_PLAYERS)

    def minimax(self, game_state, depth, alpha, beta, max_player):
        """
        Minimax main code
        """
        terminal_reached, round_end = self._check_terminal(game_state)

        if depth == 0 or terminal_reached or round_end:
            return None, self._evaluate(game_state)

        actions = self._get_best_actions(game_state)

        best_action = actions[0]  # init best action to the first action in the list and the
        value = -math.inf if max_player else math.inf  # value to negative or positive infinity depending on the player role

        for action in actions:

            game_state_copy = deepcopy(game_state)
            game_state_copy = self.game_rule.generateSuccessor(game_state_copy, action, self.id)

            new_value = self.minimax(game_state_copy, depth - 1, alpha, beta, not max_player)[1]

            if max_player and new_value > value or not max_player and new_value < value:
                value = new_value
                best_action = action

            # update alpha or beta depending on the player role
            if max_player:
                alpha = max(alpha, value)
            else:
                beta = min(beta, value)

            # PRUNING the search tree if alpha is greater than or equal to beta
            if alpha >= beta:
                break

        return best_action, value

    def _check_terminal(self, game_state):
        """
        check game state as terminal or not
        """

        # check if any player has completed a row on their grid
        terminal_reached = any([plr_state.GetCompletedRows() > 0 for plr_state in game_state.agents])

        # check if there are no tiles remaining in the factories and centre pool
        end_of_round = False if terminal_reached else game_state.TilesRemaining() == 0

        return terminal_reached, end_of_round

    def _evaluate(self, game_state):
        game_state_dc = deepcopy(game_state)
        opp_id = 1 - self.id
        num_rounds = 4 - (len(game_state.bag)//20)
        game_state_dc.ExecuteEndOfRound()

        player_score = game_state_dc.agents[self.id].score
        opp_score = game_state_dc.agents[opp_id].score

        grid_line_score = self._get_grid_line_score(game_state_dc)

        set_differences = self._get_set_difference(game_state_dc)

        center_score = self._get_center_score(game_state_dc)

        return (player_score - opp_score) + grid_line_score + 2*set_differences*(num_rounds/4) + center_score/num_rounds

    def _get_grid_line_score(self, game_state):

        """
        TO CONSIDER GRID/PATTERN-LINE diff.
        this function finds the difference between the number of tiles in players grid and opponents grid
        as well as player pattern lines and opponent pattern lines.
        """

        player_grid_tiles, opp_grid_tiles, player_line_tiles, opp_line_tiles = 0, 0, 0, 0
        plr_state = game_state.agents[self.id]
        opp_state = game_state.agents[1 - self.id]

        for row in range(plr_state.GRID_SIZE):
            player_line_tiles += plr_state.lines_number[row]
            opp_line_tiles += opp_state.lines_number[row]
            for col in range(plr_state.GRID_SIZE):
                player_grid_tiles += plr_state.grid_state[row][col]
                opp_grid_tiles += opp_state.grid_state[row][col]

        grid_line_score = (player_grid_tiles - opp_grid_tiles) - (player_line_tiles - opp_line_tiles)

        return grid_line_score

    def _get_set_difference(self, game_state):

        """
        TO CONSIDER SET BONUS
        Calculates the difference in tile counts for each type between current player and opponent,
        then sums up the distances to consider set bonus.
        """
        plr_state = game_state.agents[self.id]
        opp_state = game_state.agents[1 - self.id]

        difference = 0

        for tile in utils.Tile:
            num_tiles_plr = plr_state.number_of[tile]
            num_tiles_opp = opp_state.number_of[tile]
            difference += (num_tiles_plr - num_tiles_opp)

        return difference
    
    def _get_center_score(self, game_state):

        """
        Rewards actions that place tiles closer to the center of the grid
        """
        player_center_score, opp_center_score = 0, 0
        plr_state = game_state.agents[self.id]
        opp_state = game_state.agents[1 - self.id]
        for row in range(plr_state.GRID_SIZE):
            for col in range(plr_state.GRID_SIZE):
                """
                Reward pattern:
                0  1  2  1  0
                1  2  3  2  1
                2  3  4  3  2
                1  2  3  2  1
                0  1  2  1  0
                """
                if row < 3:
                    player_center_score += row*plr_state.grid_state[row][col]
                    # opp_center_score += row*opp_state.grid_state[row][col]
                else:
                    player_center_score += (4 - row)*plr_state.grid_state[row][col]
                    # opp_center_score += (4 - row)*opp_state.grid_state[row][col]

                if col < 3:
                    player_center_score += col*plr_state.grid_state[row][col]
                    # opp_center_score += col*opp_state.grid_state[row][col]
                else:
                    player_center_score += (4 - col)*plr_state.grid_state[row][col]
                    # opp_center_score += (4 - col)*plr_state.grid_state[row][col]

        # center_score = (player_center_score - opp_center_score)

        return player_center_score


    def _get_best_actions(self, game_state):
        """
        get ordered actions based on desirability
        """

        actions = self.game_rule.getLegalActions(game_state, self.id)
        action_dict = {}

        for action in actions:

            tg = action[2]
            tile_type, num_to_pattern_line, pattern_line_dest, num_to_floor_line = \
                tg.tile_type, tg.num_to_pattern_line, tg.pattern_line_dest, tg.num_to_floor_line

            if pattern_line_dest == -1:  # skip actions with no PL destination
                continue

            desirability = num_to_pattern_line - num_to_floor_line

            # Save more desirable action for the same tile_type and pattern line destination
            if (tile_type, pattern_line_dest) not in action_dict or desirability > \
                    action_dict[(tile_type, pattern_line_dest)][0]:
                action_dict[(tile_type, pattern_line_dest)] = (desirability, action)

        # sort the dictionary by desirability
        to_ret = [val[1] for _, val in sorted(action_dict.items(), reverse=True, key=lambda x: x[1][0])]

        return to_ret if to_ret else actions  # original actions only returned if all actions directly lead to floor

    def SelectAction(self, actions, game_state):

        dpth = 3 if len(actions) > 40 else 4 if len(actions) > 15 else 5

        action, _ = self.minimax(game_state, dpth, -math.inf, math.inf,
                                 True)  # consider this agent as the maximizer agent
        return action
