from pbased_Trainer import LudoTrainer

def main():
    # Initialize trainer
    trainer = LudoTrainer(num_players=2, nb_chevaux=2)
    
    # Training parameters
    NUM_EPISODES = 10000
    EVALUATE_EVERY = 100
    SAVE_PATH = "trained_models"
    
    try:
        # Train models
        trainer.train(
            num_episodes=NUM_EPISODES,
            evaluate_every=EVALUATE_EVERY
        )
        
        # Save final models
        trainer.save_models(SAVE_PATH)
        
    except KeyboardInterrupt:
        print("\nTraining interrupted. Saving current models...")
        trainer.save_models(SAVE_PATH)

if __name__ == "__main__":
    main()