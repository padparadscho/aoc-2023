from typing import List, Tuple


# Card values for ranking hands (higher = stronger)
CARD_VALUES = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

# Card values with J as weakest (joker becomes wildcard for hand type)
CARD_VALUES_JOKER = {'A': 14, 'K': 13, 'Q': 12, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}


def get_hand_type(hand: str) -> int:
    counts = {}
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    
    values = sorted(counts.values(), reverse=True)
    
    if values == [5]:
        return 7  # Five of a kind
    elif values == [4, 1]:
        return 6  # Four of a kind
    elif values == [3, 2]:
        return 5  # Full house
    elif values == [3, 1, 1]:
        return 4  # Three of a kind
    elif values == [2, 2, 1]:
        return 3  # Two pair
    elif values == [2, 1, 1, 1]:
        return 2  # One pair
    else:
        return 1  # High card


def get_hand_type_with_joker(hand: str) -> int:
    joker_count = hand.count('J')
    
    if joker_count == 0:
        return get_hand_type(hand)
    
    if joker_count == 5:
        return 7  # Five of a kind
    
    counts = {}
    for card in hand:
        if card != 'J':
            counts[card] = counts.get(card, 0) + 1
    
    values = sorted(counts.values(), reverse=True)
    
    # Add jokers to highest count
    values[0] += joker_count
    
    if values == [5]:
        return 7  # Five of a kind
    elif values == [4, 1]:
        return 6  # Four of a kind
    elif values == [3, 2]:
        return 5  # Full house
    elif values == [3, 1, 1]:
        return 4  # Three of a kind
    elif values == [2, 2, 1]:
        return 3  # Two pair
    elif values == [2, 1, 1, 1]:
        return 2  # One pair
    else:
        return 1  # High card


def hand_strength(hand: str, card_values: dict) -> tuple:
    # Return (hand_type, card_values) tuple for sorting
    hand_type = get_hand_type(hand)
    card_values_list = tuple(card_values[card] for card in hand)
    
    return (hand_type, card_values_list)


def hand_strength_with_joker(hand: str) -> tuple:
    # Return (hand_type, card_values) tuple for sorting with joker rules
    hand_type = get_hand_type_with_joker(hand)
    card_values_list = tuple(CARD_VALUES_JOKER[card] for card in hand)
    
    return (hand_type, card_values_list)


def parse_line(line: str) -> Tuple[str, int]:
    # Parse line like "32T3K 765"
    parts = line.split()
    
    return parts[0], int(parts[1])


def solve_part_1(lines: List[str]) -> int:
    hands = []
    for line in lines:
        hand, bid = parse_line(line)
        strength = hand_strength(hand, CARD_VALUES)
        hands.append((strength, hand, bid))
    
    hands.sort()
    
    total = 0
    for rank, (strength, hand, bid) in enumerate(hands, 1):
        total += bid * rank
    
    return total


def solve_part_2(lines: List[str]) -> int:
    hands = []
    for line in lines:
        hand, bid = parse_line(line)
        strength = hand_strength_with_joker(hand)
        hands.append((strength, hand, bid))
    
    hands.sort()
    
    total = 0
    for rank, (strength, hand, bid) in enumerate(hands, 1):
        total += bid * rank
    
    return total


if __name__ == "__main__":
    with open("07/input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    print(solve_part_1(lines))
    print(solve_part_2(lines))