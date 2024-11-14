import sys
from eztext import *
from labyrinthe import Labyrinthe
from gui_manager import GUI_manager
from tile import Tile
import gymnasium as gym
import numpy as np


class GameEngine(gym.Env):
    """Main class of the game, managing the game parameters and the events of the menu window"""

    def __init__(self, human_players, ia_number, theme_directory):
        """Initialization of the Game class"""
        super().__init__()

        self.theme_directory = theme_directory
        self.human_players = human_players
        self.ia_number = ia_number
        assert (
            0 <= self.human_players <= 4
        ), "Nombre de joueurs humains doit être entre 0 et 4"
        assert 0 <= self.ia_number <= 4, "Nombre de IA doit être entre 0 et 4"
        assert (
            2 <= self.human_players + self.ia_number <= 4
        ), "La somme de joueurs humains et IA doit être entre 2 et 4"

        self.current_phase = 0  # Phase initiale (rotation+insertion)



        # 1. Définition de l'espace d'actions pour la phase de rotation et insertion
        # - 4 directions de rotation
        # - 12 insertions possibles (sans l'insertion invalide)
        self.action_space_rotation_insertion = gym.spaces.Discrete(4 * 12)  # 4 rotations x 12 insertions possibles

        # 2. Définition de l'espace d'actions pour la phase de déplacement
        # - 49 positions possibles, mais le déplacement est restreint par les positions accessibles
        self.action_space_deplacement = gym.spaces.Discrete(49)  # 7x7, donc 49 cases potentielles

        # 3. Vous pouvez avoir un espace d'actions combiné, si vous voulez gérer les phases séparément
        self.action_space = gym.spaces.Discrete(2)  # 2 phases : 0 pour rotation+insertion, 1 pour déplacement

        # self.observation_space = gym.spaces.Box(
        #     low=0,
        #     high=np.iinfo(np.int32).max,
        #     shape=(3, 7, 7),
        #     dtype=np.int32
        # )

        self.reset()

        # TODO labyrinthe reset
        # self.labyrinthe = Labyrinthe()

    def reset(self):

        # TODO labyrinthe reset
        # self.labyrinthe.reset()

        self.labyrinthe : Labyrinthe = Labyrinthe(
            num_human_players=self.human_players, num_ai_players=self.ia_number
        )
        self.coords_current_player = self.labyrinthe.coords_current_player
        self.gui = GUI_manager(self.labyrinthe, self.theme_directory)
        return self.get_observation()
    
    def get_observation(self):
        # 1. matrice d'accessibilité
        access = self.labyrinthe.get_matrice_accessibilite()
        
        # 2. matrice tuiles 
        tile_matrix = self.labyrinthe.get_matrice_tuiles()

        # 3. matrice position du joueur et du trésor
        position_matrix = self.labyrinthe.get_matrice_positions()
        # amélioration possible : 10 pour le trésor objectif, 1 pour joueur actuel, 2 2 2 pour autres joueurs 
        
        return np.stack([access, tile_matrix, position_matrix], axis=0)

    
    def step(self, action):
        reward = 0

        if self.current_phase == 0:  # Phase de rotation et 
            # comment faire pour interdire l'insertion invalide (1/ 12)
            rotate, insert = divmod(action, 12)  # Séparer rotation et insertion
            for _ in range(rotate):
                self.labyrinthe.rotate_tile()
            x_insert, y_insert = insert ???
            # TODO urgent

            # print pour debug
            if self.labyrinthe.is_forbidden_move(x_insert, y_insert):
                print("Coup interdit de rotation insertion", file=sys.stderr)
                reward = -10

            self.labyrinthe.play_tile(x_insert, y_insert)
            # TODO urgent :  # Calculer la récompense si un chemin plus proche du trésor a été construit
            # if self.labyrinthe.is_closer_to_treasure(x_insert, y_insert):
            #     reward += 5  # Récompense pour avoir rapproché le chemin du trésor
            # idem si il agrandit le nombre de cases auxquelles il a accès
            
            # TODO urgent
            # on pourrait calculer les cases accessibles depuis le trésor et faire en sorte 
            # de récompenser aussi si la zone d'accès est plus grande et se rapproche
            
            self.current_phase = 1  # Passer à la phase suivante : déplacement

            # reward : si il a construit un chemin plus proche du trésor
            # sinon 0, -10 si il n'a pas le droit de faire ce coup ?

        elif self.current_phase == 1:  # Phase de déplacement
            x_depl, y_depl = divmod(action, 7)
            x_ccp, y_ccp = self.labyrinthe.coords_current_player
            chemin = self.labyrinthe.is_accessible(x_ccp, y_ccp, x_depl, y_depl)

            if len(chemin) == 0:
                print("Coup interdit de déplacement", file=sys.stderr)
                reward -= 10

            self.labyrinthe.put_pawn(x_depl, y_depl)
            # si trésor trouvé : reward + = 10 # si dans case actuelle == current treasure
            # TODO urgent 
            # sinon -1
            # changer de joueur 
            # et idem pour retour base
            self.current_phase = 0  # Revenir à la phase 0

        
        done = self.labyrinthe.game_over()
        if done: 
            reward = 100  # Récompense pour avoir gagné la partie
            print(f"Fin de partie, joueur {self.labyrinthe.current_player} a gagné", file=sys.stderr)

        # reward = 1 if self.labyrinthe.current_treasure() == self.labyrinthe.board.get_value(x_depl, y_depl).get_treasure() else 0
        # self . calculate _ reward ( )
        # else : 
        #     self.labyrinthe.next_player()

        info = {
            "current_player": self.labyrinthe.current_player,
            "treasures_remaining": self.labyrinthe.get_remaining_treasures(),
            "reward": reward,
            "current_treasure_position": self.labyrinthe.get_coord_current_treasure(),
        }
        return self.get_observation(), reward, done, info


    def run(self):
        while self.running:
            self.gui.display_game()

            # si c'est au tour humain
            _, x_insert, y_insert = self.gui.get_action_phase_insertion()

            # # sinon si c'est un agent 
            # # get player roation / insertion action
            # rotate, x_insert, y_insert = self.get_action_phase_insertion()
            # for _ in range(rotate):
            #     self.labyrinthe.rotate_tile()

            # si coup interdit : print dans err 
            if self.labyrinthe.is_forbidden_move(x_insert, y_insert):
                print("Coup interdit de rotation insertion", file=sys.stderr)
                continue
            self.labyrinthe.play_tile(x_insert, y_insert)
            self.gui.display_game()

            # si c'est au tour humain 
            # get player deplacement
            x_depl, y_depl = self.gui.get_action_phase_deplacement()

            xD, yD = self.labyrinthe.coords_current_player
            chemin = self.labyrinthe.is_accessible(xD, yD, x_depl, y_depl)
            if len(chemin) == 0:
                print("Coup interdit de déplacement", file=sys.stderr)
                continue
            self.gui.animated_path(chemin) 

            # si trésor trouvé 
            current_treasure = self.labyrinthe.current_treasure()
            tile_treasure : Tile = self.labyrinthe.board.get_value(x_depl,y_depl)
            if tile_treasure.get_treasure() == current_treasure:
                self.labyrinthe.remove_current_treasure()
                self.gui.display_treasure_found(current_treasure)
                
            if self.labyrinthe.game_over():
                self.running = False
                print("Fin de partie, joueur ", self.labyrinthe.current_player, " a gagné")
                self.gui.display_fin_de_partie()

            else:
                self.labyrinthe.next_player()

    def render(self, mode="human"):
        """Display the game"""
        if mode == "human":
            self.gui.display_game()

    def close(self):
        """Close the game"""
        self.gui.quit()