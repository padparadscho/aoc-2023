from typing import List, Set, Dict
from collections import defaultdict, deque


def parse_bricks(lines: List[str]) -> List[tuple]:
    # Parse lines like "1,0,1~1,2,1" into (x1, y1, z1, x2, y2, z2)
    bricks = []
    for line in lines:
        start, end = line.split('~')
        x1, y1, z1 = map(int, start.split(','))
        x2, y2, z2 = map(int, end.split(','))
        bricks.append((x1, y1, z1, x2, y2, z2))
    
    return bricks


def get_brick_cubes(brick: tuple) -> Set[tuple]:
    x1, y1, z1, x2, y2, z2 = brick
    cubes = set()
    
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for z in range(min(z1, z2), max(z1, z2) + 1):
                cubes.add((x, y, z))
    
    return cubes


def settle_bricks(bricks: List[tuple]) -> List[Set[tuple]]:
    # Drop bricks down until they hit ground or other bricks
    sorted_bricks = sorted(bricks, key=lambda b: min(b[2], b[5]))
    
    settled_cubes = []
    occupied = set()
    
    for brick in sorted_bricks:
        cubes = get_brick_cubes(brick)
        
        while True:
            can_fall = True
            
            for x, y, z in cubes:
                if z == 1 or (x, y, z - 1) in occupied:
                    can_fall = False
                    break
            
            if can_fall:
                cubes = {(x, y, z - 1) for (x, y, z) in cubes}
            else:
                break
        
        settled_cubes.append(cubes)
        occupied.update(cubes)
    
    return settled_cubes


def build_support_graph(bricks: List[Set[tuple]]) -> tuple:
    # Build support relationships: which bricks support which others
    all_cubes = {}
    for i, cubes in enumerate(bricks):
        for cube in cubes:
            all_cubes[cube] = i
    
    supported_by = defaultdict(set)
    supports = defaultdict(set)
    
    for i, cubes in enumerate(bricks):
        for x, y, z in cubes:
            if z == 1:
                continue
            
            below = (x, y, z - 1)
            if below in all_cubes:
                j = all_cubes[below]
                if j != i:
                    supported_by[i].add(j)
                    supports[j].add(i)
    
    return supported_by, supports


def solve_part_1(lines: List[str]) -> int:
    # Count bricks that can be safely disintegrated (no other brick would fall)
    bricks = parse_bricks(lines)
    bricks.sort(key=lambda b: min(b[2], b[5]))
    
    settled = settle_bricks(bricks)
    supported_by, supports = build_support_graph(settled)
    
    disintegratable = 0
    
    for i in range(len(settled)):
        can_disintegrate = True
        for j in supports[i]:
            if len(supported_by[j]) == 1:
                can_disintegrate = False
                break
        
        if can_disintegrate:
            disintegratable += 1
    
    return disintegratable


def count_falling(supports: Dict[int, Set[int]], supported_by: Dict[int, Set[int]], removed: int) -> int:
    # BFS to count bricks that fall in cascade after removing one brick
    q = deque([removed])
    falling = set()
    
    while q:
        brick = q.popleft()
        falling.add(brick)
        
        for supported in supports[brick]:
            if supported in falling:
                continue
            
            if all(support in falling for support in supported_by[supported]):
                falling.add(supported)
                q.append(supported)
    
    return len(falling) - 1


def solve_part_2(lines: List[str]) -> int:
    bricks = parse_bricks(lines)
    bricks.sort(key=lambda b: min(b[2], b[5]))
    
    settled = settle_bricks(bricks)
    supported_by, supports = build_support_graph(settled)
    
    total = 0
    
    for i in range(len(settled)):
        total += count_falling(supports, supported_by, i)
    
    return total


if __name__ == "__main__":
    with open("22/input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")