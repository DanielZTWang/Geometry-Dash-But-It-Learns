# Training algorithm and game environment
from stable_baselines3 import PPO
from GD_env import GameEnv

# File managing
import os

# Create folders for models and logs
os.makedirs("models", exist_ok = True)
os.makedirs("logs", exist_ok = True)

# Initialize environment and model
env = GameEnv()
model = PPO("MlpPolicy", env, verbose = 1, tensorboard_log = "./logs/")

# Start training
model.learn(total_timesteps = 10000)

# Save trained model and close environment
model.save("models/gd_ppo")
env.close()