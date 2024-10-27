import gymnasium as gym
from gymnasium import spaces
import numpy as np
from labyrinthe import NUM_TREASURES, NUM_TREASURES_PER_PLAYER, Labyrinthe
from gui_manager import GUI_manager

# Environnement Gym pour le jeu Labyrinthe
class LabyrinthEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, max_steps=-1):
        super(LabyrinthEnv, self).__init__()

        self.max_steps = max_steps
        self.current_step = 0

        # Calculer le nombre total d'actions possibles
        self.num_insertion = 12
        self.num_rotation = 4
        self.num_deplacement = 49
        self.total_actions = self.num_insertion * self.num_rotation * self.num_deplacement

        # Espace d'action aplati
        self.action_space = spaces.Discrete(self.total_actions)

        # Espace d'observation
        self.observation_space = spaces.Dict({
            'plateau': spaces.Box(low=0, high=1, shape=(7, 7, 6), dtype=np.float32),
            'tuile_sup': spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32),
            'tresor_a_trouver': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)
        })

        self.joueur_actuel = 1
        self.termine = False
        self.derniere_insertion = None

        self.reset()

    def _decode_action(self, action):
        idx_insertion = action // (self.num_rotation * self.num_deplacement)
        reste = action % (self.num_rotation * self.num_deplacement)
        idx_rotation = reste // self.num_deplacement
        action_deplacement = reste % self.num_deplacement
        return idx_insertion, idx_rotation, action_deplacement

    def reset(self, seed=None, options=None):
        self.current_step = 0
        self.np_random, seed = gym.utils.seeding.np_random(seed)

        # Paramètres du jeu
        self.game = Labyrinthe(num_human_players=2, num_ai_players=0)

        self.termine = False
        self.derniere_insertion = None
        return self._get_observation(), {}

    def step(self, action):
        self.current_step += 1

        # Décoder l'action
        idx_insertion, idx_rotation, action_deplacement = self._decode_action(action)

        # Vérification de l'insertion interdite
        if self._est_interdit(idx_insertion):
            recompense = -10  # Récompense : -10 si mouvement interdit
            termine = False
            tronque = False
            return self._get_observation(), recompense, termine, tronque, {}

        direction, rangee = self._get_insertion(idx_insertion)

        # Rotation de la tuile supplémentaire
        for _ in range(idx_rotation):
            self.game.rotate_tile("H")  # "H" pour sens horaire

        # Insertion de la tuile
        self.game.play_tile(direction, rangee)
        self.derniere_insertion = idx_insertion

        # Calcul des mouvements possibles
        mouvements_ok = self._get_mouvements_ok()

        if not mouvements_ok:
            # Si aucun mouvement possible, pénalité
            recompense = -5
        else:
            # Conversion de l'action de déplacement en coordonnées
            ligA, colA = divmod(action_deplacement, 7)
            if (ligA, colA) in mouvements_ok:
                # Calculer la récompense basée sur la distance au trésor (a voir si c'est efficace)
                position_joueur_avant = self.game.get_coord_current_player()
                distance_avant = self._distance_au_tresor(position_joueur_avant)
                self._deplacer_joueur((ligA, colA))
                distance_apres = self._distance_au_tresor((ligA, colA))
                recompense = (distance_avant - distance_apres) * 0.1  # Ajuster si nécessaire

                # Vérifier si le joueur a trouvé le trésor
                if self._is_tresor_trouve():
                    self.game.get_current_player_num_find_treasure()
                    recompense += 100  # Grande récompense pour avoir trouvé le trésor
                    self.termine = True
            else:
                # Mouvement invalide
                recompense = -10  # Récompense : -10 si le mouvement est invalide

        # Vérification de la fin de la partie
        gagnant = self.game.players.check_for_winner()
        if gagnant is not None:
            print(f"Le joueur {gagnant} a gagné la partie !")
            termine = True
        else:
            termine = False

        if self.max_steps != -1 and (self.current_step >= self.max_steps):
            termine = True

        tronque = False  # À définir si on veut arrêter la partie avant la fin

        # Passage au joueur suivant
        if not termine:
            self.game.next_player()

        return self._get_observation(), recompense, termine, tronque, {}
    
    def render(self, mode='human'):
        if not hasattr(self, "graphique"):
            self.graphique = GUI_manager(self.game)
        self.graphique.display_game()

    def close(self):
        if hasattr(self, "graphique"):
            self.graphique.close()
        super().close()

    def _get_observation(self):
        infos_labyrinthe = np.zeros((7, 7, 6), dtype=np.float32)
        plateau = self.game.get_board()

        for i in range(7):
            for j in range(7):
                carte = plateau.get_value(i, j)
                # Infos murs
                infos_labyrinthe[i, j, 0] = carte.wall_north()
                infos_labyrinthe[i, j, 1] = carte.wall_south()
                infos_labyrinthe[i, j, 2] = carte.wall_east()
                infos_labyrinthe[i, j, 3] = carte.wall_west()
                # Infos joueur
                infos_labyrinthe[i, j, 4] = 1 if carte.get_nb_pawns() > 0 else 0
                # Infos trésor
                infos_labyrinthe[i, j, 5] = 1 if carte.get_treasure() is not None else 0

        # Infos sur la tuile supplémentaire
        tuile_sup = np.array([
            self.game.get_tile_to_play().wall_north(),
            self.game.get_tile_to_play().wall_south(),
            self.game.get_tile_to_play().wall_east(),
            self.game.get_tile_to_play().wall_west(),
            1 if self.game.get_tile_to_play().get_treasure() is not None else 0
        ], dtype=np.float32)

        # Trésor à trouver (normalisé entre 0 et 1)
        current_treasure = self.game.current_treasure()
        if current_treasure is not None:
            tresor_a_trouver = np.array([current_treasure / NUM_TREASURES], dtype=np.float32)
        else:
            tresor_a_trouver = np.array([0.0], dtype=np.float32)

        # Combiner les observations
        observation = {
            'plateau': infos_labyrinthe,
            'tuile_sup': tuile_sup,
            'tresor_a_trouver': tresor_a_trouver
        }

        return observation
    
    def _distance_au_tresor(self, position):
        x1, y1 = position
        tresor_pos = self.game.get_coord_current_treasure()
        if tresor_pos is None:
            return 0
        x2, y2 = tresor_pos
        return abs(x1 - x2) + abs(y1 - y2)  # Distance de Manhattan


    def _is_tresor_trouve(self):
        joueur_pos = self.game.get_coord_current_player()
        tresor_pos = self.game.get_coord_current_treasure()

        return joueur_pos == tresor_pos

    def _deplacer_joueur(self, new_position):
        ligD, colD = self.game.get_coord_current_player()
        ligA, colA = new_position
        self.game.remove_current_player_from_tile(ligD, colD)
        self.game.put_current_player_in_tile(ligA, colA)

        joueur_courant = self.game.players.players[self.game.get_current_player()]
        joueur_courant.move_to((ligA, colA))

    def _get_mouvements_ok(self):
        ligD, colD = self.game.get_coord_current_player()
        mouvements_ok = []

        for ligA in range(7):
            for colA in range(7):
                if self.game.accessible(ligD, colD, ligA, colA):
                    mouvements_ok.append((ligA, colA))

        return mouvements_ok

    def _est_interdit(self, idx_insertion):
        if self.derniere_insertion is None:
            return False

        idx_inverse = (idx_insertion + 6) % 12
        return idx_insertion == idx_inverse

    def _get_insertion(self, idx_insertion):
        rangees_ok = [1, 3, 5]

        if idx_insertion < 3:
            return ("N", rangees_ok[idx_insertion])
        elif idx_insertion < 6:
            return ("S", rangees_ok[idx_insertion % 3])
        elif idx_insertion < 9:
            return ("E", rangees_ok[idx_insertion % 3])
        else:
            return ("O", rangees_ok[idx_insertion % 3])
