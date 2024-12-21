from typing import List, Tuple

def parse_input() -> Tuple[List[int], List[int]]:
    with open("input.txt", "r") as file:
        lines = file.readlines()
        
    left = []
    right = []
    for line in lines:
        parts = line.split()
        
        left.append(int(parts[0]))
        right.append(int(parts[1]))

    left.sort()
    right.sort()
    return [left, right]

def part1():    
    left, right = parse_input()
    total_diff = 0
    for i in range(len(left)):
        diff = abs(left[i] - right[i])
        total_diff += diff

    print(total_diff)
    
def part2():
    left, right = parse_input()
    
    right_frequency_map = {}
    for r in right:
        if r not in right_frequency_map:
            right_frequency_map[r] = 0
        
        right_frequency_map[r] += 1
    
    total_similarity = 0
    for l in left:
        similarity_score = l * right_frequency_map[l] if l in right_frequency_map else 0
        total_similarity += similarity_score
    
    print(total_similarity)