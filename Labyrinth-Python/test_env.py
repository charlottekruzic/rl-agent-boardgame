import time
import random
from gym_env_labyrinthe import LabyrinthEnv

# Création de l'environnement et test rapide des fonctions
env = LabyrinthEnv()

num_tours = 1000
observation, info = env.reset()

for tour in range(num_tours):
    print(f"Tour {tour + 1}/{num_tours}")

    # Vérifier la phase actuelle
    phase = env.phase

    if phase == 0:
        # Phase d'insertion
        # L'espace des actions est MultiDiscrete([4, 12])
        action = env.action_space.sample()  # Action est une liste [rotation_idx, insertion_idx]
        print(f"Phase d'insertion - Action choisie : Rotation {action[0]}, Insertion {action[1]}")

    elif phase == 1:
        # Phase de déplacement
        # L'espace des actions est Discrete(n), où n est le nombre de mouvements possibles
        action = env.action_space.sample()  # Action est un entier représentant l'index du mouvement
        print(f"Phase de déplacement - Action choisie : Mouvement index {action}")

    else:
        # Cas improbable, mais on le gère par sécurité
        print("Phase inconnue !")
        break

    # Effectuer l'action
    observation, recompense, termine, tronque, info = env.step(action)

    print(f"Recompense : {recompense}")

    env.render()
    # time.sleep(1)

    if termine:
        print("Game over !")
        break

env.close()
