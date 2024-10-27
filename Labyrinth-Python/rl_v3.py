import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import gymnasium as gym
from gym_env_lab_v3 import LabyrinthEnv

# Créer l'environnement
def make_env():
    return LabyrinthEnv(num_human_players=2, num_ai_players=0)

env = DummyVecEnv([make_env])

# Créer le modèle
model = PPO('MultiInputPolicy', env, verbose=1)

# Entraîner le modèle
model.learn(total_timesteps=100000)

# Sauvegarder le modèle
model.save("ppo_labyrinth")
