from typing import List, Tuple

type BlockList = List[str]
type DiskMapList = List[int]

EMPTY_BLOCK = "."


def parse_input(f) -> DiskMapList:
    with open(f, "r") as file:
        input = file.readline()

    disk_map = [int(c) for c in input]
    return disk_map


def print_blocks(blocks: BlockList):
    print("".join([str(int(b) % 10) if b != EMPTY_BLOCK else "." for b in blocks]))


def get_blocks(disk_map: DiskMapList) -> BlockList:
    # Pre-allocate blocks. Total number of blocks is sum of disk map entries
    total_blocks = 0
    for b in disk_map:
        total_blocks += b
    blocks = [EMPTY_BLOCK] * total_blocks

    id = 0
    block_idx = 0
    for disk_map_index in range(len(disk_map)):
        cur_block_size = disk_map[disk_map_index]
        is_file = disk_map_index % 2 == 0

        for cur_block_idx in range(block_idx, block_idx + cur_block_size):
            blocks[cur_block_idx] = str(id) if is_file else EMPTY_BLOCK

        if is_file:
            id += 1

        block_idx += cur_block_size

    return blocks


def defrag_blocks(blocks: BlockList) -> BlockList:
    defragged = blocks[:]

    head, tail = 0, len(blocks) - 1
    while head < tail:
        is_head_empty = defragged[head] == EMPTY_BLOCK
        is_tail_empty = defragged[tail] == EMPTY_BLOCK

        # Swap when start block is empty and end block is occupied
        if is_head_empty and not is_tail_empty:
            defragged[head], defragged[tail] = defragged[tail], defragged[head]

        # March pointers toward each other when they are in the correct conditions
        if not is_head_empty:
            head += 1
        if is_tail_empty:
            tail -= 1

    return defragged


def find_first_empty_block(blocks: BlockList, block_size, bounds: range) -> int:
    run_start = run_end = bounds.start
    prev_block = ""

    for i in bounds:
        id_changed = blocks[i] != prev_block
        if id_changed:
            if blocks[i] == EMPTY_BLOCK:
                run_start = run_end = i
            elif prev_block == EMPTY_BLOCK:
                run_end = i
                if run_end - run_start >= block_size:
                    return run_start

        prev_block = blocks[i]

    return -1


def defrag_files(disk_map: DiskMapList, blocks: BlockList) -> BlockList:
    defragged = blocks[:]

    tail = len(blocks) - 1
    disk_map_idx = len(disk_map) - 1

    # General idea: starting from highest block id, find required number of empty blocks.
    # Then, scan until a contiguous set of empty blocks is found and move to that location.
    # This is n^2, but it works fast enough for this case
    while disk_map_idx >= 0:
        tail_block_size = disk_map[disk_map_idx]

        # Find unoccupied space starting from lowest empty address
        first_empty_block = find_first_empty_block(
            defragged, tail_block_size, range(0, tail)
        )

        # Move to lower block
        if first_empty_block >= 0:
            for b in range(0, tail_block_size):
                defragged[first_empty_block + b], defragged[tail - b] = (
                    defragged[tail - b],
                    defragged[first_empty_block + b],
                )

        # Move up tail, including empty blocks
        for _ in range(2):
            tail_block_size = disk_map[disk_map_idx]
            tail -= tail_block_size
            disk_map_idx -= 1

    return defragged


def compute_checksum(blocks: BlockList):
    return sum([i * int(n) for i, n in enumerate(blocks) if n != EMPTY_BLOCK])


def part1():
    disk_map = parse_input("input.txt")

    blocks = get_blocks(disk_map)
    print_blocks(blocks)

    defragged = defrag_blocks(blocks)
    print_blocks(defragged)

    checksum = compute_checksum(defragged)
    print(f"Checksum: {checksum}")


def part2():
    disk_map = parse_input("input.txt")

    blocks = get_blocks(disk_map)

    defragged = defrag_files(disk_map, blocks)
    # print_blocks(defragged)

    checksum = compute_checksum(defragged)
    print(f"Checksum: {checksum}")


part2()
