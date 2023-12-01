from typing import Final


# Spelled out digits
WORD_TO_DIGIT: Final[dict[str, str]] = {
    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
    'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
}


def solve_part_1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        digits = [c for c in line if c.isdigit()]
        assert digits, f"Line has no digits: {line}"
        # Combine first and last digit to form the calibration value
        total += int(digits[0] + digits[-1])
    
    return total


def solve_part_2(lines: list[str]) -> int:
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Find first digit or spelled out word from left
        first_digit: str | None = None
        for i in range(len(line)):
            if line[i].isdigit():
                first_digit = line[i]
                break
            for word, digit in WORD_TO_DIGIT.items():
                if line[i:i+len(word)] == word:
                    first_digit = digit
                    break
            if first_digit:
                break

        # Find last digit or spelled out word from right
        last_digit: str | None = None
        for i in range(len(line) - 1, -1, -1):
            if line[i].isdigit():
                last_digit = line[i]
                break
            for word, digit in WORD_TO_DIGIT.items():
                if line[i:i+len(word)] == word:
                    last_digit = digit
                    break
            if last_digit:
                break

        assert first_digit is not None and last_digit is not None, f"Line has no digits: {line}"
        total += int(first_digit + last_digit)
    
    return total


if __name__ == "__main__":
    with open('01/input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")