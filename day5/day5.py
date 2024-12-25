from functools import cmp_to_key

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
    
    def find_child(self, val):
        bfs = [self]
        visited = {}
        while len(bfs) > 0:
            n = bfs.pop()
            if n not in visited:
                visited[n] = n
            else:
                continue
            
            if n.value == val:
                return n
            bfs.extend(n.children)
            
        return None
    
def parse_input():
    order = []
    update = []
    with open("input.txt", "r") as file:
        lines = file.readlines()
      
    split_index = lines.index("\n")
    for dep in lines[:split_index]:
        n1, n2 = dep.strip().split("|")
        order.append([int(n1), int(n2)])
    
    update_lines = lines[split_index+1:]
    for u in update_lines:
        nums = [int(num) for num in u.strip().split(",")]
        update.append(nums)
            
    return [order, update]

def find_or_create_node(root, val):
    n = root.find_child(val)
    if not n:
        n = Node(val)
        root.children.append(n)
    return n

def is_greater(root, v1, v2):
    n1 = root.find_child(v1)
    if not n1:
        return False
    
    return n1.find_child(v2) != None

def is_correct_update(update, root):
    for i in range(0, len(update)-1):
        v1, v2 = update[i], update[i+1]
        if not is_greater(root, v1, v2):
            return False
        
    return True
    
def part1():
    order, update = parse_input()
    
    # Find correct updates
    correct_updates = []
    for u in update:
        # Build tree only for numbers used in update
        root = Node(None)
        for o1, o2 in order:
            if o1 in u and o2 in u:
                n1, n2 = find_or_create_node(root, o1), find_or_create_node(root, o2)
                n1.children.append(n2)
                
        if is_correct_update(u, root):
            correct_updates.append(u)
            
    print(f"Correct: {len(correct_updates)} of {len(update)}")
    
    # Sum middle elements
    middle_sum = 0
    for correct in correct_updates:
        middle = correct[int(len(correct) / 2)]
        middle_sum += middle
    
    return middle_sum

def fix_update(update, root):
    # Use custom comparitor with is_greater
    def compare(v1, v2):
        if is_greater(root, v1, v2):
            return -1
        elif is_greater(root, v2, v1):
            return 1
        else:
            return 0
        
    return sorted(update, key=cmp_to_key(compare))

def part2():
    order, update = parse_input()
    
    fixed_updates = []
    for u in update:
        # Build tree only for numbers used in update
        root = Node(None)
        for o1, o2 in order:
            if o1 in u and o2 in u:
                n1, n2 = find_or_create_node(root, o1), find_or_create_node(root, o2)
                n1.children.append(n2)
            
            
        if not is_correct_update(u, root):
            fixed = fix_update(u, root)
            fixed_updates.append(fixed)
    
    # Sum middle elements
    middle_sum = 0
    for correct in fixed_updates:
        middle = correct[int(len(correct) / 2)]
        middle_sum += middle
    
    return middle_sum
