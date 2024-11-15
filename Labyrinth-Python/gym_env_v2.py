import gymnasium as gym
from gymnasium import spaces
import numpy as np
from labyrinthe import Labyrinthe
from matrix import DIMENSION
from gui_manager import GUI_manager

class LabyrinthEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, num_human_players=0, num_ai_players=2, render_mode=None):
        super(LabyrinthEnv, self).__init__()
        
        # Initialize the game
        self.game = Labyrinthe(num_human_players=num_human_players, 
                              num_ai_players=num_ai_players)
        
        # Define action space as a single MultiDiscrete
        # [rotation (4), insertion position (3), movement position (49)]
        self.action_space = spaces.MultiDiscrete([4, 3, 49])

        # Observation space remains the same
        self.observation_space = spaces.Dict({
            'board': spaces.Box(low=0, high=1, shape=(7, 7, 6), dtype=np.int8),
            'current_tile': spaces.Box(low=0, high=1, shape=(4,), dtype=np.int8),
            'player_positions': spaces.Box(low=0, high=6, shape=(2, 2), dtype=np.int8),
            'player_treasures': spaces.Box(low=0, high=24, shape=(2,), dtype=np.int8),
            'forbidden_move': spaces.Box(low=0, high=5, shape=(2,), dtype=np.int8),
        })
        
        self.render_mode = render_mode
        self._current_phase = 1

    def _calculate_manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _calculate_distance_reward(self, current_pos, target_pos):
        """Calculate reward based on change in distance to target"""
        current_distance = self._calculate_manhattan_distance(current_pos, target_pos)
        
        if self._previous_distance is None:
            self._previous_distance = current_distance
            return 0
        
        # Calculate change in distance
        distance_change = self._previous_distance - current_distance
        self._previous_distance = current_distance
        
        # Return scaled reward
        return distance_change * 0.1  # Scale factor can be adjusted

    def _get_accessibility_score(self, pos1, pos2):
        """Calculate how accessible one position is from another"""
        path = self.game.is_accessible(pos1[0], pos1[1], pos2[0], pos2[1])
        if not path:
            return 0
        return 1.0 / len(path)  # Shorter paths get higher scores

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Reset the game state
        self.game = Labyrinthe(num_human_players=0, num_ai_players=2)
        self._current_phase = 1
        
        observation = self._get_observation()
        info = {}
        
        return observation, info

    def _get_observation(self):
        # Convert game state to observation
        board_state = np.zeros((7, 7, 6), dtype=np.int8)
        
        # Fill board state
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                tile = self.game.board.get_value(i, j)
                # Walls
                board_state[i, j, 0] = int(tile.wall_north())
                board_state[i, j, 1] = int(tile.wall_east())
                board_state[i, j, 2] = int(tile.wall_south())
                board_state[i, j, 3] = int(tile.wall_west())
                # Treasure
                board_state[i, j, 4] = tile.get_treasure() + 1 if tile.get_treasure() != -1 else 0
                # Players
                board_state[i, j, 5] = len(tile.get_pawns())

        # Current tile state
        current_tile = np.array([
            int(self.game.tile_to_play.wall_north()),
            int(self.game.tile_to_play.wall_east()),
            int(self.game.tile_to_play.wall_south()),
            int(self.game.tile_to_play.wall_west())
        ])

        # Player positions
        player_positions = np.zeros((2, 2), dtype=np.int8)
        for i in range(2):
            pos = self.game.get_coord_player(i)
            if pos:
                player_positions[i] = pos

        # Current treasures
        player_treasures = np.zeros(2, dtype=np.int8)
        for i in range(2):
            treasure = self.game.players.get_next_treasure(i)
            player_treasures[i] = treasure if treasure is not None else 0

        # Forbidden move
        direction_map = {"N": 0, "E": 1, "S": 2, "O": 3}
        forbidden_move = np.array([
            direction_map.get(self.game.forbidden_move[0], 4),
            self.game.forbidden_move[1]
        ])

        return {
            'board': board_state,
            'current_tile': current_tile,
            'player_positions': player_positions,
            'player_treasures': player_treasures,
            'forbidden_move': forbidden_move
        }

    def step(self, action):
        terminated = False
        truncated = False
        reward = 0
        
        # Unpack the action
        rotation_idx, insertion_idx, movement = action
        
        current_player = self.game.get_current_player()
        current_pos = self.game.get_coord_player()
        treasure_pos = self.game.get_coord_current_treasure()
        base_pos = self.game.get_current_player_object().get_start_position()
        
        # Phase 1: Tile insertion and rotation
        direction_map = {0: "N", 1: "E", 2: "S", 3: "O"}
        direction = direction_map[rotation_idx]
        
        insertion_positions = [1, 3, 5]
        index = insertion_positions[insertion_idx]
        
        # Check if move is forbidden
        if self.game.is_forbidden_move(direction, index):
            reward = -1
            self._current_phase = 1
        else:
            # Store pre-move accessibility
            pre_move_accessibility = 0
            if treasure_pos:
                pre_move_accessibility = self._get_accessibility_score(current_pos, treasure_pos)
            elif self.game.get_current_player_remaining_treasure() == 0:
                pre_move_accessibility = self._get_accessibility_score(current_pos, base_pos)

            # Execute the move
            self.game.play_tile(direction, index)
            
            # Calculate post-move accessibility
            post_move_accessibility = 0
            if treasure_pos:
                post_move_accessibility = self._get_accessibility_score(current_pos, treasure_pos)
            elif self.game.get_current_player_remaining_treasure() == 0:
                post_move_accessibility = self._get_accessibility_score(current_pos, base_pos)

            # Reward improvement in accessibility
            accessibility_change = post_move_accessibility - pre_move_accessibility
            reward += accessibility_change * 0.5
            
            # Phase 2: Movement
            target_pos = (movement // 7, movement % 7)
            valid_movements = self._get_mouvements_possibles()
            
            if target_pos in valid_movements:
                # Calculate distance-based reward
                if treasure_pos:
                    reward += self._calculate_distance_reward(target_pos, treasure_pos)
                elif self.game.get_current_player_remaining_treasure() == 0:
                    reward += self._calculate_distance_reward(target_pos, base_pos)
                
                # Execute move
                self._execute_movement(target_pos)
                
                # Check for treasure collection
                if treasure_pos and target_pos == treasure_pos:
                    reward += 1
                    treasures_found = self.game.get_current_player_object().get_nb_found_treasures()
                    reward += 0.5 * treasures_found
                    self.game.remove_current_treasure()
                
                # Check for win condition
                if (self.game.get_current_player_remaining_treasure() == 0 and 
                    target_pos == base_pos):
                    reward += 5
                    terminated = True
                
                # Move to next player's turn
                self.game.next_player()
                self._previous_distance = None
            else:
                reward = -0.5

        observation = self._get_observation()
        info = {
            "phase": self._current_phase,
            "current_player": current_player,
            "treasures_remaining": self.game.get_current_player_remaining_treasure()
        }
        
        return observation, reward, terminated, truncated, info

    def _execute_movement(self, target_pos):
        """Execute player movement to target position"""
        current_pos = self.game.get_coord_player()
        self.game.remove_current_player_from_tile(*current_pos)
        self.game.put_current_player_in_tile(*target_pos)

    def _get_mouvements_possibles(self, joueur_id=None):
        """Get list of possible movements for current player"""
        current_pos = self.game.get_coord_player(joueur_id)
        mouvements = []
        
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if len(self.game.is_accessible(current_pos[0], current_pos[1], i, j)) > 0:
                    mouvements.append((i, j))
                        
        return mouvements

    def render(self):
        if self.render_mode == "human":
            if not hasattr(self, "graphique"):
                self.graphique = GUI_manager(
                    self.game, model="./modeles/best_model.zip", env=self
                )
            self.graphique.display_game()

    def close(self):
        pass