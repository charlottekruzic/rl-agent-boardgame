from stable_baselines3 import PPO
from typing import Dict, List, Optional, Tuple
import numpy as np
import os
import datetime
from collections import deque

class SelfPlayManager:
    def __init__(
        self,
        env,
        num_players: int = 2,
        save_freq: int = 10000,
        eval_freq: int = 5000,
        num_eval_episodes: int = 100,
        win_rate_threshold: float = 0.55,
        models_to_keep: int = 5
    ):
        """
        Manages self-play training, model versioning, and evaluation.
        
        Args:
            env: The Ludo environment
            num_players: Number of players in the game
            save_freq: How often to save models (in timesteps)
            eval_freq: How often to evaluate models (in timesteps)
            num_eval_episodes: Number of episodes for evaluation
            win_rate_threshold: Required win rate to update best model
            models_to_keep: Number of past model versions to maintain
        """
        self.env = env
        self.num_players = num_players
        self.save_freq = save_freq
        self.eval_freq = eval_freq
        self.num_eval_episodes = num_eval_episodes
        self.win_rate_threshold = win_rate_threshold
        self.models_to_keep = models_to_keep
        
        # Initialize model versions
        self.current_models: Dict[int, PPO] = {}
        self.best_models: Dict[int, PPO] = {}
        self.past_versions: Dict[int, List[PPO]] = {i: [] for i in range(num_players)}
        
        # Training metrics
        self.win_rates = deque(maxlen=100)
        self.rewards_history = deque(maxlen=100)
        
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize models for all players."""
        for player_id in range(self.num_players):
            self.current_models[player_id] = PPO(
                "MultiInputPolicy",
                self.env,
                verbose=1,
                tensorboard_log=f"./tensorboard_logs/player_{player_id}/"
            )
            self.best_models[player_id] = self.current_models[player_id]
    
    def save_model_version(self, player_id: int, model: PPO, version: int):
        """Save a model version to disk."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"models/player_{player_id}/version_{version}_{timestamp}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        model.save(path)
        return path
    
    def evaluate_model(self, player_id: int, model: PPO) -> Tuple[float, float]:
        """
        Evaluate a model against past versions and best models.
        Returns win rate and average reward.
        """
        wins = 0
        total_reward = 0
        
        for episode in range(self.num_eval_episodes):
            obs, _ = self.env.reset()
            episode_reward = 0
            done = False
            
            while not done:
                current_player = obs["player_id"]
                
                if current_player == player_id:
                    # Use the model being evaluated
                    action, _ = model.predict(obs, deterministic=True)
                else:
                    # Use a random past version or best model for opponent
                    opponent_model = self._select_opponent_model(current_player)
                    action, _ = opponent_model.predict(obs, deterministic=True)
                
                obs, reward, done, _, _ = self.env.step(action)
                episode_reward += reward
                
                if done and self.env.game.is_winner() == player_id:
                    wins += 1
            
            total_reward += episode_reward
        
        win_rate = wins / self.num_eval_episodes
        avg_reward = total_reward / self.num_eval_episodes
        
        return win_rate, avg_reward
    
    def _select_opponent_model(self, player_id: int) -> PPO:
        """Select an opponent model from past versions or best model."""
        if len(self.past_versions[player_id]) == 0:
            return self.best_models[player_id]
        
        # 80% chance to use best model, 20% chance to use random past version
        if np.random.random() < 0.8:
            return self.best_models[player_id]
        else:
            return np.random.choice(self.past_versions[player_id])
    
    def update_best_model(self, player_id: int, model: PPO, win_rate: float):
        """Update best model if win rate exceeds threshold."""
        if win_rate > self.win_rate_threshold:
            # Store current best model in past versions
            if len(self.past_versions[player_id]) >= self.models_to_keep:
                self.past_versions[player_id].pop(0)  # Remove oldest version
            self.past_versions[player_id].append(self.best_models[player_id])
            
            # Update best model
            self.best_models[player_id] = model
            return True
        return False
    
    def train(self, total_timesteps: int):
        """Main training loop with self-play."""
        timesteps = 0
        version = 0
        
        while timesteps < total_timesteps:
            # Training phase
            for player_id in range(self.num_players):
                self.current_models[player_id].learn(
                    total_timesteps=self.eval_freq,
                    reset_num_timesteps=False
                )
                timesteps += self.eval_freq
                
                # Evaluation phase
                win_rate, avg_reward = self.evaluate_model(
                    player_id,
                    self.current_models[player_id]
                )
                
                # Update metrics
                self.win_rates.append(win_rate)
                self.rewards_history.append(avg_reward)
                
                # Update best model if performance is good enough
                if self.update_best_model(player_id, self.current_models[player_id], win_rate):
                    version += 1
                    # Save new best model
                    if timesteps % self.save_freq == 0:
                        self.save_model_version(player_id, self.best_models[player_id], version)
                
                print(f"Player {player_id} - Win Rate: {win_rate:.2f}, Avg Reward: {avg_reward:.2f}")
    
    def get_best_model(self, player_id: int) -> PPO:
        """Get the best model for a player."""
        return self.best_models[player_id]