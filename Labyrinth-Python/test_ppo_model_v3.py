import os
from time import sleep
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from gym_env_lab_v3 import LabyrinthEnv

# Créer l'environnement
def make_env():
    return LabyrinthEnv(num_human_players=2, num_ai_players=0, render_mode="human")

env = DummyVecEnv([make_env])

# Charger le modèle
model = PPO.load("ppo_labyrinth", env=env)

# Tester le modèle
observation = env.reset()
done = False
num_tours = 1000

for tour in range(num_tours):
    print(f"Tour {tour + 1}/{num_tours}")
    
    # Prédire l'action en utilisant le modèle
    action, _states = model.predict(observation)

    # Appliquer l'action dans l'environnement
    observation, recompense, done, info = env.step(action)

    # Afficher les détails
    print(f"Action prédite : {action}")
    print(f"Récompense : {recompense}")
    sleep(0.1)
    env.render()

    # if done:
    #     print("Game over!")
    #     break

env.close()
