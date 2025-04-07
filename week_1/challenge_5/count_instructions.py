import dis
from collections import defaultdict

# Define instruction categories
CATEGORIES = {
    "Arithmetic": {"BINARY_OP", "UNARY_OP"},
    "Comparison": {"COMPARE_OP"},
    "Control Flow": {
        "POP_JUMP_FORWARD_IF_TRUE", "POP_JUMP_FORWARD_IF_FALSE",
        "JUMP_FORWARD", "JUMP_BACKWARD", "FOR_ITER", "RETURN_VALUE",
        "RESUME"
    },
    "Function Call": {"CALL", "CALL_FUNCTION", "CALL_METHOD", "PRECALL"},
    "Variable Access": {
        "LOAD_FAST", "STORE_FAST", "LOAD_CONST", "LOAD_GLOBAL",
        "STORE_GLOBAL", "LOAD_NAME", "STORE_NAME",
        "LOAD_ATTR", "STORE_ATTR"
    },
}

def categorize_instruction(opname):
    for category, opnames in CATEGORIES.items():
        if opname in opnames:
            return category
    return "Other"

def count_and_categorize_instructions(func):
    raw_counts = defaultdict(int)
    categorized_counts = defaultdict(int)
    for instr in dis.Bytecode(func):
        raw_counts[instr.opname] += 1
        cat = categorize_instruction(instr.opname)
        categorized_counts[cat] += 1
    return raw_counts, categorized_counts

def report(func_name, raw_counts, categorized_counts):
    print(f"\n=== {func_name} ===")
    print("\nRaw Instruction Counts:")
    for instr, count in sorted(raw_counts.items()):
        print(f"  {instr:25} {count}")

    print("\nCategorized Instruction Counts:")
    for category, count in sorted(categorized_counts.items()):
        print(f"  {category:20} {count}")

if __name__ == "__main__":
    from quicksort import quicksort
    from matrix_multiplication import matrix_multiply
    from ode_solver import solve_ode

    # Analyze and report for each function
    for name, func in [
        ("QuickSort", quicksort),
        ("Matrix Multiplication", matrix_multiply),
        ("ODE Solver", solve_ode),
    ]:
        raw, cat = count_and_categorize_instructions(func)
        report(name, raw, cat)
