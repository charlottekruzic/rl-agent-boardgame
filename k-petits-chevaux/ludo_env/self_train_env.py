import gymnasium as gym
import numpy as np
from ludo_env.mp_game_logic import GameLogic, NB_CHEVAUX, NUM_PLAYERS, TOTAL_SIZE, Action, BOARD_SIZE
from ludo_env.interface import Interface

class SelfLudoEnv(gym.Env):
    def __init__(self, with_render=False, print_action_invalide_mode=True, mode_jeu="normal"):
        super(SelfLudoEnv, self).__init__()
        self.metadata = {"render.modes": ["human", "rgb_array"], "render_fps": 10}
        self.with_render = with_render
        self.print_action_invalide_mode = print_action_invalide_mode
        self.mode_jeu = mode_jeu

        self.num_players = NUM_PLAYERS
        self.num_pawns = 2
        self.board_size = 56
        self.safe_zone_size = 6

        if self.with_render:
            self.renderer = Interface()

        # Action space remains the same
        self.action_space = gym.spaces.Discrete(
            2 + NUM_PLAYERS * (len(Action) - 2)
        )

        # Modified observation space to include player_id
        self.observation_space = gym.spaces.Dict({
            "my_board": gym.spaces.Box(
                low=0, high=NB_CHEVAUX, shape=(TOTAL_SIZE,), dtype=np.int8
            ),
            "dice_roll": gym.spaces.Discrete(7),
            "player_id": gym.spaces.Discrete(NUM_PLAYERS),  # Added player_id to observation
            "relative_positions": gym.spaces.Box(  # Added relative positions of other players
                low=0, 
                high=NB_CHEVAUX * (NUM_PLAYERS - 1), 
                shape=(BOARD_SIZE,), 
                dtype=np.int8
            )
        })

        self.reset()

    def _get_observation(self):
        obs = {
            "my_board": self.game.board[self.current_player],
            "dice_roll": self.dice_roll,
            "player_id": self.current_player,
            "relative_positions": self.game.get_board_pour_voir_ou_sont_adversaires_sur_mon_plateau(self.current_player)
        }
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.current_player = 0
        self.game = GameLogic()
        self.dice_roll = self.game.dice_generator()
        return self._get_observation(), {}

    def step(self, action):
        obs = self._get_observation()
        if self.mode_jeu == "debug":
            print("dé : ", obs["dice_roll"])
            print("my board : ", obs["my_board"])
            print("player_id : ", obs["player_id"])
        
        info = {}
        pawn_id, action_type = self.game.decode_action(action)
        valid_actions = self.game.get_valid_actions(self.current_player, self.dice_roll)
        encoded_valid_actions = self.game.encode_valid_actions(valid_actions)
        
        if action not in encoded_valid_actions:
            if self.print_action_invalide_mode:
                print(f"ACTION INTERDITE : {Action(action%len(Action))} not in valid_actions {valid_actions} : {encoded_valid_actions}")
            if self.mode_jeu == "debug":
                action = self.game.debug_action(encoded_valid_actions)
                pawn_id, action_type = self.game.decode_action(action)
                print("debug : ", action, pawn_id, action_type)
            else:
                return self._get_observation(), -10, False, False, info

        pawn_pos = self.game.get_pawns_info(self.current_player)[pawn_id]["position"]
        old_position = pawn_pos

        self.game.move_pawn(self.current_player, pawn_pos, self.dice_roll, action_type)

        # Get new position after move
        new_position = self.game.get_pawns_info(self.current_player)[pawn_id]["position"]

        # Calculate reward using enhanced reward system
        reward = self.game.get_reward(
            self.current_player, 
            action_type,
            old_position,
            new_position
        )
        done = self.game.is_game_over()

        if not done:
            self.current_player = (self.current_player + 1) % NUM_PLAYERS
            if self.current_player == 0:
                self.game.tour += 1

        self.dice_roll = self.game.dice_generator()
        observation = self._get_observation()
        return observation, reward, done, False, info

    def render(self, game, mode="human"):
        if self.with_render:
            self.renderer.render(self.game)