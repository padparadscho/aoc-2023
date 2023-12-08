from typing import List, Tuple
from math import lcm


def parse_input(lines: List[str]) -> Tuple[str, dict]:
    # Parse input: line 0 is instructions, lines1+ are node definitions
    instructions = lines[0]
    
    network = {}
    for line in lines[1:]:
        parts = line.split(" = ")
        node = parts[0]
        left, right = parts[1].strip("()").split(", ")
        network[node] = (left, right)
    
    return instructions, network


def count_steps_to_zzz(instructions: str, network: dict) -> int:
    current = "AAA"
    steps = 0
    i = 0
    
    while current != "ZZZ":
        direction = instructions[i % len(instructions)]
        left, right = network[current]
        current = left if direction == "L"else right
        
        steps += 1
        i += 1
    
    return steps


def count_steps_to_z(node: str, instructions: str, network: dict) -> int:
    steps = 0
    i = 0
    
    while not node.endswith("Z"):
        direction = instructions[i % len(instructions)]
        left, right = network[node]
        node = left if direction == "L" else right
        
        steps += 1
        i += 1
    
    return steps


def solve_part_1(lines: List[str]) -> int:
    instructions, network = parse_input(lines)
    
    return count_steps_to_zzz(instructions, network)


def solve_part_2(lines: List[str]) -> int:
    instructions, network = parse_input(lines)
    
    starts = [node for node in network if node.endswith("A")]
    
    # Each starting node cycles to a Z node in a fixed number of steps
    # Find cycle length for each starting node, then use LCM
    cycle_lengths = []
    for start in starts:
        steps = count_steps_to_z(start, instructions, network)
        cycle_lengths.append(steps)
    
    result = 1
    for length in cycle_lengths:
        result = lcm(result, length)
    
    return result


if __name__ == "__main__":
    with open("08/input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    print(solve_part_1(lines))
    print(solve_part_2(lines))