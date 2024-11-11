from labyrinthe import Labyrinthe
from gui_manager import GUI_manager
import gymnasium as gym
import numpy as np
import random
import math
import time


class LabyrinthEnv(gym.Env):
    def __init__(self, num_human_players=0, num_ai_players=2,max_steps=-1, render_mode="human", epsilon=1.0, epsilon_decay=0.999, min_epsilon=0.1):
        super(LabyrinthEnv, self).__init__()

        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

        self.max_steps = max_steps
        self.current_step = 0
        self.phase = 0
        self.joueur_actuel = 1

        self.mouvements_possibles = []
        self.termine = False
        self.derniere_insertion = None
        self.render_mode = render_mode

        self.action_space = gym.spaces.MultiDiscrete([4, 12, 49])

        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(7 * 7 * 5,), dtype=np.float32)
     
        self.num_human_players = num_human_players
        self.num_ai_players = num_ai_players

        self.reset(self.num_human_players, self.num_ai_players)


    def reset(self, num_human_players=0, num_ai_players=2, seed=None, options=None):
        self.current_step = 0
        self.phase = 0
        self.joueur_actuel = 1

        self.mouvements_possibles = []
        self.termine = False
        self.derniere_insertion = None


        self.np_random, seed = gym.utils.seeding.np_random(seed)
        self.game = Labyrinthe(num_human_players=num_human_players, num_ai_players=num_ai_players)

        self.recompense = {player_id: 0 for player_id in range(num_human_players + num_ai_players)}

        self.action_mask = self._get_action_mask()
        info = {"action_modified" : False, "action_mask" : self.action_mask}
        return self._get_observation(), info


    def step(self, action):

        self.current_step += 1

        joueur_id = self.game.get_current_player()
        recompense = 0

        info = {}

        #action_mask = self._get_action_mask() 
        
        rotation_idx, insertion_idx, mouvement_idx = action

        # Phase d'insertion
        if self.phase == 0:

            # Eviter de tourner en rond
            if np.random.rand() < self.epsilon:
                original_insertion_idx = insertion_idx
                insertion_idx = np.random.choice(np.where(self.action_mask[1] == 1)[0])
                info["action_modified"] = True
                recompense -= 0.05
                
            #rotation_idx, insertion_idx = action

            #print("Rotation choisie : ", rotation_idx)
            #print("Insertion choisie : ", insertion_idx)

            self._appliquer_rotation(rotation_idx)
            

            if self._est_insertion_interdite(insertion_idx):
                recompense += -0.7
                print("insertion interdite !")
            else:
                print("insertion : ", insertion_idx)
                print("masque insertion : ", self.action_mask) 
                #print("derniere insertion : ", self.derniere_insertion)
                self.derniere_insertion = insertion_idx
                direction, rangee = self._get_insertion(insertion_idx)
                self.game.play_tile(direction, rangee)
                self.mouvements_possibles = self._get_mouvements_possibles()

        
            #self.action_space = self.action_space_deplacement
            

            termine = False
            tronque = False

            self.phase = 1
            self.action_mask = self._get_action_mask()
            
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
            self.recompense[joueur_id] += recompense
            info["action_mask"] =  self.action_mask
            return self._get_observation(), self.recompense[joueur_id], termine, tronque, info

        # Phase de déplacement
        elif self.phase == 1:
            
            #mouvement_idx = action
            #print("Mouvement choisi : ", mouvement_idx)
            print("mask : ", self.action_mask)

            actions_possibles = np.where(self.action_mask == 1)[0]
            #print("Actions possibles selon le masque : ", actions_possibles)

            if self.action_mask[mouvement_idx] == 0:
                print("Mouvement invalide !")
                recompense -= 0.7
                termine = False
                tronque = False
                self.game.next_player()
                self.recompense[joueur_id] += recompense
                self.phase = 0
                info["action_mask"] =  self.action_mask
                return self._get_observation(), self.recompense[joueur_id], termine, tronque, info
            else:
                print("deplacement : ", mouvement_idx)
                ancienne_position = self.game.get_coord_player()
                ligne, colonne = divmod(mouvement_idx, 7)
                nouvelle_position = (ligne, colonne)
                self._deplacer_joueur(nouvelle_position)


            # Trésor trouvé
            if self._is_tresor_trouve():
                self.game.get_current_player_num_find_treasure()
                recompense += 5 
            
            # Position par rapport au trésor
            else:
                if self.se_rapproche_du_tresor(ancienne_position, nouvelle_position):
                    recompense += 0.2
                else:
                    recompense += -0.2


            
            gagnant = self.game.players.check_for_winner()
            if gagnant is not None:
                print(f"Le joueur {gagnant} a gagné la partie !")
                termine = True
            else:
                termine = False

    
            tronque = False

            if self.max_steps != -1 and (self.current_step >= self.max_steps):
                print("Nombre maximum de tours atteint !")
                recompense += -5
                termine = True
                tronque = True


            self.phase = 0
            self.game.next_player()

            self.action_mask = self._get_action_mask()

            self.recompense[joueur_id] += recompense
            info["action_mask"] =  self.action_mask
            return self._get_observation(), self.recompense[joueur_id], termine, tronque, info

    def _get_action_mask(self):
        if self.phase == 0:
            mask_0 = np.ones(4, dtype=np.int32) 
            mask_1 = np.ones(12, dtype=np.int32)
            
            if self.derniere_insertion is not None:
                mask_1[(self.derniere_insertion + 6) % 12] = 0
            
            return [mask_0, mask_1]

        elif self.phase == 1:
            mask_2 = np.zeros(49, dtype=np.int32)
            self.mouvements_possibles = self._get_mouvements_possibles()
            for x, y in self.mouvements_possibles:
                index = x * 7 + y
                mask_2[index] = 1
        
            return mask_2

        else:
            raise ValueError("Phase inconnue")


    def se_rapproche_du_tresor(self, ancienne_position, nouvelle_position, joueur_id=None):
        if joueur_id is None:
            joueur_id = self.game.get_current_player()
        
        position_tresor = self.game.get_coord_current_treasure()

        if position_tresor is None:
            return True


        def distance_manhattan(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        distance_avant = distance_manhattan(ancienne_position, position_tresor)
        distance_apres = distance_manhattan(nouvelle_position, position_tresor)

        return distance_apres < distance_avant


    def render(self):
        if self.render_mode == "human":
            if not hasattr(self, "graphique"):
                self.graphique = GUI_manager(self.game, model="./modeles/best_model.zip", env=self)
            self.graphique.display_game()

    def close(self):
        if hasattr(self, "graphique"):
            self.graphique.close()
        #pygame.quit()  # ferme pygame
        super().close()


    def _get_observation(self):
        infos_labyrinthe = np.zeros((7, 7, 5), dtype=np.float32)
        plateau = self.game.get_board()

        # Récupération des infos sur le plateau
        for i in range(7):
            for j in range(7):
                carte = plateau.get_value(i, j)
                # Infos murs
                infos_labyrinthe[i, j, 0] = 1 if carte.wall_north() else 0
                infos_labyrinthe[i, j, 1] = 1 if carte.wall_south() else 0
                infos_labyrinthe[i, j, 2] = 1 if carte.wall_east() else 0
                infos_labyrinthe[i, j, 3] = 1 if carte.wall_west() else 0
                # Infos joueur : 1 si le joueur courant est présent
                if carte.has_pawn(self.game.get_current_player()):
                    infos_labyrinthe[i, j, 4] = 1

        return infos_labyrinthe.flatten().astype(np.float32)

    def _is_tresor_trouve(self):
        joueur_pos = self.game.get_coord_player()
        tresor_pos = self.game.get_coord_current_treasure()
        return joueur_pos == tresor_pos

    def _deplacer_joueur(self, new_position):
        ligD, colD = self.game.get_coord_player()
        ligA, colA = new_position
        self.game.remove_current_player_from_tile(ligD, colD)
        self.game.put_current_player_in_tile(ligA, colA)

        joueur_courant = self.game.players.players[self.game.get_current_player()]
        joueur_courant.move_to((ligA, colA))

    def _get_mouvements_possibles(self, joueur_id=None):
        if joueur_id is None:
            joueur_id = self.game.get_current_player()
        
        ligD, colD = self.game.get_coord_player(joueur_id)
        mouvements_possibles = []

        # Utiliser une recherche en largeur pour trouver toutes les positions accessibles
        visited = [[False for _ in range(7)] for _ in range(7)]
        queue = [(ligD, colD)]
        visited[ligD][colD] = True

        while queue:
            x, y = queue.pop(0)
            mouvements_possibles.append((x, y))

            voisins = self._get_voisins_accessibles(x, y)
            for vx, vy in voisins:
                if not visited[vx][vy]:
                    visited[vx][vy] = True
                    queue.append((vx, vy))

        return mouvements_possibles

    def _get_voisins_accessibles(self, x, y):
        voisins = []
        tile = self.game.board.get_value(x, y)

        # Nord
        if x > 0 and tile.can_go_north(self.game.board.get_value(x - 1, y)):
            voisins.append((x - 1, y))
        # Sud
        if x < 6 and tile.can_go_south(self.game.board.get_value(x + 1, y)):
            voisins.append((x + 1, y))
        # Est
        if y < 6 and tile.can_go_east(self.game.board.get_value(x, y + 1)):
            voisins.append((x, y + 1))
        # Ouest
        if y > 0 and tile.can_go_west(self.game.board.get_value(x, y - 1)):
            voisins.append((x, y - 1))

        return voisins

    def _est_insertion_interdite(self, idx_insertion):
        if self.derniere_insertion is None:
            return False

        if idx_insertion == (self.derniere_insertion + 6) % 12:
            return True
        return False

    def _get_insertion(self, idx_insertion):
        rangees_ok = [1, 3, 5]

        if idx_insertion < 3:
            #print("N", rangees_ok[idx_insertion])
            return ("N", rangees_ok[idx_insertion])
        elif idx_insertion < 6:
            #print("S", rangees_ok[idx_insertion % 3])
            return ("S", rangees_ok[idx_insertion % 3])
        elif idx_insertion < 9:
            #print("E", rangees_ok[idx_insertion % 3])
            return ("E", rangees_ok[idx_insertion % 3])
        else:
            #print("O", rangees_ok[idx_insertion % 3])
            return ("O", rangees_ok[idx_insertion % 3])

    def _appliquer_rotation(self, rotation_idx):
        # 0: 0°, 1: 90°, 2: 180°, 3: 270°
        for _ in range(rotation_idx):
            self.game.rotate_tile("H")


    