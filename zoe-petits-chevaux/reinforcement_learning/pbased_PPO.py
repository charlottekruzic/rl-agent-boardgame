from stable_baselines3 import PPO
import numpy as np
import torch
from typing import Dict, List

class PlayerSpecificPPO(PPO):
    def __init__(self, policy, env, player_id: int, **kwargs):
        super().__init__(policy=policy, env=env, **kwargs)
        self.player_id = player_id

    def collect_experience(self, obs, action, reward, next_obs, done) -> Dict:
        if isinstance(action, np.ndarray) or isinstance(action, torch.Tensor):
            action = int(action.item())

        return {
            'state': obs,
            'action': action,
            'reward': reward,
            'next_state': next_obs,
            'done': done
        }

    def _format_observation(self, obs: Dict) -> Dict[str, np.ndarray]:
        # Ensure obs are (1, obs_dim) if they are vectors
        formatted_obs = {}
        for k, v in obs.items():
            if v is None:
                raise ValueError(f"Observation key '{k}' is None.")

            # Convert to np.float32
            v_array = np.array(v, dtype=np.float32)

            # If scalar, make it (1,)
            if v_array.ndim == 0:
                v_array = v_array.reshape(1,)

            # If it's 1D (like (obs_dim,)), add a batch dim to make (1, obs_dim)
            if v_array.ndim == 1:
                v_array = v_array[np.newaxis, :]

            # Do not add more than one batch dimension.
            # After this, v_array should be (1, obs_dim) or (1, 1), etc.
            formatted_obs[k] = v_array
        return formatted_obs

    def train_on_experiences(self, experiences: List[Dict]):
        if not experiences:
            return

        for exp in experiences:
            try:
                obs_np = self._format_observation(exp['state'])
                # action, reward, done should be (1,) arrays
                action = np.array([exp['action']], dtype=np.int64)
                reward = np.array([float(exp['reward'])], dtype=np.float32)
                episode_start = np.array([bool(exp['done'])], dtype=bool)

                print(f"\n[DEBUG] Player {self.player_id} adding to buffer:")
                for k, arr in obs_np.items():
                    print(f"  Key: {k}, Type: {arr.dtype}, Shape: {arr.shape}, Value: {arr}")
                print(f"  Action: {action}, Reward: {reward}, Done: {episode_start}")

                # Convert obs to torch tensors for evaluation
                # Now we already have (1, obs_dim), so just convert directly
                obs_tensor = {k: torch.as_tensor(val, device=self.device) for k, val in obs_np.items()}

                with torch.no_grad():
                    distribution = self.policy.get_distribution(obs_tensor)
                    value = self.policy.predict_values(obs_tensor)
                    action_tensor = torch.tensor(action, dtype=torch.long, device=self.device)
                    log_prob = distribution.log_prob(action_tensor)

                    value = value.cpu().numpy().flatten()
                    log_prob = log_prob.cpu().numpy().flatten()

                value_arr = np.array([value[0]], dtype=np.float32)
                log_prob_arr = np.array([log_prob[0]], dtype=np.float32)

                # Add directly to the buffer
                self.rollout_buffer.add(
                    obs=obs_np,
                    action=action,
                    reward=reward,
                    episode_start=episode_start,
                    value=value_arr,
                    log_prob=log_prob_arr
                )

            except Exception as e:
                print(f"Error processing experience in player {self.player_id}: {e}")
                print("Experience:", exp)
                continue

        if self.rollout_buffer.full:
            try:
                self.train()
                self.rollout_buffer.reset()
            except Exception as e:
                print(f"Error in training for player {self.player_id}: {str(e)}")
