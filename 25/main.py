from typing import Dict, Set, List
import random
from collections import defaultdict


def parse_graph(lines: List[str]) -> Dict[str, Set[str]]:
    # Parse lines like "jqt: rhn xhk nvd" into adjacency list
    graph = {}
    
    for line in lines:
        node, connections = line.split(':')
        node = node.strip()
        connections = connections.strip().split()
        
        if node not in graph:
            graph[node] = set()
        
        for conn in connections:
            graph[node].add(conn)
            if conn not in graph:
                graph[conn] = set()
            graph[conn].add(node)
    
    return graph


def karger_min_cut(nodes: List[str], edges: List[tuple]) -> tuple:
    parent = {n: n for n in nodes}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    num_components = len(nodes)
    component_size = {n: 1 for n in nodes}
    edge_list = edges.copy()
    
    while num_components > 2 and edge_list:
        idx = random.randint(0, len(edge_list) - 1)
        u, v = edge_list.pop(idx)
        
        root_u = find(u)
        root_v = find(v)
        
        if root_u == root_v:
            continue
        
        if component_size[root_u] < component_size[root_v]:
            root_u, root_v = root_v, root_u
        
        parent[root_v] = root_u
        component_size[root_u] += component_size[root_v]
        num_components -= 1
    
    components = defaultdict(set)
    for node in nodes:
        components[find(node)].add(node)
    
    comp_sizes = [len(c) for c in components.values()]
    
    cut_edges = 0
    for u, v in edges:
        if find(u) != find(v):
            cut_edges += 1
    
    return cut_edges, comp_sizes[0] * comp_sizes[1]  # cut size and product of componentsizes


def solve_part_1(lines: List[str]) -> int:
    graph = parse_graph(lines)
    
    nodes = list(graph.keys())
    edges = []
    for u in graph:
        for v in graph[u]:
            if u < v:  # Avoid duplicates
                edges.append((u, v))
    
    for _ in range(1000):
        cut_size, product = karger_min_cut(nodes, edges)
        
        if cut_size == 3:  # Karger's algorithm: run until finding min-cut of size 3
            return product
    
    return -1


if __name__ == "__main__":
    with open("25/input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")