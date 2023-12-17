from typing import List
import heapq


def parse_grid(lines: List[str]) -> List[List[int]]:
    return [[int(c) for c in line] for line in lines]


def find_min_heat_loss(grid: List[List[int]], min_steps: int, max_steps: int) -> int:
    # Dijkstra's algorithm with state: (row, col, direction, steps)
    rows = len(grid)
    cols = len(grid[0])
    
    # Direction deltas: right, down, left, up (0,1,2,3)
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    
    # Start from (0,0) heading right or down
    pq = [(0, 0, 0, 0, 0), (0, 0, 0, 1, 0)]
    visited = set()
    
    while pq:
        heat_loss, row, col, direction, steps = heapq.heappop(pq)
        
        # Reached destination with minimum required steps
        if row == rows - 1 and col == cols - 1 and steps >= min_steps:
            
            return heat_loss
        
        if (row, col, direction, steps) in visited:
            continue
        visited.add((row, col, direction, steps))
        
        # Continue in same direction if under max_steps
        if steps < max_steps:
            new_row = row + dr[direction]
            new_col = col + dc[direction]
            
            if 0 <= new_row < rows and 0 <= new_col < cols:
                new_heat_loss = heat_loss + grid[new_row][new_col]
                heapq.heappush(pq, (new_heat_loss, new_row, new_col, direction, steps + 1))
        
        # Turn left or right if met minimum steps requirement
        if steps >= min_steps or steps == 0:
            for turn in [-1, 1]:
                new_direction = (direction + turn) % 4
                
                # Can't reverse direction
                if new_direction == (direction + 2) % 4:
                    continue
                
                new_row = row + dr[new_direction]
                new_col = col + dc[new_direction]
                
                if 0 <= new_row < rows and 0 <= new_col < cols:
                    new_heat_loss = heat_loss + grid[new_row][new_col]
                    heapq.heappush(pq, (new_heat_loss, new_row, new_col, new_direction, 1))
    
    return -1


def solve_part_1(lines: List[str]) -> int:
    grid = parse_grid(lines)
    
    return find_min_heat_loss(grid, 0, 3)


def solve_part_2(lines: List[str]) -> int:
    grid = parse_grid(lines)
    
    return find_min_heat_loss(grid, 4, 10)


if __name__ == "__main__":
    with open("17/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")