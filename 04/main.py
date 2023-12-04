def parse_card(line: str) -> tuple[set[int], set[int]]:
    # Parse line like "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    parts = line.split(":")[1].split("|")
    winning = set(int(x) for x in parts[0].split())
    have = set(int(x) for x in parts[1].split())
    
    return winning, have


def solve_part_1(lines: list[str]) -> int:
    total = 0
    
    for line in lines:
        winning, have = parse_card(line)
        matches = len(winning & have)
        
        if matches > 0:
            total += 2 ** (matches - 1)
    
    return total


def solve_part_2(lines: list[str]) -> int:
    # Track copies of each card (card number -> count)
    copies: dict[int, int] = {i: 1 for i in range(1, len(lines) + 1)}
    
    for i, line in enumerate(lines, start=1):
        winning, have = parse_card(line)
        matches = len(winning & have)
        
        # For each match, win copies of next cards
        for j in range(i + 1, i + matches + 1):
            if j in copies:
                copies[j] += copies[i]
    
    return sum(copies.values())


if __name__ == "__main__":
    with open("04/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")