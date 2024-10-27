import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from stable_baselines3 import PPO
from gymnasium.wrappers import FlattenObservation
from gym_env_lab_v2 import LabyrinthEnv

# Créer et envelopper l'environnement
env = LabyrinthEnv()
# Utiliser FlattenObservation si LabyrinthEnv renvoie bien une Box
env = FlattenObservation(env)

# Charger le modèle
model = PPO.load("ppo_labyrinthe")

# Tester le modèle
observation, info = env.reset()
done = False
num_tours = 1000

for tour in range(num_tours):
    print(f"Tour {tour + 1}/{num_tours}")
    
    # Prédire l'action en utilisant le modèle
    action, _states = model.predict(observation)

    # Appliquer l'action dans l'environnement
    observation, recompense, done, tronque, info = env.step(action)

    # Afficher les détails
    print(f"Action prédite : {action}")
    print(f"Récompense : {recompense}")
    env.render()

    if done:
        print("Game over!")
        break

env.close()

