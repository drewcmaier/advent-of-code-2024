import re

def parse_input() -> str:
    with open("input.txt", "r") as file:
        buf = file.read()
        
    return buf


def part1():
    buf = parse_input()
    
    pattern = re.compile(r"mul\((\d+),(\d+)\)")
    result = pattern.findall(buf)
    
    sum = 0
    for a, b in result:
        sum += (int(a) * int(b))
        
    return sum
    
def part2():
    buf = parse_input()
    
    pattern = re.compile(r"(?:(?:(do|don't)\(\))|mul\((\d+),(\d+)\))")
    result = pattern.findall(buf)
    
    sum = 0
    can_do = True
    for do_dont, a, b in result:
        if do_dont == "do":
            can_do = True
        elif do_dont == "don't":
            can_do = False
        
        if a and b and can_do:
            sum += (int(a) * int(b))
        
    return sum
