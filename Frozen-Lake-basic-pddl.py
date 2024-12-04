import pddlgym
import subprocess
import random
import time

env = pddlgym.make("FrozenLake-v1", desc = ['SFFFFFFF', 'FHFFFFFF', 'FFFFHHFF', 'FHFFHFFF', 'HFHFFFFF', 'FFFFFFHF', 'FFFFFFFF', 'HFFFFHFG']
, map_name=None, is_slippery=True)

obs, debug_info = env.reset()

def print_frozen_lake_state(obs, size):
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
    # Run pyperplan using subprocess
    subprocess.run(
        ["python", "pyperplan-main/pyperplan", "-H", "hff", "-s", "gbf", domain_file, problem_file],
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
def calculate_shortest_path_action(player_x, player_y, goal_x, goal_y):
    if player_x < goal_x:
        return 1  #down
    elif player_x > goal_x:
        return 3  #up
    elif player_y < goal_y:
        return 2  #right
    elif player_y > goal_y:
        return 0  #left
    return None
def run_frozen_lake_simulation(domain_file, problem_file, solution_file, num_runs=1, planner=1, size = 4):
    success_count = 0  
    total_steps_for_success = 0  
    total_planner_time = 0  
    goal_x, goal_y = size - 1, size - 1 

    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}")
        
        obs, debug_info = env.reset()
        if planner == 1:
            plan_output, planner_time = run_pyperplan(domain_file, problem_file, solution_file)
            plan = parse_plan(plan_output)
            total_planner_time += planner_time
        
        if num_runs == 1:
            print("Initial State:")
            print_frozen_lake_state(obs,size)

        done = False
        plan_index = 0
        steps = 0

        while not done:
            player_x, player_y = divmod(obs, size)
            
            if planner == 1:
                if plan_index < len(plan):
                    action = plan[plan_index]
                    plan_index += 1
                    intended_action_str = ["Left", "Down", "Right", "Up"][action]
                else:
                    action = calculate_shortest_path_action(player_x, player_y, goal_x, goal_y)
                    intended_action_str = "Shortest Path"
            elif planner == 11:
                action = calculate_shortest_path_action(player_x, player_y, goal_x, goal_y)
                intended_action_str = "Shortest Path"
            else:
                action = env.action_space.sample()
                intended_action_str = "Random"

            obs_before = obs
            obs, reward, done, truncated, debug_info = env.step(action)
            steps += 1

            if num_runs == 1:
                print(f"Step {steps}:")
                print(f"Intended Action: {intended_action_str}")
                print_frozen_lake_state(obs,size)
                print(f"Observation: {obs}, Reward: {reward}, Done: {done}, Truncated: {truncated}\n")

        if reward == 1:
            success_count += 1
            total_steps_for_success += steps
            if num_runs == 1:
                print("Congratulations! You've reached the goal!")
        else:
            if num_runs == 1:
                print("Game over! You fell into a hole.")

    if num_runs > 1:
        success_rate = (success_count / num_runs) * 100
        avg_steps = total_steps_for_success / success_count if success_count > 0 else 0
        avg_planner_time = total_planner_time / num_runs if planner == 1 else 0
        print(f"Success Rate: {success_count}/{num_runs} ({success_rate:.2f}%)")
        if success_count > 0:
            print(f"Average Steps (for successful runs): {avg_steps:.2f}")
        if planner == 1:
            print(f"Average Planner Time: {avg_planner_time:.4f} seconds")

domain_file = "frozen-lake-domain.pddl"
problem_file = "frozen-lake-gen.pddl"
solution_file = "frozen-lake-gen.pddl.soln"

planner = 11 # 11 for moveTo algorithm, 1 for PDDL, 0 for random sampling
num_runs = 10000  # Number of simulation runs
size = 8

run_frozen_lake_simulation(domain_file, problem_file, solution_file, num_runs, planner, size)
