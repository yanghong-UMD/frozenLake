import pddlgym
import random

# Create the Frozen Lake environment
env = pddlgym.make("FrozenLake-v1", desc=None, map_name="4x4", is_slippery=False)

# Function to visualize the current state of the Frozen Lake environment
def print_frozen_lake_state(obs, size=4):
    """Display the frozen lake environment grid."""
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    
    # Mark the player position with 'P'
    player_x, player_y = divmod(obs, size)
    grid[player_x][player_y] = 'P'

    # Mark holes and goal
    for i in range(size):
        for j in range(size):
            # Check for holes (H) and goal (G)
            if (i, j) == (size - 1, size - 1):  # Bottom-right corner is the goal
                grid[i][j] = 'G'
            elif env.desc[i, j] == b'H':  # Mark holes in the environment
                grid[i][j] = '#'
    
    # Print the grid
    for row in grid:
        print(' '.join(row))
    print("\n")

# Run the simulation multiple times
def run_frozen_lake_simulation(num_runs=1):
    """Run the Frozen Lake simulation."""
    success_count = 0  # Track the number of successful runs
    
    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}")

        obs, debug_info = env.reset()
        done = False
        steps = 0  # Track steps taken in each run

        if num_runs == 1:
            print("Initial State:")
            print_frozen_lake_state(obs)

        while not done:
            action = env.action_space.sample()  # Random action (modify as needed)
            obs_before = obs

            # Take a step in the environment
            obs, reward, done, truncated, debug_info = env.step(action)

            steps += 1
            
            # Check if slippery environment caused unintended movement
            intended_action_str = ["Left", "Down", "Right", "Up"][action]
            actual_action = action

            # Show action details
            if num_runs == 1:
                print(f"Step {steps}:")
                print(f"Intended Action: {intended_action_str}")
                print_frozen_lake_state(obs)

                # Show the step result
                print(f"Observation: {obs}, Reward: {reward}, Done: {done}, Truncated: {truncated}\n")

        # Track success
        if reward == 1:
            success_count += 1
            if num_runs == 1:
                print("Congratulations! You've reached the goal!")
        else:
            if num_runs == 1:
                print("Game over! You fell into a hole.")
    
    # Show success rate after multiple runs
    if num_runs > 1:
        print(f"Success Rate: {success_count}/{num_runs} ({(success_count / num_runs) * 100:.2f}%)")

# Example usage
num_runs = 5  # Set to a number > 1 to see success rate across multiple runs
run_frozen_lake_simulation(num_runs)
