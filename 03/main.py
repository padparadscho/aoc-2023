from typing import List, Tuple


def find_numbers(grid: List[str]) -> List[Tuple[int, int, int, int]]:
    # Find all numbers in grid, return list of (value, row, start_col, end_col)
    numbers = []
    for row in range(len(grid)):
        col = 0
        while col < len(grid[row]):
            if grid[row][col].isdigit():
                start_col = col
                num_str = ""
                while col < len(grid[row]) and grid[row][col].isdigit():
                    num_str += grid[row][col]
                    col += 1
                number = int(num_str)
                numbers.append((number, row, start_col, col - 1))
            else:
                col += 1
    
    return numbers


def is_symbol(char: str) -> bool:
    # Check if character is a symbol (not digit or period)
    return not char.isdigit() and char != '.'


def has_adjacent_symbol(grid: List[str], row: int, start_col: int, end_col: int) -> bool:
    # Check if number has any adjacent symbol (including diagonally)
    for r in range(max(0, row - 1), min(len(grid), row + 2)):
        for c in range(max(0, start_col - 1), min(len(grid[r]), end_col + 2)):
            if r != row or c < start_col or c > end_col:
                if is_symbol(grid[r][c]):
                    return True
    
    return False


def solve_part_1(lines: list[str]) -> int:
    grid = lines
    numbers = find_numbers(grid)
    total = 0
    for value, row, start_col, end_col in numbers:
        if has_adjacent_symbol(grid, row, start_col, end_col):
            total += value
    
    return total


def find_gears(grid: List[str]) -> List[Tuple[int, int]]:
    # Find all gear positions (* symbols) in grid
    gears = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '*':
                gears.append((row, col))
    
    return gears


def get_adjacent_numbers(gear_row: int, gear_col: int, 
                         numbers: List[Tuple[int, int, int, int]]) -> List[int]:
    # Get all numbers adjacent to a gear position
    adjacent = []
    for value, row, start_col, end_col in numbers:
        if (row - 1 <= gear_row <= row + 1 and 
            start_col - 1 <= gear_col <= end_col + 1):
            adjacent.append(value)

    return adjacent


def solve_part_2(lines: list[str]) -> int:
    grid = lines
    numbers = find_numbers(grid)
    gears = find_gears(grid)
    total = 0
    for gear_row, gear_col in gears:
        adjacent = get_adjacent_numbers(gear_row, gear_col, numbers)
        if len(adjacent) == 2:
            total += adjacent[0] * adjacent[1]
    
    return total


if __name__ == "__main__":
    with open("03/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")