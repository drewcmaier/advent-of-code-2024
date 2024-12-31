type Grid = list[list[str]]
type Location = tuple[int, int]
type Region = list[tuple[Location, int]]


def parse_input(f: str) -> Grid:
    with open(f, "r") as file:
        lines = file.readlines()

    grid: Grid = [[c for c in line.strip()] for line in lines]
    return grid


def in_bounds(loc: Location, grid: Grid) -> bool:
    rows, cols = len(grid), len(grid[0])
    return 0 <= loc[0] < rows and 0 <= loc[1] < cols


def find_regions(grid: Grid) -> dict[str, Region]:
    directions = [
        (0, 1),  # Right
        (0, -1),  # Left
        (1, 0),  # Down
        (-1, 0),  # Up
    ]
    regions: dict[str, Region] = {}
    grid_visited: set[Location] = set()

    def get_region(start: Location) -> tuple[str, Region]:
        start_id = grid[start[0]][start[1]]
        region_visited: set[Location] = set()
        region: list[tuple[Location, int]] = []
        bfs = [start]

        while len(bfs) > 0:
            loc = bfs.pop()

            if loc in region_visited or loc in grid_visited:
                continue

            region_visited.add(loc)

            id = grid[loc[0]][loc[1]]
            if id != start_id:
                continue

            perimeter = 4
            for d in directions:
                d_loc: Location = (loc[0] + d[0], loc[1] + d[1])
                if not in_bounds(d_loc, grid):
                    continue

                # Pre-compute perimeter while iterating neighbors.
                # Every location starts with a perimeter of 4. Subtract 1 for each neighbor of same id.
                d_id = grid[d_loc[0]][d_loc[1]]
                if d_id == start_id:
                    perimeter -= 1

                bfs.append(d_loc)

            grid_visited.add(loc)
            region.append((loc, perimeter))

        return (start_id, region)

    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            loc = (row, col)
            id, region = get_region(loc)

            if id not in regions:
                regions[id] = []

            if len(region) > 0:
                regions[id].append(region)

    return regions


def compute_area(region: Region) -> int:
    return len(region)


def compute_perimeter(region: Region) -> int:
    # perimeter is pre-computed in region tuple
    return sum([r[1] for r in region])


def compute_sides(region: Region, grid: Grid) -> int:
    # Sides are equivlanet to corners. To calculate a corner, check how many
    # adjacent grid locations share a vertex. Corners have an odd number of shared locations.
    # Some examples:
    # XX  XX  X    X
    # X    X  XX  XX
    # There is one edge case, which is when two locations share a vertex diagonally:
    # X   X
    #  X X
    # This has an even number of locations and counts as 2 sides since each side has its own corner.
    vertices: dict[Location, set[Region]] = {}
    for point in region:
        r, c = point[0]
        corners = [(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)]
        for corner in corners:
            if corner not in vertices:
                vertices[corner] = set()
            vertices[corner].add(point[0])

    num_sides = 0
    for vertex in vertices:
        points_at_v = vertices[vertex]

        # Sides have an odd number of contributing vertices
        if len(points_at_v) % 2 == 1:
            num_sides += 1

        # Edge case: only diagonals contribute (no L shape). This counts as 2 sides
        if len(points_at_v) == 2:
            p0, p1 = points_at_v
            if abs(p0[0] - p1[0]) + abs(p0[1] - p1[1]) == 2:
                num_sides += 2
    return num_sides


def part1():
    grid = parse_input("input.txt")
    regions = find_regions(grid)

    total_price = 0
    for region_id in regions:
        regions_with_id = regions[region_id]
        for region in regions_with_id:
            area = compute_area(region)
            perimeter = compute_perimeter(region)
            price = area * perimeter
            total_price += price
            print(f"{region_id}: {area} * {perimeter} = {price}")
    return total_price


def part2():
    grid = parse_input("input.txt")
    regions = find_regions(grid)

    total_price = 0
    for region_id in regions:
        regions_with_id = regions[region_id]
        for region in regions_with_id:
            area = compute_area(region)
            sides = compute_sides(region, grid)
            price = area * sides
            total_price += price
            print(f"{region_id}: {area} * {sides} = {price}")
    return total_price
