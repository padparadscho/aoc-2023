def parse_seeds(line: str) -> list[int]:
    # Parse line like "seeds: 79 14 55 13"
    return [int(x) for x in line.split(':')[1].strip().split()]


def parse_map(lines: list[str], start_idx: int) -> tuple[list[tuple[int, int, int]], int]:
    # Parse mapping ranges, return (ranges, next_index)
    # Each range is (destination_start, source_start, length)
    ranges = []
    idx = start_idx
    while idx < len(lines) and lines[idx].strip():
        parts = lines[idx].strip().split()
        if len(parts) == 3 and parts[0].isdigit():
            ranges.append((int(parts[0]), int(parts[1]), int(parts[2])))
        idx += 1
    
    return ranges, idx + 1


def apply_map(number: int, ranges: list[tuple[int, int, int]]) -> int:
    for dest_start, src_start, length in ranges:
        if src_start <= number < src_start + length:
            return dest_start + (number - src_start)
    
    return number


def apply_map_to_range(
    input_range: range, 
    ranges: list[tuple[int, int, int]]
) -> list[range]:
    # Apply mapping to a range, return list of mapped ranges
    result = []
    to_process = [input_range]
    
    for dest_start, src_start, length in ranges:
        src_end = src_start + length
        new_to_process = []
        
        for r in to_process:
            # Split range into: before, overlap, after
            before = range(r.start, min(r.stop, src_start))
            overlap = range(max(r.start, src_start), min(r.stop, src_end))
            after = range(max(r.start, src_end), r.stop)
            
            # Non-overlapping parts need further processing
            if len(before) > 0:
                new_to_process.append(before)
            if len(after) > 0:
                new_to_process.append(after)
            
            # Overlapping part gets mapped
            if len(overlap) > 0:
                offset = dest_start - src_start
                mapped = range(overlap.start + offset, overlap.stop + offset)
                result.append(mapped)
        
        to_process = new_to_process
    
    # Any remaining ranges map to themselves
    result.extend(to_process)
    
    return result


def solve_part_1(lines: list[str]) -> int:
    seeds = parse_seeds(lines[0])
    
    # Parse all maps
    maps: list[list[tuple[int, int, int]]] = []
    idx = 2  # Skip seeds line and blank line
    while idx < len(lines):
        if 'map:' in lines[idx]:
            ranges, idx = parse_map(lines, idx + 1)
            maps.append(ranges)
        else:
            idx += 1
    
    # Find minimum location
    min_location = float('inf')
    for seed in seeds:
        number = seed
        for ranges in maps:
            number = apply_map(number, ranges)
        min_location = min(min_location, number)
    
    return int(min_location)


def solve_part_2(lines: list[str]) -> int:
    seed_data = parse_seeds(lines[0])
    
    # Parse all maps
    maps: list[list[tuple[int, int, int]]] = []
    idx = 2
    while idx < len(lines):
        if 'map:' in lines[idx]:
            ranges, idx = parse_map(lines, idx + 1)
            maps.append(ranges)
        else:
            idx += 1
    
    # Process seed ranges efficiently
    seed_ranges = []
    for i in range(0, len(seed_data), 2):
        start, length = seed_data[i], seed_data[i + 1]
        seed_ranges.append(range(start, start + length))
    
    # Apply all maps to seed ranges
    current_ranges = seed_ranges
    for ranges in maps:
        new_ranges = []
        for r in current_ranges:
            new_ranges.extend(apply_map_to_range(r, ranges))
        current_ranges = new_ranges
    
    # Find minimum location
    return min(r.start for r in current_ranges)


if __name__ == "__main__":
    with open('05/input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")