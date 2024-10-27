import gymnasium as gym
from gymnasium import spaces
import numpy as np

# Importer le code existant
from labyrinthe import Labyrinthe, NUM_TREASURES_PER_PLAYER
from matrix import DIMENSION
import random
from gui_manager import GUI_manager

class LabyrinthEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, num_human_players=2, num_ai_players=0, render_mode='human'):
        super(LabyrinthEnv, self).__init__()
        self.render_mode = render_mode

        # Initialiser le jeu Labyrinthe avec les joueurs spécifiés
        self.labyrinth = Labyrinthe(num_human_players, num_ai_players)

        # Définir l'espace d'action
        self.action_space = spaces.MultiDiscrete([
            4,  # rotation: 0°, 90°, 180°, 270°
            4,  # insertion_direction: N, E, S, O
            3,  # insertion_index: 0, 1, 2 (indices impairs 1,3,5)
            DIMENSION,  # move_row: 0 to DIMENSION-1
            DIMENSION   # move_col: 0 to DIMENSION-1
        ])

        # Définir l'espace d'observation
        self.observation_space = spaces.Dict({
            'board': spaces.Box(low=0, high=24, shape=(DIMENSION, DIMENSION, 6), dtype=np.float32),
            'tile_to_play': spaces.Box(low=0, high=24, shape=(6,), dtype=np.float32),
            'current_player': spaces.Discrete(self.labyrinth.get_num_players()),
            'player_positions': spaces.Box(low=0, high=DIMENSION-1, shape=(self.labyrinth.get_num_players(), 2), dtype=np.int32),
            'remaining_treasures': spaces.Box(low=0, high=NUM_TREASURES_PER_PLAYER, shape=(self.labyrinth.get_num_players(),), dtype=np.int32),
            'current_treasure': spaces.Discrete(NUM_TREASURES_PER_PLAYER * self.labyrinth.get_num_players() + 1)
        })

        self.current_player = self.labyrinth.get_current_player()
        self.done = False

    def reset(self, seed=None, options=None):
        # Appel à super().reset() pour gérer le seed si nécessaire
        super().reset(seed=seed)

        # Initialiser le seed si fourni
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
            # Si votre code utilise d'autres modules aléatoires, initialisez-les ici

        # Réinitialiser le jeu
        self.labyrinth = Labyrinthe(2, 0)  # Deux IA pour commencer
        self.current_player = self.labyrinth.get_current_player()
        self.done = False

        # Générer l'observation
        observation = self._get_observation()
        info = {}

        return observation, info

    def step(self, action):
        info = {}

        if self.done:
            # Si l'épisode est terminé, retourner l'observation actuelle
            return self._get_observation(), 0, True, False, info

        reward = 0

        # Extraire les sous-actions
        rotation, insertion_direction_idx, insertion_index_idx, move_row, move_col = action

        # Étape 1 : Rotation de la tuile
        for _ in range(rotation):
            self.labyrinth.rotate_tile()

        # Étape 2 : Insertion de la tuile
        direction_mapping = {0: 'N', 1: 'E', 2: 'S', 3: 'O'}
        insertion_direction = direction_mapping[insertion_direction_idx % 4]

        insertion_indices = [1, 3, 5]  # Indices impairs pour un plateau 7x7
        insertion_index = insertion_indices[insertion_index_idx % len(insertion_indices)]

        if self.labyrinth.is_forbidden_move(insertion_direction, insertion_index):
            reward -= 1  # Pénalité pour mouvement interdit
            self.done = True
            # Terminated=True, Truncated=False
            return self._get_observation(), reward, True, False, info

        self.labyrinth.play_tile(insertion_direction, insertion_index)

        # Étape 3 : Déplacement du joueur
        move_row = move_row % DIMENSION
        move_col = move_col % DIMENSION

        current_pos = self.labyrinth.get_coord_current_player()

        path = self.labyrinth.is_accessible(current_pos[0], current_pos[1], move_row, move_col)
        if len(path) == 0:
            reward -= 1  # Pénalité pour déplacement invalide
            self.done = True
            # Terminated=True, Truncated=False
            return self._get_observation(), reward, True, False, info

        # Déplacer le joueur le long du chemin
        for x, y in path[1:]:
            self.labyrinth.remove_current_player_from_tile(current_pos[0], current_pos[1])
            self.labyrinth.put_current_player_in_tile(x, y)
            current_pos = (x, y)

        # Vérifier si le joueur a trouvé un trésor
        tile = self.labyrinth.board.get_value(current_pos[0], current_pos[1])
        current_treasure = self.labyrinth.current_treasure()
        if tile.get_treasure() == current_treasure:
            self.labyrinth.get_current_player_num_find_treasure()
            reward += 10  # Récompense pour avoir trouvé un trésor
            if self.labyrinth.get_current_player_remaining_treasure() == 0:
                reward += 100  # Récompense pour avoir collecté tous les trésors
                self.done = True

        # Passer au joueur suivant
        self.labyrinth.next_player()
        self.current_player = self.labyrinth.get_current_player()

        # Vérifier si le jeu est terminé (tout le monde a fini)
        # Si vous avez une condition spécifique, vous pouvez la vérifier ici

        # Terminated=False, Truncated=False
        return self._get_observation(), reward, self.done, False, info

    def render(self):
        if not hasattr(self, "graphique"):
            self.graphique = GUI_manager(self.labyrinth)
        self.graphique.display_game()

    def close(self):
        if hasattr(self, "graphique"):
            self.graphique.close()
        super().close()

    def _get_observation(self):
        # Générer l'observation à partir de l'état du jeu
        board_obs = np.zeros((DIMENSION, DIMENSION, 6), dtype=np.float32)
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                tile = self.labyrinth.board.get_value(i, j)
                board_obs[i, j, 0] = 1.0 if tile.way_north() else 0.0
                board_obs[i, j, 1] = 1.0 if tile.way_east() else 0.0
                board_obs[i, j, 2] = 1.0 if tile.way_south() else 0.0
                board_obs[i, j, 3] = 1.0 if tile.way_west() else 0.0
                board_obs[i, j, 4] = float(tile.get_treasure())  # Ajusté le high dans observation_space
                board_obs[i, j, 5] = float(tile.is_base())

        tile_to_play = self.labyrinth.get_tile_to_play()
        tile_obs = np.array([
            1.0 if tile_to_play.way_north() else 0.0,
            1.0 if tile_to_play.way_east() else 0.0,
            1.0 if tile_to_play.way_south() else 0.0,
            1.0 if tile_to_play.way_west() else 0.0,
            float(tile_to_play.get_treasure()),
            float(tile_to_play.is_base())
        ], dtype=np.float32)

        player_positions = np.zeros((self.labyrinth.get_num_players(), 2), dtype=np.int32)
        for player_id in range(1, self.labyrinth.get_num_players() + 1):
            pos = self._get_player_position(player_id)
            player_positions[player_id - 1] = pos

        remaining_treasures = np.zeros(self.labyrinth.get_num_players(), dtype=np.int32)
        for player_id in range(1, self.labyrinth.get_num_players() + 1):
            remaining_treasures[player_id - 1] = self.labyrinth.get_remaining_treasures(player_id)

        current_treasure = self.labyrinth.current_treasure() or 0
        current_treasure = int(current_treasure)
        max_treasure = NUM_TREASURES_PER_PLAYER * self.labyrinth.get_num_players()
        current_treasure = min(current_treasure, max_treasure)
        assert 0 <= current_treasure < (max_treasure + 1), f"current_treasure={current_treasure} out of range"

        observation = {
            'board': board_obs,
            'tile_to_play': tile_obs,
            'current_player': self.current_player - 1,
            'player_positions': player_positions,
            'remaining_treasures': remaining_treasures,
            'current_treasure': current_treasure
        }

        return observation

    def _get_player_position(self, player_id):
        # Obtenir la position du joueur spécifié
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                tile = self.labyrinth.board.get_value(i, j)
                if tile.has_pawn(player_id):
                    return np.array([i, j], dtype=np.int32)
        return np.array([-1, -1], dtype=np.int32)  # Si le joueur n'est pas trouvé (ne devrait pas arriver)
