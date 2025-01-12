class CPUState:
    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c
        self.pc = 0
        self.out: list[int] = []

    def __str__(self):
        return f"a={self.a}, b={self.b}, c={self.c}, pc={self.pc}, out={",".join([str(o) for o in self.out])}"


def parse_input(f: str):
    with open(f, "r") as file:
        lines = [l for l in file.readlines() if l != "\n"]

    line = iter(lines)
    a = int(next(line).split()[-1])
    b = int(next(line).split()[-1])
    c = int(next(line).split()[-1])
    program = [int(p) for p in next(line).split()[-1].split(",")]
    return (a, b, c, program)


def execute_instruction(opcode: int, operand: int, state: CPUState):
    if operand == 4:
        combo_operand = state.a
    elif operand == 5:
        combo_operand = state.b
    elif operand == 6:
        combo_operand = state.c
    else:
        combo_operand = operand

    # Increment
    state.pc += 2

    # Execute
    match opcode:
        # adv
        case 0:
            state.a = int(state.a / (2**combo_operand))
        # bxl
        case 1:
            state.b = state.b ^ operand
        # bst
        case 2:
            state.b = combo_operand % 8
        # jnz
        case 3:
            if state.a != 0:
                state.pc = operand
        # bxc
        case 4:
            state.b = state.b ^ state.c
        # out
        case 5:
            state.out.append(combo_operand % 8)
        # bdv
        case 6:
            state.b = int(state.a / (2**combo_operand))
        # cdv
        case 7:
            state.c = int(state.a / (2**combo_operand))


def run_program(program: list[int], state: CPUState) -> CPUState:
    while state.pc < len(program) - 1:
        # Fetch
        opcode, operand = program[state.pc], program[state.pc + 1]
        # Increment + execute
        execute_instruction(opcode, operand, state)
    return state


def part1():
    a, b, c, program = parse_input("input.txt")
    state = CPUState(a, b, c)

    return run_program(program, state)


def part2():
    program = parse_input("input.txt")[3]

    # Start with 16 octal digits
    count = 0o1000000000000000
    step = 1
    # Find sequential matched digits, increasing speed each match
    while True:
        run = run_program(program, CPUState(count, 0, 0))

        if run.out == program:
            return count

        if len(run.out) > len(program):
            return None

        for i in range(len(program)):
            if run.out[i] == program[i]:
                step = max(step, 8 ** (i - 1))
            else:
                break

        count += step


print(part2())
