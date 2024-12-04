import random

def generate_frozen_lake_map(size=4, start=(0, 0), goal=(3, 3), num_holes=3):
    # Create a grid filled with 'F' (free spaces)
    grid = [['F' for _ in range(size)] for _ in range(size)]
    
    # Place the start and goal locations
    grid[start[0]][start[1]] = 'S'  # Start
    grid[goal[0]][goal[1]] = 'G'    # Goal
    
    # Place holes randomly, ensuring they do not occupy the start or goal
    holes = set()
    while len(holes) < num_holes:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if (x, y) != start and (x, y) != goal and (x, y) not in holes:
            holes.add((x, y))
    
    for hole in holes:
        grid[hole[0]][hole[1]] = 'H'
    
    # Ensure there's at least one path from start to goal
    if not find_path(grid, start, goal):
        return generate_frozen_lake_map(size, start, goal, num_holes)
    
    return grid, holes

def find_path(grid, start, goal):
    size = len(grid)
    visited = set()
    stack = [start]
    
    while stack:
        current = stack.pop()
        if current == goal:
            return True
        if current in visited:
            continue
        
        visited.add(current)
        x, y = current
        
        # Check all possible movements (right, down, left, up)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < size and 0 <= new_y < size:
                if grid[new_x][new_y] != 'H' and (new_x, new_y) not in visited:
                    stack.append((new_x, new_y))
    
    return False

def create_pddl(grid, holes, start, goal):
    size = len(grid)
    pddl_content = "(define (problem frozen-lake-4x4)\n"
    pddl_content += "  (:domain frozen-lake)\n\n"
    
    pddl_content += "  (:objects\n"
    for i in range(size):
        for j in range(size):
            pddl_content += f"    loc-{i}-{j} "
    pddl_content += "- location\n  )\n\n"
    
    pddl_content += "  (:init\n"
    pddl_content += f"    (at loc-{start[0]}-{start[1]})\n"
    pddl_content += f"    (is-goal loc-{goal[0]}-{goal[1]})\n" 
    
    for hole in holes:
        pddl_content += f"    (is-hole loc-{hole[0]}-{hole[1]})\n"

    # Define safe locations
    for i in range(size):
        for j in range(size):
            if grid[i][j] != 'H':
                pddl_content += f"    (is-safe loc-{i}-{j})\n" 
    
    # Define directional relationships
    for i in range(size):
        for j in range(size):
            if i < size - 1:  # Down
                pddl_content += f"    (down loc-{i}-{j} loc-{i+1}-{j})\n"
                pddl_content += f"    (up loc-{i+1}-{j} loc-{i}-{j})\n"
            if j < size - 1:  # Right
                pddl_content += f"    (right loc-{i}-{j} loc-{i}-{j+1})\n"
                pddl_content += f"    (left loc-{i}-{j+1} loc-{i}-{j})\n"
    
    pddl_content += "  )\n\n"
    pddl_content += f"  (:goal (at loc-{goal[0]}-{goal[1]}))\n"
    pddl_content += ")"
    
    return pddl_content

def save_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

# Configuration 
size = 8
start = (0, 0) 
goal = (7, 7)
num_holes = 10 

# Generate the map and PDDL
grid, holes = generate_frozen_lake_map(size, start, goal, num_holes)

desc = [''.join(row) for row in grid]
print("desc =", desc)

pddl_content = create_pddl(grid, holes, start, goal)
save_to_file(pddl_content, "frozen-lake-gen.pddl")
print("\nPDDL File has been saved as 'frozen-lake-gen.pddl'.")
