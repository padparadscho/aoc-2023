from typing import List


# Parse line like "0 3 6 9 12 15"
def parse_line(line: str) -> List[int]:
    return [int(x) for x in line.split()]


# Compute differences between consecutive elements
def get_differences(sequence: List[int]) -> List[int]:
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


# Extrapolate next value by building difference sequences and summing last elements
def extrapolate_forward(sequence: List[int]) -> int:
    if all(x == 0 for x in sequence):
        return 0

    differences = get_differences(sequence)

    return sequence[-1] + extrapolate_forward(differences)


# Extrapolate previous value by building difference sequences and subtracting first elements
def extrapolate_backward(sequence: List[int]) -> int:
    if all(x == 0 for x in sequence):
        return 0

    differences = get_differences(sequence)

    return sequence[0] - extrapolate_backward(differences)


def solve_part_1(lines: List[str]) -> int:
    total = 0

    for line in lines:
        sequence = parse_line(line)
        total += extrapolate_forward(sequence)

    return total


def solve_part_2(lines: List[str]) -> int:
    total = 0

    for line in lines:
        sequence = parse_line(line)
        total += extrapolate_backward(sequence)

    return total


if __name__ == "__main__":
    with open("09/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")