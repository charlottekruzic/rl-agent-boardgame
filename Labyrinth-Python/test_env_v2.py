import time
import random
from gym_env_lab_v2 import LabyrinthEnv

# Création de l'environnement et test rapide des fonctions
env = LabyrinthEnv()

num_tours = 1000
observation, info = env.reset()

for tour in range(num_tours):
    print(f"Tour {tour + 1}/{num_tours}")

    # Échantillonner une action depuis l'espace d'action
    action = env.action_space.sample()  # Action est un tuple (idx_insertion, idx_rotation, action_deplacement)

    # Afficher l'action choisie
    print(f"Action choisie : {action}")

    # Effectuer l'action
    observation, recompense, termine, tronque, info = env.step(action)

    # Afficher la récompense
    print(f"Récompense : {recompense}")

    # Afficher l'état du jeu
    env.render()
    # time.sleep(1)  # Décommentez si vous souhaitez une pause entre les tours

    if termine:
        print("Game over !")
        break

env.close()
