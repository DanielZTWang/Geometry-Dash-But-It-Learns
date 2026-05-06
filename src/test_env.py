# Import the environment to be tested
from GD_env import GameEnv

# Input checking
import keyboard

# Allow for manual start
while True:
    if keyboard.is_pressed('z'): # CHANGE 'z' TO ANY KEY YOU WANT AS START
        break

# Initialize environment
env = GameEnv()

# Reset environment
obs, info = env.reset()
print("Starting obs:", obs)

for i in range(1000):
    # Allow for manual termination
    if keyboard.is_pressed("x"):
        print("finished")
        break
    
    # Take a random action
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    # Print current step information
    print(
        f"step={i}, action={action}, obs={obs}, reward={reward}, "
        f"terminated={terminated}, truncated={truncated}, info={info}"
    )

    # Reset environment if terminated or truncated
    if terminated or truncated:
        print("Resetting...")
        obs, info = env.reset()

env.close()