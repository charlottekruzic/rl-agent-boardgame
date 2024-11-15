import time
import numpy as np
from gym_env_v2 import LabyrinthEnv
import pythoncom
import pygame

# Create the environment
env = LabyrinthEnv(render_mode="human")
obs = env.reset()

pygame.init()

num_tours = 1000
tour = 0

while tour < num_tours:
    pythoncom.PumpWaitingMessages()

    # Handle window closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.close()
            pygame.quit()
            exit()

    # Sample random action based on current phase
    if env._current_phase == 1:
        # Phase 1: Tile insertion and rotation
        rotation = np.random.randint(0, 4)  # 0-3 for N,E,S,W
        insertion = np.random.randint(0, 3)  # 0-2 for positions 1,3,5
        movement = env.action_space[1].sample()  # Sample movement for next phase
        action = (np.array([rotation, insertion]), movement)
    else:  # Phase 2
        # Phase 2: Movement
        # Keep the same insertion action but generate new movement
        movement = env.action_space[1].sample()
        action = (last_insertion_action, movement)

    # Store the insertion action for next phase
    if env._current_phase == 1:
        last_insertion_action = action[0]

    observation, reward, terminated, truncated, info = env.step(action)

    # Print game state information
    print(f"\n\nTour : {tour}")
    print(f"Joueur : {info['current_player']}")
    print(f"Trésors restants : {info['treasures_remaining']}")
    print(f"Phase : {'Insertion' if env._current_phase == 1 else 'Déplacement'}")
    
    if env._current_phase == 1:
        direction_map = {0: "N", 1: "E", 2: "S", 3: "O"}
        positions = [1, 3, 5]
        print(f"Action Insertion - Direction: {direction_map[action[0][0]]}, Position: {positions[action[0][1]]}")
    else:
        target_pos = (action[1] // 7, action[1] % 7)
        print(f"Action Mouvement - Position cible: {target_pos}")
    
    print(f"Récompense : {reward}")
    print(f"Position joueur : {env.game.get_coord_player()}")
    print(f"Terminé : {terminated}")
    print(f"Tronqué : {truncated}")

    # Render the game state
    env.render()
    # time.sleep(0.5)

    # Only increment tour counter when we complete both phases
    if env._current_phase == 1:
        tour += 1

    if terminated:
        print("Game over!")
        print(f"Partie terminée au tour {tour}")
        break

env.close()
pygame.quit()