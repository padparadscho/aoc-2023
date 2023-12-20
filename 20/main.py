from typing import Dict, List, Set
from collections import defaultdict
from math import gcd


def parse_modules(lines: List[str]) -> tuple:
    # Parse module configuration
    modules = {}
    inputs = defaultdict(list)
    
    for line in lines:
        if '->' in line:
            parts = line.split(' -> ')
            source = parts[0]
            dests = [d.strip() for d in parts[1].split(',')]
            
            if source == 'broadcaster':
                modules[source] = ('broadcaster', dests)
            elif source.startswith('%'):
                name = source[1:]
                modules[name] = ('flipflop', dests)
            elif source.startswith('&'):
                name = source[1:]
                modules[name] = ('conjunction', dests)
            
            for dest in dests:
                inputs[dest].append(source[1:] if source[0] in '%&' else source)
    
    return modules, dict(inputs)


def simulate_pulse(modules: Dict[str, tuple], inputs: Dict[str, List[str]], button_presses: int, find_rx: bool = False) -> tuple:
    # Simulate pulses through module network
    module_types = {name: info[0] for name, info in modules.items()}
    dests = {name: info[1] for name, info in modules.items()}
    
    # Initialize states
    flipflop_states = {name: False for name, typ in module_types.items() if typ == 'flipflop'}
    conjunction_states = {name: {inp: False for inp in inputs[name]} for name, typ in module_types.items() if typ == 'conjunction'}
    
    low_count = 0
    high_count = 0
    
    # Track when inputs to conjunction feeding rx first send high pulse
    rx_input_cycles = {}
    rx_feeder = None
    
    if find_rx:
        # Find conjunction module that feeds into rx
        for name in inputs.get('rx', []):
            rx_feeder = name
            break
    
    press_count = 0
    
    while press_count < button_presses:
        press_count += 1
        
        # Button sends low pulse to broadcaster
        pulses = [('broadcaster', False, 'button')]
        
        while pulses:
            new_pulses = []
            
            for dest, pulse, source in pulses:
                if pulse:
                    high_count += 1
                else:
                    low_count += 1
                
                if dest not in modules:
                    continue
                
                module_type = module_types[dest]
                
                if module_type == 'broadcaster':
                    for d in dests[dest]:
                        new_pulses.append((d, pulse, dest))
                
                elif module_type == 'flipflop':
                    if not pulse:
                        flipflop_states[dest] = not flipflop_states[dest]
                        for d in dests[dest]:
                            new_pulses.append((d, flipflop_states[dest], dest))
                
                elif module_type == 'conjunction':
                    conjunction_states[dest][source] = pulse
                    
                    # Track when inputs to rx_feeder first send high
                    if find_rx and rx_feeder and dest == rx_feeder and pulse:
                        if source not in rx_input_cycles:
                            rx_input_cycles[source] = press_count
                    
                    all_high = all(conjunction_states[dest].values())
                    for d in dests[dest]:
                        new_pulses.append((d, not all_high, dest))
            
            pulses = new_pulses
        
        # Check if we found all cycles for rx_feeder inputs
        if find_rx and rx_feeder:
            if len(rx_input_cycles) == len(inputs[rx_feeder]):
                break
    
    return low_count, high_count, rx_input_cycles


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def solve_part_1(lines: List[str]) -> int:
    modules, inputs = parse_modules(lines)
    low_count, high_count, _ = simulate_pulse(modules, inputs, 1000)
    
    return low_count * high_count


def solve_part_2(lines: List[str]) -> int:
    modules, inputs = parse_modules(lines)
    
    # Find when inputs to conjunction feeding rx first send high pulse
    _, _, rx_input_cycles = simulate_pulse(modules, inputs, 1000000, find_rx=True)
    
    # LCM of all cycle lengths
    result = 1
    for cycle_length in rx_input_cycles.values():
        result = lcm(result, cycle_length)
    
    return result


if __name__ == "__main__":
    with open("20/input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")