from typing import List, Tuple
from collections import deque


def parse_grid(lines: List[str]) -> Tuple[List[List[str]], Tuple[int, int]]:
    # Parse grid and find starting position marked 'S'
    grid = [list(line) for line in lines]
    
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'S':
                return grid, (row, col)
    
    raise ValueError("No starting position found")


def solve_part_1(lines: List[str], steps: int = 64) -> int:
    # BFS to find all positions reachable in exactly 64 steps
    grid, start = parse_grid(lines)
    rows, cols = len(grid), len(grid[0])
    
    queue = deque([(start[0], start[1], 0)])
    visited = {(start[0], start[1], 0)}
    
    positions = set()
    
    while queue:
        row, col, step = queue.popleft()
        
        if step == steps:
            positions.add((row, col))
            continue
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row][new_col] != '#':
                    state = (new_row, new_col, step + 1)
                    if state not in visited:
                        visited.add(state)
                        queue.append(state)
    
    return len(positions)


def count_reachable(grid: List[List[str]], start_row: int, start_col: int, steps: int) -> int:
    # BFS on infinite grid (wrapping modulo grid size)
    rows, cols = len(grid), len(grid[0])
    
    queue = deque([(start_row, start_col, 0)])
    visited = {(start_row, start_col, 0)}
    
    positions = set()
    
    while queue:
        row, col, step = queue.popleft()
        
        if step == steps:
            positions.add((row, col))
            continue
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            
            wrapped_row = new_row % rows
            wrapped_col = new_col % cols
            
            if grid[wrapped_row][wrapped_col] != '#':
                state = (new_row, new_col, step + 1)
                if state not in visited:
                    visited.add(state)
                    queue.append(state)
    
    return len(positions)


def solve_part_2(lines: List[str], steps: int = 26501365) -> int:
    # Use quadratic interpolation for infinite grid
    # steps = half + n * grid_size where half = grid_size // 2
    # Calculate f(half), f(half + grid_size), f(half + 2*grid_size)
    # Then use quadratic formula: f(n) = a + n*b + n(n-1)/2*c
    grid, start = parse_grid(lines)
    grid_size = len(grid)
    
    half = grid_size // 2
    
    f0 = count_reachable(grid, start[0], start[1], half)
    f1 = count_reachable(grid, start[0], start[1], half + grid_size)
    f2 = count_reachable(grid, start[0], start[1], half + 2 * grid_size)
    
    n = steps // grid_size
    
    # Quadratic coefficients
    a = f0
    b = f1 - f0
    c = f2 - 2 * f1 + f0
    
    result = a + n * b + n * (n - 1) // 2 * c
    
    return result


if __name__ == "__main__":
    with open("21/input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")