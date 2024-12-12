from typing import Dict, List
import numpy as np
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from pbased_PPO import PlayerSpecificPPO
from ludo_env import LudoEnv
from tqdm import tqdm
import time

class LudoTrainer:
    def __init__(self, num_players: int = 2, nb_chevaux: int = 2):
        self.env = LudoEnv(
            num_players=num_players, 
            nb_chevaux=nb_chevaux, 
            mode_gym="entrainement",
            mode_fin_partie="tous"
        )
        
        self.models = {}
        for i in range(num_players):
            # Create environment copy for each player
            player_env = LudoEnv(
                num_players=num_players,
                nb_chevaux=nb_chevaux,
                mode_gym="entrainement"
            )
            
            self.models[i] = PlayerSpecificPPO(
                policy="MultiInputPolicy",
                env=player_env,  # Use player-specific environment
                player_id=i,
                verbose=1,
                n_steps=2048,
                batch_size=64,
                n_epochs=10,
                learning_rate=3e-4
            )

        # Training statistics
        self.stats = {
            'episodes_completed': 0,
            'total_rewards': {i: [] for i in range(num_players)},
            'wins': {i: 0 for i in range(num_players)},
            'training_time': 0
        }
        
    def train_episode(self) -> Dict[int, List[Dict]]:
        obs, _ = self.env.reset()
        done = False
        experiences = {i: [] for i in range(self.env.num_players)}
        episode_rewards = {i: 0 for i in range(self.env.num_players)}
        
        while not done:
            current_player = self.env.current_player
            # Get action from current player's model
            action, _ = self.models[current_player].predict(obs)
            
            # Execute action
            next_obs, reward, done, truncated, info = self.env.step(action)
            
            # Store experience
            experience = self.models[current_player].collect_experience(
                obs=obs,
                action=action,
                reward=reward,
                next_obs=next_obs,
                done=done
            )
            experiences[current_player].append(experience)
            episode_rewards[current_player] += reward 
            obs = next_obs

        # Update statistics
        for player_id, reward in episode_rewards.items():
            self.stats['total_rewards'][player_id].append(reward)
        
        winner = self.env.game.is_winner()
        if winner != -1:
            self.stats['wins'][winner] += 1
            
        return experiences

    def train(self, num_episodes: int = 1000, evaluate_every: int = 100):

        start_time = time.time()
        
        # Progress bar for episodes
        pbar = tqdm(total=num_episodes, desc="Training Progress")


        for episode in range(num_episodes):
            # Reset rollout buffers
            for model in self.models.values():
                model.rollout_buffer.reset()

            # Collect experiences
            experiences = self.train_episode()
            
            # Train each player's model
            for player_id, player_experiences in experiences.items():
                if len(player_experiences) > 0:
                    try:
                        self.models[player_id].train_on_experiences(player_experiences)
                    except Exception as e:
                        print(f"Error training player {player_id}: {str(e)}")
                        continue

            # Update statistics
            self.stats['episodes_completed'] += 1
            
            # Evaluate
            if episode % evaluate_every == 0:
                results = self.evaluate_models()
                self._log_evaluation(episode, results)

            pbar.update(1)

        pbar.close()
        self.stats['training_time'] = time.time() - start_time
        self._log_final_stats()
    
    def evaluate_models(self, num_games: int = 100) -> Dict[int, int]:
        """Evaluate current models by playing games"""
        wins = {i: 0 for i in range(self.env.num_players)}
        
        for _ in range(num_games):
            obs, _ = self.env.reset()
            done = False
            
            while not done:
                current_player = self.env.current_player
                action, _ = self.models[current_player].predict(obs, deterministic=True)
                obs, _, done, _, _ = self.env.step(action)
            
            winner = self.env.game.is_winner()
            wins[winner] += 1
        
        return wins
    
    def _log_evaluation(self, episode: int, results: Dict[int, int]):
        """Log evaluation results"""
        print(f"\nEpisode {episode} evaluation results:")
        for player_id, wins in results.items():
            print(f"Player {player_id} wins: {wins}")

    def _log_final_stats(self):
        """Log final training statistics"""
        print("\nTraining Complete!")
        print(f"Total Episodes: {self.stats['episodes_completed']}")
        print(f"Training Time: {self.stats['training_time']:.2f} seconds")
        print("\nFinal Statistics:")
        for player_id in range(self.env.num_players):
            print(f"\nPlayer {player_id}:")
            print(f"  Total Wins: {self.stats['wins'][player_id]}")
            print(f"  Win Rate: {self.stats['wins'][player_id]/self.stats['episodes_completed']:.2%}")
            print(f"  Average Reward: {np.mean(self.stats['total_rewards'][player_id]):.2f}")
            
    def save_models(self, path: str):
        """Save all models"""
        for player_id, model in self.models.items():
            model.save(f"{path}/player_{player_id}_model")
            
    def load_models(self, path: str):
        """Load all models"""
        for player_id in self.models.keys():
            self.models[player_id] = PlayerSpecificPPO.load(
                f"{path}/player_{player_id}_model"
            )