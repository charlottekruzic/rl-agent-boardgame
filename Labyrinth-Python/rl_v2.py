import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from gymnasium.wrappers import FlattenObservation
from gym_env_lab_v2 import LabyrinthEnv

# Créer l'environnement et le wrapper
env = LabyrinthEnv()
env = FlattenObservation(env)

# Vérifier l'environnement
check_env(env)

# Créer le modèle PPO
model = PPO('MlpPolicy', env, verbose=1)

# Entraîner le modèle
total_timesteps = 100000
model.learn(total_timesteps=total_timesteps)

# Sauvegarder le modèle
model.save("ppo_labyrinthe")

# Évaluer le modèle
obs, _ = env.reset()
done = False

while not done:
    action, _states = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    env.render()
