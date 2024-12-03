from stable_baselines3 import PPO
from typing import Dict, List
import numpy as np
import gymnasium as gym

class MultiPolicyWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env, num_players: int = 2):
        """
        Wrapper that maintains separate policies for each player position.
        
        Args:
            env: The Ludo environment
            num_players: Number of players in the game
        """
        super().__init__(env)
        self.num_players = num_players
        self.policies: Dict[int, PPO] = {}
        
        # Initialize a separate policy for each player position
        for player_id in range(num_players):
            self.policies[player_id] = PPO(
                "MultiInputPolicy",
                env,
                verbose=1,
                tensorboard_log=f"./tensorboard_logs/player_{player_id}/"
            )
        
        self.current_policy = self.policies[0]
        
    def reset(self, **kwargs):
        """Reset environment and update current policy."""
        observation, info = self.env.reset(**kwargs)
        player_id = observation["player_id"]
        self.current_policy = self.policies[player_id]
        return observation, info
    
    def step(self, action):
        """
        Take a step in the environment and switch to the appropriate policy.
        Returns modified rewards based on the current player.
        """
        observation, reward, done, truncated, info = self.env.step(action)
        
        # If game isn't over, update the current policy
        if not done:
            player_id = observation["player_id"]
            self.current_policy = self.policies[player_id]
            
        return observation, reward, done, truncated, info
    
    def learn(self, total_timesteps: int):
        """
        Train all policies through self-play.
        
        Args:
            total_timesteps: Total number of environment steps to train for
        """
        timesteps_per_policy = total_timesteps // self.num_players
        
        for episode in range(timesteps_per_policy):
            obs, _ = self.reset()
            done = False
            
            while not done:
                # Get current player
                player_id = obs["player_id"]
                current_policy = self.policies[player_id]
                
                # Get action from current player's policy
                action, _states = current_policy.predict(obs, deterministic=False)
                
                # Take step in environment
                next_obs, reward, done, truncated, info = self.step(action)
                
                # Store transition in current policy's buffer
                current_policy.rollout_buffer.add(
                    obs,
                    action,
                    reward,
                    done,
                    value=current_policy.policy.value(obs),
                    log_prob=current_policy.policy.evaluate_actions(obs, action)[1]
                )
                
                obs = next_obs
                
            # Update all policies after each episode
            for policy in self.policies.values():
                policy.train()
    
    def get_policy(self, player_id: int) -> PPO:
        """Get the policy for a specific player."""
        return self.policies[player_id]
    
    def save_policies(self, path: str):
        """Save all policies to disk."""
        for player_id, policy in self.policies.items():
            policy.save(f"{path}_player_{player_id}")
    
    def load_policies(self, path: str):
        """Load all policies from disk."""
        for player_id in range(self.num_players):
            self.policies[player_id] = PPO.load(f"{path}_player_{player_id}")