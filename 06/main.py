import math


def parse_races(lines: list[str]) -> list[tuple[int, int]]:
    time_parts = lines[0].split(":")[1].split()
    distance_parts = lines[1].split(":")[1].split()
    
    # Parse lines like "Time: 54 81 70 88"
    return [(int(t), int(d)) for t, d in zip(time_parts, distance_parts)]


def count_ways(time: int, record: int) -> int:
    # hold * (time - hold) > record
    # This is quadratic: hold^2 - time*hold + record < 0
    discriminant = time * time - 4 * record
    
    if discriminant <= 0:
        
        return 0
    
    sqrt_disc = math.sqrt(discriminant)
    
    # Roots: (time ± √discriminant) / 2
    h1 = (time - sqrt_disc) / 2
    h2 = (time + sqrt_disc) / 2
    
    # Count integers strictly between roots
    first_win = math.floor(h1) + 1
    last_win = math.ceil(h2) - 1
    
    return last_win - first_win + 1


def solve_part_1(lines: list[str]) -> int:
    races = parse_races(lines)
    
    result = 1
    for time, record in races:
        result *= count_ways(time, record)
    
    return result


def solve_part_2(lines: list[str]) -> int:
    time_str = "".join(lines[0].split(":")[1].split())
    distance_str = "".join(lines[1].split(":")[1].split())
    
    time = int(time_str)
    record = int(distance_str)
    
    return count_ways(time, record)


if __name__ == "__main__":
    with open("06/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")