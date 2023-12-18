from typing import List, Tuple


def parse_instruction(line: str) -> Tuple[str, int]:
    # Parse line like "R 6 (#70c710)"
    parts = line.split()
    direction = parts[0]
    distance = int(parts[1])
    
    return direction, distance


def parse_instruction_hex(line: str) -> Tuple[str, int]:
    # Parse hex code from line like "R 6 (#70c710)"
    parts = line.split()
    hex_code = parts[2][2:-1]  # Remove (# and )
    
    distance = int(hex_code[:5], 16)
    direction_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    direction = direction_map[hex_code[5]]
    
    return direction, distance


def get_vertices(instructions: List[Tuple[str, int]]) -> List[Tuple[int, int]]:
    # Follow instructions to get polygon vertices
    vertices = [(0, 0)]
    row, col = 0, 0
    
    # Direction deltas: R, D, L, U (row change, col change)
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    direction_map = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
    
    for direction, distance in instructions:
        d = direction_map[direction]
        row += dr[d] * distance
        col += dc[d] * distance
        vertices.append((row, col))
    
    return vertices


def calculate_area(vertices: List[Tuple[int, int]]) -> int:
    # Shoelace formula to calculate polygon area
    n = len(vertices)
    area = 0
    
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    
    return abs(area) // 2


def calculate_perimeter(instructions: List[Tuple[str, int]]) -> int:
    # Sum of all distances
    return sum(distance for _, distance in instructions)


def solve_part_1(lines: List[str]) -> int:
    instructions = [parse_instruction(line) for line in lines]
    vertices = get_vertices(instructions)
    
    area = calculate_area(vertices)
    perimeter = calculate_perimeter(instructions)
    
    # Shoelace area + half perimeter + 1 for boundary width
    return area + perimeter // 2 + 1


def solve_part_2(lines: List[str]) -> int:
    instructions = [parse_instruction_hex(line) for line in lines]
    vertices = get_vertices(instructions)
    
    area = calculate_area(vertices)
    perimeter = calculate_perimeter(instructions)
    
    return area + perimeter // 2 + 1


if __name__ == "__main__":
    with open("18/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")