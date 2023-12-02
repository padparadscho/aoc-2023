from typing import Final, Dict


# Cube counts available in the bag
AVAILABLE_CUBES: Final[Dict[str, int]] = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_game(line: str) -> tuple[int, list[Dict[str, int]]]:
    # Parse line like "Game 1: 3 blue, 4 red; 1 red, 2 green"
    game_part, subsets_part = line.split(": ")
    game_id = int(game_part.split()[1])
    
    subsets = []
    for subset_str in subsets_part.split("; "):
        subset: Dict[str, int] = {}
        for cube_str in subset_str.split(", "):
            count, color = cube_str.split()
            subset[color] = int(count)
        subsets.append(subset)
    
    return game_id, subsets


def is_game_possible(subsets: list[Dict[str, int]]) -> bool:
    # Check if all cube counts fit within available cubes
    for subset in subsets:
        for color, count in subset.items():
            if count > AVAILABLE_CUBES.get(color, 0):
                return False
    
    return True


def solve_part_1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        game_id, subsets = parse_game(line)
        if is_game_possible(subsets):
            total += game_id
    
    return total


def solve_part_2(lines: list[str]) -> int:
    total_power = 0
    for line in lines:
        _, subsets = parse_game(line)
        
        # Find minimum cubes needed (max of each color across all subsets)
        min_red = max(subset.get("red", 0) for subset in subsets)
        min_green = max(subset.get("green", 0) for subset in subsets)
        min_blue = max(subset.get("blue", 0) for subset in subsets)
        
        power = min_red * min_green * min_blue
        total_power += power
    
    return total_power


if __name__ == "__main__":
    with open("02/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")