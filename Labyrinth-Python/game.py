import sys
from eztext import *
from labyrinthe import Labyrinthe
from gui_manager import GUI_manager
from tile import Tile


class GameEngine(object):
    """Main class of the game, managing the game parameters and the events of the menu window"""

    def __init__(self, human_players, ia_number, theme_directory, use_rl_agent=True):
        """Initialization of the Game class"""

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
        
        self.running = True
        self.gui = None # GUI_manager(self.theme_directory)

        self.reset()

    def reset(self):
        self.labyrinthe : Labyrinthe = Labyrinthe(
            num_human_players=self.human_players, num_ai_players=self.ia_number
        )
        self.gui = GUI_manager(self.labyrinthe, self.theme_directory)

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

    # def reset(self):
    #     """Reset the game"""
# 
    #     self.current_step = 0
    #     self.phase = 0  # Commence par la phase d'insertion
# 
    #     # Réinitialiser l'action_space pour la phase d'insertion
    #     self.action_space = self.action_space_insertion
# 
    #     # Fixer une seed aléatoire
    #     self.np_random, seed = gym.utils.seeding.np_random(seed)
# 
    #     # Initialisation du jeu
    #     self.game = Labyrinthe(
    #         num_human_players=num_human_players, num_ai_players=num_ai_players
    #     )
# 
    #     self.termine = False
    #     self.derniere_insertion = None
# 
    #     return self._get_observation(), {}
    # 
    #     self.env.reset()
    #     self.env.render(mode="human")
# 
    # def step(self, action):
# 
# 
    # def render(self):
    #     """Render the game"""
# 
    # def close(self):