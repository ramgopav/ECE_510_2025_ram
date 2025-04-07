# disassemble_pyc.py

import dis
import marshal

def disassemble_pyc(pyc_file):
    with open(pyc_file, 'rb') as f:
        f.read(8)  # Skip the header
        code_obj = marshal.load(f)
    dis.dis(code_obj)

if __name__ == "__main__":
    # Adjust the path to your actual .pyc file
    disassemble_pyc('__pycache__/quicksort.cpython-39.pyc')
    disassemble_pyc('__pycache__/matrix_multiplication.cpython-39.pyc')
    disassemble_pyc('__pycache__/ode_solver.cpython-39.pyc')
