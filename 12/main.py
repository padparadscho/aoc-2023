from typing import List, Tuple
from functools import lru_cache


def parse_line(line: str) -> Tuple[str, List[int]]:
    # Parse line like "???.### 1,1,3"
    parts = line.split()
    springs = parts[0]
    groups = [int(x) for x in parts[1].split(',')]
    
    return springs, groups


def unfold_record(springs: str, groups: List[int]) -> Tuple[str, List[int]]:
    # Unfold record by repeating 5 times with ? separator
    unfolded_springs = '?'.join([springs] * 5)
    unfolded_groups = groups * 5
    
    return unfolded_springs, unfolded_groups


@lru_cache(maxsize=None)
def count_arrangements(springs: str, groups: Tuple[int, ...], current_group: int = -1) -> int:
    # Base case: no more springs to process
    if not springs:
        # If in a group, it must match the first remaining group
        if current_group > 0:
            if groups and groups[0] == current_group:
                groups = groups[1:]
                current_group = -1
            else:
                return 0
        # Should have no more groups to match
        return 1 if not groups and current_group <= 0 else 0
    
    result = 0
    first_char = springs[0]
    
    # Try '.' option, either explicitly '.' or '?'
    if first_char in '.?':
        if current_group > 0:
            if groups and groups[0] == current_group:
                result += count_arrangements(springs[1:], groups[1:], -1)
        elif current_group == -1:
            result += count_arrangements(springs[1:], groups, -1)
    
    # Try '#' option, either explicitly '#' or '?'
    if first_char in '#?':
        if current_group == -1:
            result += count_arrangements(springs[1:], groups, 1)
        else:
            result += count_arrangements(springs[1:], groups, current_group + 1)
    
    return result


def solve_part_1(lines: List[str]) -> int:
    total = 0
    
    for line in lines:
        springs, groups = parse_line(line)
        arrangements = count_arrangements(springs, tuple(groups))
        total += arrangements
        count_arrangements.cache_clear()
    
    return total


def solve_part_2(lines: List[str]) -> int:
    total = 0
    
    for line in lines:
        springs, groups = parse_line(line)
        unfolded_springs, unfolded_groups = unfold_record(springs, groups)
        arrangements = count_arrangements(unfolded_springs, tuple(unfolded_groups))
        total += arrangements
        count_arrangements.cache_clear()
    
    return total


if __name__ == "__main__":
    with open("12/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")