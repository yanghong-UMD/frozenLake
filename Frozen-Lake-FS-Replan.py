import pddlgym
import subprocess
import random
import time
import os
import re

env = pddlgym.make("FrozenLake-v1", desc = ['SFFFFFFF', 'FHFFFFFF', 'FFFFHHFF', 'FHFFHFFF', 'HFHFFFFF', 'FFFFFFHF', 'FFFFFFFF', 'HFFFFHFG']
, map_name=None, is_slippery=True)

obs, debug_info = env.reset()

def update_pddl_with_new_location(original_problem_file, temp_problem_file, player_x, player_y):
    with open(original_problem_file, 'r') as file:
        lines = file.readlines()

    with open(temp_problem_file, 'w') as file:
        in_init_section = False
        for line in lines:
            if ":init" in line:
                in_init_section = True
            if ":goal" in line:
                in_init_section = False
            if "at loc-" in line and in_init_section:
                new_loc = f"loc-{player_x}-{player_y}"
                line = re.sub(r'loc-\d-\d', new_loc, line)
            file.write(line)

def run_ff_replan(domain_file, original_problem_file, solution_file, num_runs=1,size=4):
    success_count = 0
    total_steps_for_success = 0
    total_planner_time = 0
    temp_problem_file = "temp-frozen-lake-gen.pddl"
    plan = None
    plan_index = 0 

    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}")
        
        obs, debug_info = env.reset()
        done = False
        steps = 0
        
        while not done:
            player_x, player_y = divmod(obs, size)
            
            # Always replan from current state (FS-Replan)
            if plan is None or plan_index >= len(plan):
                update_pddl_with_new_location(original_problem_file, temp_problem_file, player_x, player_y)
                plan_output, planner_time = run_pyperplan(domain_file, temp_problem_file, solution_file)
                total_planner_time += planner_time
                plan_index = 0
                plan = parse_plan(plan_output)

            if plan:
                action = plan[plan_index] 
                action_str = ["Left", "Down", "Right", "Up"][action]
            else:
                # Random action if no plan is found
                action = env.action_space.sample()
                action_str = "Random"

            intended_x, intended_y = player_x, player_y  # Starting point
            if action_str == "Up":
                intended_x -= 1
            elif action_str == "Down":
                intended_x += 1
            elif action_str == "Left":
                intended_y -= 1
            elif action_str == "Right":
                intended_y += 1
            obs_before = obs
            obs, reward, done, truncated, debug_info = env.step(action)
            steps += 1

            player_x_new, player_y_new = divmod(obs, 4)
            if player_x_new != intended_x or player_y_new != intended_y:
                plan = None
            else:
                plan_index += 1

            if run == 0:
                print(f"Step {steps}:")
                print(f"Action taken: {action_str}")
                print_frozen_lake_state(obs,size)
                print(f"Observation: {obs}, Reward: {reward}, Done: {done}, Truncated: {truncated}\n")

            if done:
                if reward == 1:
                    success_count += 1
                    total_steps_for_success += steps
                    if run == 0:
                        print("Success! Reached the goal!")
                else:
                    if run == 0:
                        print("Failed! Fell into a hole.")

    if num_runs > 1:
        success_rate = (success_count / num_runs) * 100
        avg_steps = total_steps_for_success / success_count if success_count > 0 else 0
        avg_planner_time = total_planner_time / num_runs
        print(f"\nResults Summary:")
        print(f"Success Rate: {success_count}/{num_runs} ({success_rate:.2f}%)")
        if success_count > 0:
            print(f"Average Steps (for successful runs): {avg_steps:.2f}")
        print(f"Average Planner Time: {avg_planner_time:.4f} seconds")

def print_frozen_lake_state(obs,size):
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    player_x, player_y = divmod(obs, size)
    grid[player_x][player_y] = 'P'
    
    for i in range(size):
        for j in range(size):
            if (i, j) == (size - 1, size - 1):
                grid[i][j] = 'G'
            elif env.desc[i, j] == b'H':
                grid[i][j] = '#'
    
    for row in grid:
        print(' '.join(row))
    print("\n")

def run_pyperplan(domain_file, problem_file, solution_file):
    start_time = time.time()
    subprocess.run(
        ["python", "-m", "pyperplan", "-H", "hff", "-s", "gbf", domain_file, problem_file],
        stdout=subprocess.PIPE,
        text=True
    )

    planner_time = time.time() - start_time
    with open(solution_file, 'r') as file:
        return file.readlines(), planner_time

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

# Example usage
domain_file = "frozen-lake-domain.pddl"
problem_file = "frozen-lake-gen.pddl"
solution_file = "temp-frozen-lake-gen.pddl.soln"

num_runs = 1000
size = 8
run_ff_replan(domain_file, problem_file, solution_file, num_runs,size)