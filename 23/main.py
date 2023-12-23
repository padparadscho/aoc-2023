from typing import List, Tuple
from collections import defaultdict, deque


def parse_grid(lines: List[str]) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
    # Parse grid and find start/end positions (single '.' on top and bottom rows)
    grid = [list(line) for line in lines]
    start = (0, lines[0].index('.'))
    end = (len(lines) - 1, lines[-1].index('.'))
    
    return grid, start, end


def get_neighbors(grid: List[List[str]], row: int, col: int, ignore_slopes: bool) -> List[Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    cell = grid[row][col]
    
    if ignore_slopes or cell == '.':
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] != '#':
                neighbors.append((new_row, new_col))
        return neighbors
    elif cell == 'v':
        return [(row + 1, col)]
    elif cell == '^':
        return [(row - 1, col)]
    elif cell == '>':
        return [(row, col + 1)]
    elif cell == '<':
        return [(row, col - 1)]
    
    return []


def is_junction(grid: List[List[str]], row: int, col: int, ignore_slopes: bool) -> bool:
    count = sum(grid[r][c] != '#' for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)])
    return count > 2 or (grid[row][col] != '.' and not ignore_slopes)


def build_graph(grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int], ignore_slopes: bool) -> dict:
    # Build compressed graph with junctions as nodes (reduces search space)
    graph = defaultdict(list)
    visited = set()
    queue = deque([start])
    
    while queue:
        pos = queue.popleft()
        if pos in visited:
            continue
        
        visited.add(pos)
        
        # BFS to find distances to other junctions
        bfs_queue = deque([(pos, 0)])
        bfs_seen = {pos}
        
        while bfs_queue:
            current, dist = bfs_queue.popleft()
            
            for neighbor in get_neighbors(grid, current[0], current[1], ignore_slopes):
                if neighbor in bfs_seen:
                    continue
                
                if neighbor == end or is_junction(grid, neighbor[0], neighbor[1], ignore_slopes):
                    graph[pos].append((neighbor, dist + 1))
                    queue.append(neighbor)
                else:
                    bfs_queue.append((neighbor, dist + 1))
                    bfs_seen.add(neighbor)
    
    return graph


def dfs_longest(graph: dict, current: Tuple[int, int], end: Tuple[int, int], visited: set) -> int:
    # DFS to find longest path (compressed graph makes this tractable)
    if current == end:
        return 0
    
    visited.add(current)
    max_path = 0
    
    for neighbor, dist in graph[current]:
        if neighbor not in visited:
            path_length = dfs_longest(graph, neighbor, end, visited)
            if path_length >= 0:
                max_path = max(max_path, path_length + dist)
    
    visited.remove(current)
    
    return max_path


def solve_part_1(lines: List[str]) -> int:
    grid, start, end = parse_grid(lines)
    graph = build_graph(grid, start, end, ignore_slopes=False)
    
    return dfs_longest(graph, start, end, set())


def solve_part_2(lines: List[str]) -> int:
    grid, start, end = parse_grid(lines)
    graph = build_graph(grid, start, end, ignore_slopes=True)
    
    return dfs_longest(graph, start, end, set())


if __name__ == "__main__":
    with open("23/input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")