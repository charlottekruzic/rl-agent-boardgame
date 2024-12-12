from stable_baselines3 import PPO
import numpy as np
import torch
from typing import Dict, List

class PlayerSpecificPPO(PPO):
    def __init__(self, policy, env, player_id: int, **kwargs):
        super().__init__(policy=policy, env=env, **kwargs)
        self.player_id = player_id

    def preprocess_obs(self, obs: Dict) -> Dict[str, torch.Tensor]:
        """Convert observation dict to tensor format"""
        preprocessed = {}
        
        # Handle each observation type
        preprocessed['my_ecurie'] = torch.tensor([[float(obs['my_ecurie'])]], dtype=torch.float32)
        preprocessed['my_chemin'] = torch.tensor([obs['my_chemin']], dtype=torch.float32)
        preprocessed['my_escalier'] = torch.tensor([obs['my_escalier']], dtype=torch.float32)
        preprocessed['my_goal'] = torch.tensor([[float(obs['my_goal'])]], dtype=torch.float32)
        preprocessed['dice_roll'] = torch.tensor([[float(obs['dice_roll'])]], dtype=torch.float32)
        
        return preprocessed
    
    def debug_observation(self, obs: Dict):
        """Print detailed information about observation structure"""
        print("\nObservation structure:")
        for key, value in obs.items():
            print(f"{key}:")
            print(f"  Type: {type(value)}")
            print(f"  Shape/Length: {np.array(value).shape if isinstance(value, (list, np.ndarray)) else len(str(value))}")
            print(f"  Value: {value}")
            print()

    def collect_experience(self, obs, action, reward, next_obs, done) -> Dict:
        if isinstance(action, np.ndarray):
            action = action.item()
        elif isinstance(action, torch.Tensor):
            action = action.item()

        return {
            'state': obs,
            'action': action,
            'reward': reward,
            'next_state': next_obs,
            'done': done
        }

    def train_on_experiences(self, experiences: List[Dict]):
        if not experiences:
            return

        for exp in experiences:
            try:
                # Preprocess the observation
                processed_obs = self.preprocess_obs(exp['state'])

                # Convert to numpy arrays
                obs_np = {k: v.detach().cpu().numpy() for k, v in processed_obs.items()}
                
                # Get value and log prob
                with torch.no_grad():
                    value = self.policy.predict_values(processed_obs).detach().numpy().flatten()
                    action_tensor = torch.tensor([[exp['action']]], dtype=torch.long)
                    log_prob = self.policy.get_distribution(processed_obs).log_prob(action_tensor).detach().numpy().flatten()

                reward = float(exp['reward'])
                done = bool(exp['done'])

                # Add to buffer
                self.rollout_buffer.add(
                    obs=obs_np,
                    action=np.array([exp['action']]),
                    reward=float(reward),  # Convert to float
                    episode_start=bool(done),  # Convert to boolean
                    value=float(value[0]),  # Take first element as float
                    log_prob=float(log_prob[0])  # Take first element as float
                )
            except Exception as e:
                print(f"Error processing experience in player {self.player_id}:")
                print(f"Error: {str(e)}")
                print(f"Value: {value if 'value' in locals() else 'not computed'}")
                print(f"Log prob: {log_prob if 'log_prob' in locals() else 'not computed'}")
                print(f"Reward: {exp['reward']}")
                print(f"Done: {exp['done']}")
                continue

        try:
            self.train()
        except Exception as e:
            print(f"Error in training for player {self.player_id}: {str(e)}")