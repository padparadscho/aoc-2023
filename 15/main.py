from typing import List, Dict


def hash_string(s: str) -> int:
    # HASH algorithm: for each char, add ASCII, multiply by 17, mod 256
    current = 0
    
    for char in s:
        current += ord(char)
        current *= 17
        current %= 256
    
    return current


def parse_steps(line: str) -> List[str]:
    # Parse comma separated steps from input line
    return [step.strip() for step in line.split(',')]


def process_step(step: str, boxes: Dict[int, List[tuple]]) -> None:
    # Process a single step and modify boxes in place
    # "label=focal_length" or "label-"
    
    if '=' in step:
        # Add or replace lens
        label, focal_length_str = step.split('=')
        focal_length = int(focal_length_str)
        box_num = hash_string(label)
        
        # Find if label already exists in box
        if box_num not in boxes:
            boxes[box_num] = []
        
        # Check if label already exists
        found = False
        for i, (existing_label, _) in enumerate(boxes[box_num]):
            if existing_label == label:
                boxes[box_num][i] = (label, focal_length)
                found = True
                break
        
        if not found:
            boxes[box_num].append((label, focal_length))
    
    else:
        # Remove lens
        label = step[:-1]  # Remove the '-'
        box_num = hash_string(label)
        
        if box_num in boxes:
            boxes[box_num] = [(l, f) for l, f in boxes[box_num] if l != label]


def calculate_focusing_power(boxes: Dict[int, List[tuple]]) -> int:
    # Calculate total focusing power: (box_num + 1) * slot_num * focal_length
    total = 0
    
    for box_num, lenses in boxes.items():
        for slot_num, (_, focal_length) in enumerate(lenses, start=1):
            total += (box_num + 1) * slot_num * focal_length
    
    return total


def solve_part_1(lines: List[str]) -> int:
    # Parse all steps and sum hash values
    steps = parse_steps(lines[0])
    total = 0
    
    for step in steps:
        total += hash_string(step)
    
    return total


def solve_part_2(lines: List[str]) -> int:
    # Process all steps and calculate focusing power
    steps = parse_steps(lines[0])
    boxes: Dict[int, List[tuple]] = {}
    
    for step in steps:
        process_step(step, boxes)
    
    return calculate_focusing_power(boxes)


if __name__ == "__main__":
    with open("15/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")