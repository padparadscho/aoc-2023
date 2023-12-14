from typing import List


def parse_grid(lines: List[str]) -> List[List[str]]:
    return [list(line) for line in lines]


def tilt_north(grid: List[List[str]]) -> None:
    # Tilt grid north, move all O's up as far as they can go
    rows = len(grid)
    cols = len(grid[0])
    
    for col in range(cols):
        # For each column, find positions where O's can move up
        write_pos = 0
        for row in range(rows):
            if grid[row][col] == '#':
                write_pos = row + 1
            elif grid[row][col] == 'O':
                if write_pos < row:
                    grid[write_pos][col] = 'O'
                    grid[row][col] = '.'
                write_pos += 1


def tilt_west(grid: List[List[str]]) -> None:
    # Tilt grid west, move all O's left as far as they can go
    rows = len(grid)
    cols = len(grid[0])
    
    for row in range(rows):
        write_pos = 0
        for col in range(cols):
            if grid[row][col] == '#':
                write_pos = col + 1
            elif grid[row][col] == 'O':
                if write_pos < col:
                    grid[row][write_pos] = 'O'
                    grid[row][col] = '.'
                write_pos += 1


def tilt_south(grid: List[List[str]]) -> None:
    # Tilt grid south, move all O's down as far as they can go
    rows = len(grid)
    cols = len(grid[0])
    
    for col in range(cols):
        write_pos = rows - 1
        for row in range(rows - 1, -1, -1):
            if grid[row][col] == '#':
                write_pos = row - 1
            elif grid[row][col] == 'O':
                if write_pos > row:
                    grid[write_pos][col] = 'O'
                    grid[row][col] = '.'
                write_pos -= 1


def tilt_east(grid: List[List[str]]) -> None:
    # Tilt grid east, move all O's right as far as they can go
    rows = len(grid)
    cols = len(grid[0])
    
    for row in range(rows):
        write_pos = cols - 1
        for col in range(cols - 1, -1, -1):
            if grid[row][col] == '#':
                write_pos = col - 1
            elif grid[row][col] == 'O':
                if write_pos > col:
                    grid[row][write_pos] = 'O'
                    grid[row][col] = '.'
                write_pos -= 1


def run_cycle(grid: List[List[str]]) -> None:
    # Run one cycle: tilt north, west, south, east
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)


def calculate_load(grid: List[List[str]]) -> int:
    # Calculate total load on north support beams
    rows = len(grid)
    total = 0
    
    for row in range(rows):
        for col in range(len(grid[row])):
            if grid[row][col] == 'O':
                total += rows - row
    
    return total


def grid_to_string(grid: List[List[str]]) -> str:
    return ''.join(''.join(row) for row in grid)


def solve_part_1(lines: List[str]) -> int:
    grid = parse_grid(lines)
    tilt_north(grid)
    
    return calculate_load(grid)


def solve_part_2(lines: List[str]) -> int:
    grid = parse_grid(lines)
    
    # Track seen states for cycle detection
    seen = {}
    cycle_count = 0
    target = 1000000000
    
    while cycle_count < target:
        state = grid_to_string(grid)
        
        if state in seen:
            # Found a cycle
            cycle_start = seen[state]
            cycle_length = cycle_count - cycle_start
            # How many more cycles need to be run
            remaining = target - cycle_count
            # Skip cycles
            cycle_count += (remaining // cycle_length) * cycle_length
            
            if cycle_count >= target:
                break
        
        seen[state] = cycle_count
        run_cycle(grid)
        cycle_count += 1
    
    return calculate_load(grid)


if __name__ == "__main__":
    with open("14/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")