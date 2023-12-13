from typing import List


def parse_patterns(lines: List[str]) -> List[List[str]]:
    # Parse patterns separated by blank lines
    patterns = []
    current_pattern = []
    
    for line in lines:
        if line:
            current_pattern.append(line)
        else:
            if current_pattern:
                patterns.append(current_pattern)
                current_pattern = []
    
    if current_pattern:
        patterns.append(current_pattern)
    
    return patterns


def is_horizontal_reflection(pattern: List[str], row: int) -> bool:
    # Check if reflection line is between row and row+1
    i, j = row, row + 1
    
    while i >= 0 and j < len(pattern):
        if pattern[i] != pattern[j]:
            return False
        i -= 1
        j += 1
    
    return True


def is_vertical_reflection(pattern: List[str], col: int) -> bool:
    # Check if reflection line is between col and col+1
    i, j = col, col + 1
    
    while i >= 0 and j < len(pattern[0]):
        # Check if column i matches column j
        col_i = [pattern[row][i] for row in range(len(pattern))]
        col_j = [pattern[row][j] for row in range(len(pattern))]
        
        if col_i != col_j:
            return False
        i -= 1
        j += 1
    
    return True


def find_reflection(pattern: List[str]) -> tuple:
    # Find reflection line, return (type, position)
    # Return ('h', row) for horizontal, ('v', col) for vertical
    
    # Check horizontal reflections
    for row in range(len(pattern) - 1):
        if is_horizontal_reflection(pattern, row):
            return ('h', row)
    
    # Check vertical reflections
    for col in range(len(pattern[0]) - 1):
        if is_vertical_reflection(pattern, col):
            return ('v', col)
    
    return (None, None)


def count_differences(s1: str, s2: str) -> int:
    return sum(1 for a, b in zip(s1, s2) if a != b)


def is_horizontal_reflection_with_smudge(pattern: List[str], row: int) -> bool:
    # Check if reflection line is between row and row+1 with exactly one smudge
    i, j = row, row + 1
    smudge_count = 0
    
    while i >= 0 and j < len(pattern):
        diff = count_differences(pattern[i], pattern[j])
        smudge_count += diff
        
        if smudge_count > 1:
            return False
        i -= 1
        j += 1
    
    return smudge_count == 1


def is_vertical_reflection_with_smudge(pattern: List[str], col: int) -> bool:
    # Check if reflection line is between col and col+1 with exactly one smudge
    i, j = col, col + 1
    smudge_count = 0
    
    while i >= 0 and j < len(pattern[0]):
        col_i = [pattern[row][i] for row in range(len(pattern))]
        col_j = [pattern[row][j] for row in range(len(pattern))]
        
        diff = count_differences(''.join(col_i), ''.join(col_j))
        smudge_count += diff
        
        if smudge_count > 1:
            return False
        i -= 1
        j += 1
    
    return smudge_count == 1


def find_reflection_with_smudge(pattern: List[str]) -> tuple:
    # Find reflection line with exactly one smudge, return (type, position)
    
    # Check horizontal reflections
    for row in range(len(pattern) - 1):
        if is_horizontal_reflection_with_smudge(pattern, row):
            return ('h', row)
    
    # Check vertical reflections
    for col in range(len(pattern[0]) - 1):
        if is_vertical_reflection_with_smudge(pattern, col):
            return ('v', col)
    
    return (None, None)


def solve_part_1(lines: List[str]) -> int:
    patterns = parse_patterns(lines)
    total = 0
    
    for pattern in patterns:
        reflection_type, position = find_reflection(pattern)
        
        if reflection_type == 'h':
            total += 100 * (position + 1)
        elif reflection_type == 'v':
            total += position + 1
    
    return total


def solve_part_2(lines: List[str]) -> int:
    patterns = parse_patterns(lines)
    total = 0
    
    for pattern in patterns:
        reflection_type, position = find_reflection_with_smudge(pattern)
        
        if reflection_type == 'h':
            total += 100 * (position + 1)
        elif reflection_type == 'v':
            total += position + 1
    
    return total


if __name__ == "__main__":
    with open("13/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")