from typing import List, Tuple


# Directions: (row_delta, col_delta)
DIRECTIONS = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}


# Which pipes connect in which directions
PIPE_CONNECTIONS = {
    '|': ['N', 'S'],
    '-': ['E', 'W'],
    'L': ['N', 'E'],
    'J': ['N', 'W'],
    '7': ['S', 'W'],
    'F': ['S', 'E'],
    '.': [],
}


# Opposite direction mapping
OPPOSITE = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}


def parse_grid(lines: List[str]) -> List[List[str]]:
    # Convert each line to list of characters
    return [list(line) for line in lines]


def find_start(grid: List[List[str]]) -> Tuple[int, int]:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                return (row, col)

    raise ValueError("Start position S not found")


def get_pipe_at(grid: List[List[str]], row: int, col: int) -> str:
    # Return pipe character or '.' if out of bounds
    if 0 <= row < len(grid) and 0 <= col < len(grid[row]):
        return grid[row][col]

    return '.'


def can_connect(pipe: str, direction: str) -> bool:
    # Check if pipe can connect in given direction
    return direction in PIPE_CONNECTIONS.get(pipe, [])


def find_loop_length(grid: List[List[str]], start: Tuple[int, int]) -> int:
    # Find starting direction by checking which adjacent pipe connects back
    start_row, start_col = start

    for direction in ['N', 'S', 'E', 'W']:
        dr, dc = DIRECTIONS[direction]
        next_row = start_row + dr
        next_col = start_col + dc
        next_pipe = get_pipe_at(grid, next_row, next_col)

        # Check if this pipe connects back to start
        if can_connect(next_pipe, OPPOSITE[direction]):
            # Found valid starting direction, now follow the loop
            row, col = next_row, next_col
            current_dir = direction
            steps = 1

            while (row, col) != start:
                pipe = grid[row][col]
                directions = PIPE_CONNECTIONS[pipe]
                # Find next direction (the one that's not opposite to current)
                for d in directions:
                    if d != OPPOSITE[current_dir]:
                        current_dir = d
                        break

                dr, dc = DIRECTIONS[current_dir]
                row += dr
                col += dc
                steps += 1

            return steps

    raise ValueError("Loop not found")


def get_loop_tiles(grid: List[List[str]], start: Tuple[int, int]) -> set:
    # Return set of all tiles that are part of the loop
    start_row, start_col = start
    loop_tiles = {(start_row, start_col)}

    for direction in ['N', 'S', 'E', 'W']:
        dr, dc = DIRECTIONS[direction]
        next_row = start_row + dr
        next_col = start_col + dc
        next_pipe = get_pipe_at(grid, next_row, next_col)

        if can_connect(next_pipe, OPPOSITE[direction]):
            # Found valid starting direction, now follow the loop
            row, col = next_row, next_col
            current_dir = direction

            while (row, col) != start:
                loop_tiles.add((row, col))
                pipe = grid[row][col]
                directions = PIPE_CONNECTIONS[pipe]

                for d in directions:
                    if d != OPPOSITE[current_dir]:
                        current_dir = d
                        break

                dr, dc = DIRECTIONS[current_dir]
                row += dr
                col += dc

            return loop_tiles

    raise ValueError("Loop not found")


def solve_part_1(lines: List[str]) -> int:
    grid = parse_grid(lines)
    start = find_start(grid)
    loop_length = find_loop_length(grid, start)
    
    return loop_length // 2


def determine_s_type(grid: List[List[str]], start: Tuple[int, int]) -> str:
    # Determine what type of pipe S actually is based on its connections
    start_row, start_col = start
    connections = []

    # For each direction, check if there's a connecting pipe
    for direction in ['N', 'S', 'E', 'W']:
        dr, dc = DIRECTIONS[direction]
        next_row = start_row + dr
        next_col = start_col + dc
        next_pipe = get_pipe_at(grid, next_row, next_col)

        if can_connect(next_pipe, OPPOSITE[direction]):
            connections.append(direction)

    # Find the pipe type that matches these connections
    for pipe_type, dirs in PIPE_CONNECTIONS.items():
        if pipe_type != '.' and set(connections) == set(dirs):
            return pipe_type

    raise ValueError(f"Cannot determine S type, connections: {connections}")


def count_enclosed_tiles(grid: List[List[str]], loop_tiles: set, start: Tuple[int, int]) -> int:
    # Use scanline approach with even-odd rule to count tiles enclosed by the loop
    enclosed_count = 0

    # Determine what S actually is
    s_type = determine_s_type(grid, start)

    for row in range(len(grid)):
        inside = False

        for col in range(len(grid[row])):
            if (row, col) in loop_tiles:
                pipe = grid[row][col]
                # Replace S with its actual type
                if pipe == 'S':
                    pipe = s_type
                # Count upward connections (north): |, L, J
                if pipe in ['|', 'L', 'J']:
                    inside = not inside
            else:
                # Not part of loop
                if inside:
                    enclosed_count += 1

    return enclosed_count


def solve_part_2(lines: List[str]) -> int:
    grid = parse_grid(lines)
    start = find_start(grid)
    loop_tiles = get_loop_tiles(grid, start)
    
    return count_enclosed_tiles(grid, loop_tiles, start)


if __name__ == "__main__":
    with open("10/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")