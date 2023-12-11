from typing import List, Tuple


def parse_grid(lines: List[str]) -> List[List[str]]:
    # Parse grid as list of lists
    return [list(line) for line in lines]


def find_galaxies(grid: List[List[str]]) -> List[Tuple[int, int]]:
    # Find all galaxy positions (#) in the grid
    galaxies = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '#':
                galaxies.append((row, col))
    
    return galaxies


def find_empty_rows(grid: List[List[str]]) -> set:
    # Find rows with no galaxies
    empty_rows = set()
    for row in range(len(grid)):
        if all(cell == '.' for cell in grid[row]):
            empty_rows.add(row)
    
    return empty_rows


def find_empty_cols(grid: List[List[str]]) -> set:
    # Find columns with no galaxies
    empty_cols = set()
    for col in range(len(grid[0])):
        if all(grid[row][col] == '.' for row in range(len(grid))):
            empty_cols.add(col)
    
    return empty_cols


def sum_of_shortest_paths(galaxies: List[Tuple[int, int]], empty_rows: set, empty_cols: set, expansion_factor: int) -> int:
    # Calculate sum of shortest paths between all pairs
    total = 0
    
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            r1, c1 = galaxies[i]
            r2, c2 = galaxies[j]
            
            # Manhattan distance
            distance = abs(r2 - r1) + abs(c2 - c1)
            
            # Add expansion for empty rows between the galaxies
            min_row, max_row = min(r1, r2), max(r1, r2)
            for row in range(min_row + 1, max_row):
                if row in empty_rows:
                    distance += expansion_factor
            
            # Add expansion for empty columns between the galaxies
            min_col, max_col = min(c1, c2), max(c1, c2)
            for col in range(min_col + 1, max_col):
                if col in empty_cols:
                    distance += expansion_factor
            
            total += distance
    
    return total


def solve_part_1(lines: List[str]) -> int:
    grid = parse_grid(lines)
    galaxies = find_galaxies(grid)
    empty_rows = find_empty_rows(grid)
    empty_cols = find_empty_cols(grid)
    
    return sum_of_shortest_paths(galaxies, empty_rows, empty_cols, 1)


def solve_part_2(lines: List[str]) -> int:
    grid = parse_grid(lines)
    galaxies = find_galaxies(grid)
    empty_rows = find_empty_rows(grid)
    empty_cols = find_empty_cols(grid)
    
    return sum_of_shortest_paths(galaxies, empty_rows, empty_cols, 999999)


if __name__ == "__main__":
    with open("11/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")