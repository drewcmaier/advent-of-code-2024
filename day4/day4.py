def parse_input() -> str:
    lines = []
    
    with open("input.txt", "r") as file:
        lines = file.readlines()
      
    rows = []  
    for line in lines:
        cur_row = []
        for c in line:
            if c != "\n":
                cur_row.append(c)
        rows.append(cur_row)
        
    return rows

def find_word_in_word_search(board, word):
    count = 0
    
    def backtrack(r, c, index, dir):
        nonlocal count
        
        if index == len(word):
            count += 1
            return
        
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[index]:
            return

        # Mark the cell as visited
        prev_val, board[r][c] = board[r][c], "."

        dr, dc = dir
        backtrack(r + dr, c + dc, index + 1, dir)

        board[r][c] = prev_val

    rows, cols = len(board), len(board[0])
    directions = [
        (0, 1),   # Right
        (0, -1),  # Left
        (1, 0),   # Down
        (-1, 0),  # Up
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
        (-1, 1),  # Diagonal up-right
        (-1, -1), # Diagonal up-left
    ]

    for r in range(rows):
            for c in range(cols):
                if board[r][c] == word[0]:
                    for dir in directions:
                        backtrack(r, c, 0, dir)

    return count

def find_patterns_in_word_search(board, patterns):
    rows, cols = len(board), len(board[0])
    
    def matches_pattern(r, c, pattern):
        pattern_rows, pattern_cols = len(pattern), len(pattern[0])
        
        for r_pattern in range(0, pattern_rows):
            for c_pattern in range(0, pattern_cols):                
                board_r, board_c = r+r_pattern, c+c_pattern
                if board_r >= rows or board_c >= cols:
                    return False
                
                # No match if pattern is filled in and different than board
                if pattern[r_pattern][c_pattern] != '.' and pattern[r_pattern][c_pattern] != board[board_r][board_c]:
                    return False
        
        return True
            

    count = 0
    for r in range(rows):
        for c in range(cols):
            for pattern in patterns:
                if matches_pattern(r, c, pattern):
                    count += 1

    return count

def part1(): 
    rows = parse_input()
    matches = find_word_in_word_search(rows, "XMAS")
    print(f"Matches: {matches}")

def part2():
    rows = parse_input()
    patterns = [
        ['M.M',
         '.A.',
         'S.S'],
        ['M.S',
         '.A.',
         'M.S'],
        ['S.M',
         '.A.',
         'S.M'],
        ['S.S',
         '.A.',
         'M.M']
    ]
    matches = find_patterns_in_word_search(rows, patterns)
    print(f"Matches: {matches}")
    
part2()