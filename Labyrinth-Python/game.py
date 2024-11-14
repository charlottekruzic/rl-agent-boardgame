import sys
from eztext import *
from gui_manager import *
from stable_baselines3 import PPO

from gym_env_2dim import LabyrinthEnv


class GameEngine(object):
    """Main class of the game, managing the game parameters and the events of the menu window"""

    def __init__(self, human_players, ia_number, theme_directory, use_rl_agent=True):
        """Initialization of the Game class"""

        self.theme_directory = theme_directory

        self.human_players = human_players
        self.ia_number = ia_number
        self.use_rl_agent = use_rl_agent

        assert (
            0 <= self.human_players <= 4
        ), "Nombre de joueurs humains doit être entre 0 et 4"
        assert 0 <= self.ia_number <= 4, "Nombre de IA doit être entre 0 et 4"
        assert (
            2 <= self.human_players + self.ia_number <= 4
        ), "La somme de joueurs humains et IA doit être entre 2 et 4"


        self.env = LabyrinthEnv(
            num_human_players=human_players,
            num_ai_players=ia_number,
            render_mode="human",
        )
        
        self.model = None
        if self.use_rl_agent:
            self.model = PPO.load("./modeles/best_model.zip")

        self.running = True

    def launch(self):
        """Launch the game"""
       
        g = GUI_manager(
            self.env.game, self.model, self.env, prefixeImage=self.theme_directory
        )

        g.start()
        

    def reset(self):
        # mettre les pions dans leur base
        # plcer les tuiles 

        self.labyrinthe = Labyrinthe(
            num_human_players=self.human_players, num_ai_players=self.ia_number
        )

        # self.state = self.get_initial_state() ? 

        self.phase = 1

    def fin_de_partie(self):
        if self.labyrinthe.player_at_start():
            print("Partie terminée")
            self.running = False

        
    def get_player_action(self):
        """Get the action of the player"""
        if self.use_rl_agent:
            action, _ = self.model.predict(self.state, deterministic=True)
            return action
        else:
            # Attendre une action du joueur
            return self.gui_manager.get_player_action()

    def run(self):
        while self.running:


            # si c'est au tour humain
            # get player roation / insertion action
            _, x_insert, y_insert = self.get_action_phase_insertion()

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

            # update display de la grille

            # si c'est au tour humain 
            # get player deplacement
            x_depl, y_depl = self.get_action_phase_deplacement()

            curr_player = self.labyrinthe.get_current_player()
            xD, yD = self.labyrinthe.coords_current_player
            chemin = self.labyrinthe.is_accessible(xD, yD, x_depl, y_depl)
            if len(chemin) == 0:
                print("Coup interdit de déplacement", file=sys.stderr)
                continue

            # gui.animated_path 

            # si current treasure trouvé 
            current_treasure = self.labyrinthe.get_current_treasure()
            tile_treasure = self.labyrinthe.board.get_value(x_depl,y_depl)
            if tile_treasure == current_treasure.get_treasure():
                print("Trésor trouvé")
                self.labyrinthe.remove_current_treasure()
                # update display trésor troubé

            # si il doit juste retourner à la base
            # display update
                
            self.fin_de_partie()
            # sinon changement de joueur : self.labyrinthe.next_player()

            # si fin de partie 
            # update display fin de partie 


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