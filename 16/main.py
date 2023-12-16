from typing import List, Set, Tuple


def parse_grid(lines: List[str]) -> List[List[str]]:
    return [list(line) for line in lines]


def simulate_beam(grid: List[List[str]], start_row: int, start_col: int, start_direction: str) -> int:
    # Simulate beam path and count energized tiles using BFS
    visited: Set[Tuple[int, int, str]] = set()
    energized: Set[Tuple[int, int]] = set()
    beams = [(start_row, start_col, start_direction)]
    
    # Direction deltas and mirror reflection mappings
    deltas = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    
    # Forward/backward mirror reflection rules
    mirror_forward = {
        'right': 'up',
        'left': 'down',
        'up': 'right',
        'down': 'left'
    }
    
    mirror_backward = {
        'right': 'down',
        'left': 'up',
        'up': 'left',
        'down': 'right'
    }
    
    while beams:
        row, col, direction = beams.pop(0)
        
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
            continue
        
        state = (row, col, direction)
        if state in visited:
            continue
        
        visited.add(state)
        energized.add((row, col))
        
        tile = grid[row][col]
        
        if tile == '.':
            dr, dc = deltas[direction]
            beams.append((row + dr, col + dc, direction))
        
        elif tile == '/':
            new_direction = mirror_forward[direction]
            dr, dc = deltas[new_direction]
            beams.append((row + dr, col + dc, new_direction))
        
        elif tile == '\\':
            new_direction = mirror_backward[direction]
            dr, dc = deltas[new_direction]
            beams.append((row + dr, col + dc, new_direction))
        
        # Splitters create two beams perpendicular to their orientation
        elif tile == '|':
            if direction in ['up', 'down']:
                dr, dc = deltas[direction]
                beams.append((row + dr, col + dc, direction))
            else:
                beams.append((row - 1, col, 'up'))
                beams.append((row + 1, col, 'down'))
        
        elif tile == '-':
            if direction in ['left', 'right']:
                dr, dc = deltas[direction]
                beams.append((row + dr, col + dc, direction))
            else:
                beams.append((row, col - 1, 'left'))
                beams.append((row, col + 1, 'right'))
    
    return len(energized)


def solve_part_1(lines: List[str]) -> int:
    grid = parse_grid(lines)
    
    return simulate_beam(grid, 0, 0, 'right')


def solve_part_2(lines: List[str]) -> int:
    # Try all edge starting positions to find maximum energized tiles
    grid = parse_grid(lines)
    max_energized = 0
    
    rows = len(grid)
    cols = len(grid[0])
    
    for col in range(cols):
        energized = simulate_beam(grid, 0, col, 'down')
        max_energized = max(max_energized, energized)
    
    for col in range(cols):
        energized = simulate_beam(grid, rows - 1, col, 'up')
        max_energized = max(max_energized, energized)
    
    for row in range(rows):
        energized = simulate_beam(grid, row, 0, 'right')
        max_energized = max(max_energized, energized)
    
    for row in range(rows):
        energized = simulate_beam(grid, row, cols - 1, 'left')
        max_energized = max(max_energized, energized)
    
    return max_energized


if __name__ == "__main__":
    with open("16/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")