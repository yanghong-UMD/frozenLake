import pddlgym
import subprocess
import random
import time
import os
import re

# Create the Frozen Lake environment (PDDL version)
env = pddlgym.make("FrozenLake-v1", desc=['SFFF', 'FFFF', 'FFFH', 'FFFG'], map_name=None, is_slippery=True)

obs, debug_info = env.reset()

# Function to update the PDDL problem file with the new player location without modifying the goal
def update_pddl_with_new_location(original_problem_file, temp_problem_file, player_x, player_y):
    with open(original_problem_file, 'r') as file:
        lines = file.readlines()

    with open(temp_problem_file, 'w') as file:
        in_init_section = False  # To track if we're in the :init section
        for line in lines:
            # Look for the :init section
            if ":init" in line:
                in_init_section = True

            # Look for the :goal section, signaling the end of :init section
            if ":goal" in line:
                in_init_section = False

            # Modify only the player's location in the :init section
            if "at loc-" in line and in_init_section:
                new_loc = f"loc-{player_x}-{player_y}"
                line = re.sub(r'loc-\d-\d', new_loc, line)

            # Write the line to the new temp file
            file.write(line)


# Run-lookahead algorithm
def run_lookahead(domain_file, original_problem_file, solution_file, num_runs=1):
    success_count = 0
    total_steps_for_success = 0
    total_planner_time = 0
    temp_problem_file = "temp-frozen-lake-gen.pddl"  # Keep temp file for debugging
    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}")
        
        obs, debug_info = env.reset()
        
        done = False
        steps = 0
        
        while not done:
            # Get player's current position
            player_x, player_y = divmod(obs, 4)
            
            # Update the PDDL problem file with the new player position
            update_pddl_with_new_location(original_problem_file, temp_problem_file, player_x, player_y)

            # Run pyperplan to generate a new plan from the current position
            plan_output, planner_time = run_pyperplan(domain_file, temp_problem_file, solution_file)
            plan = parse_plan(plan_output)
            total_planner_time += planner_time
            
            # Execute the first action from the plan
            if plan:
                action = plan[0]
                intended_action_str = ["Left", "Down", "Right", "Up"][action]
            else:
                # If no valid plan, fallback to random action
                action = env.action_space.sample()
                intended_action_str = "Random"

            obs_before = obs
            obs, reward, done, truncated, debug_info = env.step(action)
            steps += 1

            # Print current state
            if (num_runs == 1):
                print(f"Step {steps}:")
                print(f"Intended Action: {intended_action_str}")
                print_frozen_lake_state(obs)
                print(f"Observation: {obs}, Reward: {reward}, Done: {done}, Truncated: {truncated}\n")

            if done:
                if reward == 1:
                    success_count += 1
                    total_steps_for_success += steps
                    if (num_runs == 1):
                        print("Congratulations! You've reached the goal!")
                else:
                    if (num_runs == 1):
                        print("Game over! You fell into a hole.")
                
        # Don't delete temp files for debugging
        # if os.path.exists(temp_problem_file):
        #     os.remove(temp_problem_file)

    # Show results after multiple runs
    if num_runs > 1:
        success_rate = (success_count / num_runs) * 100
        avg_steps = total_steps_for_success / success_count if success_count > 0 else 0
        avg_planner_time = total_planner_time / num_runs
        print(f"Success Rate: {success_count}/{num_runs} ({success_rate:.2f}%)")
        if success_count > 0:
            print(f"Average Steps (for successful runs): {avg_steps:.2f}")
        print(f"Average Planner Time: {avg_planner_time:.4f} seconds")


# Function to visualize the current state of the Frozen Lake environment
def print_frozen_lake_state(obs):
    size = 4  # Assuming a 4x4 grid for Frozen Lake
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    
    # Mark player position with 'P'
    player_x, player_y = divmod(obs, size)
    grid[player_x][player_y] = 'P'

    # Mark holes and goal
    for i in range(size):
        for j in range(size):
            if (i, j) == (size - 1, size - 1):
                grid[i][j] = 'G'
            elif env.desc[i, j] == b'H':
                grid[i][j] = '#'

    # Print the grid
    for row in grid:
        print(' '.join(row))
    print("\n")

# Function to run pyperplan and return the solution file content
def run_pyperplan(domain_file, problem_file, solution_file):
    start_time = time.time()  # Start timing the planner
    # Run pyperplan using subprocess
    subprocess.run(
        ["python", "-m", "pyperplan", "-H", "hff", "-s", "gbf", domain_file, problem_file],
        stdout=subprocess.PIPE,
        text=True
    )
    planner_time = time.time() - start_time  # Calculate planner execution time
    # Read the solution file
    with open(solution_file, 'r') as file:
        return file.readlines(), planner_time

# Parse solution file and map actions to FrozenLake action space
def parse_plan(plan_lines):
    action_mapping = {
        "move-up": 3,
        "move-right": 2,
        "move-down": 1,
        "move-left": 0
    }
    actions = []
    for line in plan_lines:
        action = line.split()[0].strip('()')
        if action in action_mapping:
            actions.append(action_mapping[action])
    return actions

# Example usage of Pyperplan
domain_file = "frozen-lake-domain.pddl"
problem_file = "frozen-lake-gen.pddl"
solution_file = "temp-frozen-lake-gen.pddl.soln"

num_runs = 100  # Number of simulation runs

run_lookahead(domain_file, problem_file, solution_file, num_runs)

