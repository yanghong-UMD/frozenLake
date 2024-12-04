import pddlgym
import subprocess
import random
import time
import os
import re

# Create the Frozen Lake environment (PDDL version)
env = pddlgym.make("FrozenLake-v1", desc=None, map_name='4x4', is_slippery=True)

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


def run_lazy_lookahead(domain_file, original_problem_file, solution_file, num_runs=1):
    success_count = 0
    total_steps_for_success = 0
    total_planner_time = 0
    temp_problem_file = "temp-frozen-lake-gen.pddl"  # Keep temp file for debugging
    plan = None  # Store the current plan across steps
    plan_index = 0  # Track the current step in the plan

    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}")
        
        obs, debug_info = env.reset()
        done = False
        steps = 0
        plan = None  # Reset plan at the beginning of each run
        plan_index = 0
        
        while not done:
            # Get player's current position
            player_x, player_y = divmod(obs, 4)
            
            if plan is None or plan_index >= len(plan):  # No plan or exhausted plan, run pyperplan
                # Update the PDDL problem file with the new player position
                update_pddl_with_new_location(original_problem_file, temp_problem_file, player_x, player_y)

                # Run pyperplan to generate a new plan from the current position
                plan_output, planner_time = run_pyperplan(domain_file, temp_problem_file, solution_file)
                plan = parse_plan(plan_output)
                plan_index = 0  # Reset plan index
                total_planner_time += planner_time
            
            if plan:
                # Execute the next action from the plan
                intended_action = plan[plan_index]
                intended_action_str = ["Left", "Down", "Right", "Up"][intended_action]

                # Track the current position before stepping
                obs_before = obs
                
                # Take the intended action
                obs, reward, done, truncated, debug_info = env.step(intended_action)
                steps += 1

                # Check if the agent slipped by comparing the new observation with the intended movement
                player_x_new, player_y_new = divmod(obs, 4)
                intended_x, intended_y = player_x, player_y  # Starting point
                if intended_action_str == "Up":
                    intended_x -= 1
                elif intended_action_str == "Down":
                    intended_x += 1
                elif intended_action_str == "Left":
                    intended_y -= 1
                elif intended_action_str == "Right":
                    intended_y += 1

                # If the agent slipped (i.e., not where we intended to move), re-plan
                if player_x_new != intended_x or player_y_new != intended_y:
                    if num_runs == 1:
                        print(f"Slip detected! Agent did not move to the intended location {intended_x},{intended_y}. Replanning...")
                    plan = None  # Invalidate the plan and force a re-plan
                else:
                    # If the agent moved as intended, proceed to the next step in the plan
                    plan_index += 1
                    if num_runs == 1:
                        print(f"Agent moved as intended to {player_x_new},{player_y_new}. Proceeding with current plan.")
            else:
                # Fallback to random action if no valid plan is available
                action = env.action_space.sample()
                intended_action_str = "Random"
                obs, reward, done, truncated, debug_info = env.step(action)
                steps += 1

            # Print current state (only for single run)
            if run == 0: 
                print(f"Step {steps}:")
                print(f"Intended Action: {intended_action_str}")
                print_frozen_lake_state(obs)
                print(f"Observation: {obs}, Reward: {reward}, Done: {done}, Truncated: {truncated}\n")

            if done:
                if reward == 1:
                    success_count += 1
                    total_steps_for_success += steps
                    if run == 0:
                        print("Congratulations! You've reached the goal!")
                else:
                    if run == 0:
                        print("Game over! You fell into a hole.")
                
    # Results summary after multiple runs
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
        ["python", "pyperplan-main/pyperplan", "-H", "hff", "-s", "gbf", domain_file, problem_file],
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
problem_file = "frozen-lake-4x4.pddl"
solution_file = "temp-frozen-lake-gen.pddl.soln"

num_runs = 100  # Number of simulation runs

run_lazy_lookahead(domain_file, problem_file, solution_file, num_runs)

