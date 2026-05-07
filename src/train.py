# Training algorithm and game environment
from stable_baselines3 import PPO
from GD_env import GameEnv

# File managing
import os

# Input checking
import keyboard

# Create folders for models and logs
os.makedirs("models", exist_ok = True)
os.makedirs("logs", exist_ok = True)

# Allow for manual start
while True:
    if keyboard.is_pressed('z'): # CHANGE 'z' TO ANY KEY YOU WANT AS START
        break

# Initialize environment and model
env = GameEnv()
env.adapt_mode = True
model = PPO(
    "MlpPolicy", 
    env, 
    verbose = 1, 
    tensorboard_log = "./logs/", 
    n_steps = 128, 
    batch_size = 64,
    ent_coef = 0.1
)

# Start training
model.learn(total_timesteps = 5000)

# Save trained model and close environment
model.save("models/gd_ppo")
env.close()