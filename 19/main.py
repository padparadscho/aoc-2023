from typing import Dict, List, Tuple


def parse_workflows(lines: List[str]) -> Dict[str, List[Tuple[str, str, int, str]]]:
    # Parse workflows like "px{a<2006:qkq,m>2090:A,rfg}"
    workflows = {}
    
    for line in lines:
        if not line:
            break
        
        name = line.split('{')[0]
        rules_str = line.split('{')[1][:-1]
        rules = []
        
        for rule in rules_str.split(','):
            if ':' in rule:
                # Conditional rule: "a<2006:qkq"
                condition, dest = rule.split(':')
                if '<' in condition:
                    var, val = condition.split('<')
                    rules.append((var, '<', int(val), dest))
                else:
                    var, val = condition.split('>')
                    rules.append((var, '>', int(val), dest))
            else:
                # Default rule: just destination (A, R, or workflow name)
                rules.append(('', '', 0, rule))
        
        workflows[name] = rules
    
    return workflows


def parse_parts(lines: List[str]) -> List[Dict[str, int]]:
    # Parse parts like "{x=787,m=2655,a=1222,s=2876}"
    parts = []
    
    for line in lines:
        if not line.startswith('{'):
            continue
        
        ratings = {}
        for item in line[1:-1].split(','):
            var, val = item.split('=')
            ratings[var] = int(val)
        
        parts.append(ratings)
    
    return parts


def process_part(part: Dict[str, int], workflows: Dict[str, List[Tuple[str, str, int, str]]]) -> bool:
    # Process part through workflows, return True if accepted
    current = 'in'
    
    while current not in ['A', 'R']:
        rules = workflows[current]
        
        for var, op, val, dest in rules:
            if var == '':
                # Default rule
                current = dest
                break
            
            # Check condition
            part_val = part[var]
            if op == '<':
                if part_val < val:
                    current = dest
                    break
            else:
                if part_val > val:
                    current = dest
                    break
    
    return current == 'A'


def count_accepted_combinations(workflows: Dict[str, List[Tuple[str, str, int, str]]]) -> int:
    # Count all combinations that lead to acceptance using ranges
    def count_recursive(workflow: str, ranges: Dict[str, Tuple[int, int]]) -> int:
        if workflow == 'A':
            # Calculate number of combinations in this range
            result = 1
            for low, high in ranges.values():
                if high < low:
                    return 0
                result *= (high - low + 1)
            return result
        
        if workflow == 'R':
            return 0
        
        rules = workflows[workflow]
        total = 0
        
        for var, op, val, dest in rules:
            if var == '':
                # Default rule: use entire remaining range
                total += count_recursive(dest, ranges.copy())
                break
            
            low, high = ranges[var]
            
            if op == '<':
                if low < val:
                    # Split: values < val go to dest, rest continue
                    new_ranges = ranges.copy()
                    new_ranges[var] = (low, min(high, val - 1))
                    total += count_recursive(dest, new_ranges)
                    ranges[var] = (max(low, val), high)
            else:
                if high > val:
                    # Split: values > val go to dest, rest continue
                    new_ranges = ranges.copy()
                    new_ranges[var] = (max(low, val + 1), high)
                    total += count_recursive(dest, new_ranges)
                    ranges[var] = (low, min(high, val))
        
        return total
    
    # Start with full range 1-4000 for each variable
    initial_ranges = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
    
    return count_recursive('in', initial_ranges)


def solve_part_1(lines: List[str]) -> int:
    workflows = parse_workflows(lines)
    parts = parse_parts(lines)
    
    total = 0
    for part in parts:
        if process_part(part, workflows):
            total += sum(part.values())
    
    return total


def solve_part_2(lines: List[str]) -> int:
    workflows = parse_workflows(lines)
    
    return count_accepted_combinations(workflows)


if __name__ == "__main__":
    with open("19/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")