from typing import List

def parse_input():
    with open("input.txt", "r") as file:
        lines = file.readlines()
        
    vals = []
    for line in lines:
        line_vals = [int(val) for val in line.split()]
        vals.append(line_vals)
        
    return vals
    
def is_safe(report: List[int]) -> bool:
    prev_diff = 0
    
    for i in range(1, len(report)):
        diff = report[i] - report[i-1]
        if abs(diff) < 1 or abs(diff) > 3:
            return False
        
        if diff < 0 and prev_diff > 0 or diff > 0 and prev_diff < 0:
            return False
        
        prev_diff = diff
    
    return True


def part1():    
    reports = parse_input()
    
    num_safe = 0
    for report in reports:
        if is_safe(report):
            num_safe += 1
        
    return num_safe

def is_safe_with_tolerance(report: List[int]) -> bool:
    for i in range(len(report)):
        report_without_ith_element = report[:]
        report_without_ith_element.pop(i)
        
        if is_safe(report_without_ith_element):
            return True
        
    return False
    
def part2():
    reports = parse_input()
    
    num_safe = 0
    for report in reports:
        if is_safe_with_tolerance(report):
            num_safe += 1
        
    return num_safe

print(part2())