import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import py_compile
import dis
import cProfile
import multiprocessing
from itertools import permutations
import torch
import torch.nn as nn
import torch.optim as optim

# === Differential Equation Solver ===
def dydx(x, y):
    return y - x**2 + 1

def solve_ode():
    sol = solve_ivp(dydx, (0, 5), [0.5], t_eval=np.linspace(0, 5, 100))
    plt.plot(sol.t, sol.y[0])
    plt.show()

# === Convolutional Neural Network ===
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(16 * 28 * 28, 10)
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        return x

def train_cnn():
    model = SimpleCNN()
    optimizer = optim.Adam(model.parameters())
    criterion = nn.CrossEntropyLoss()
    dummy_input = torch.randn(1, 1, 28, 28)
    output = model(dummy_input)
    loss = criterion(output, torch.tensor([1]))
    loss.backward()
    optimizer.step()

# === Traveling Salesman Problem (TSP) ===
def tsp_bruteforce(cities):
    min_path = None
    min_cost = float("inf")
    for perm in permutations(range(len(cities))):
        cost = sum(np.linalg.norm(cities[perm[i]] - cities[perm[i+1]]) for i in range(len(cities)-1))
        if cost < min_cost:
            min_cost = cost
            min_path = perm
    return min_path, min_cost

def solve_tsp():
    cities = np.random.rand(5, 2)
    tsp_bruteforce(cities)

# === Bytecode Compilation ===
def compile_code():
    py_compile.compile('python_workloads.py')

# === Disassemble Bytecode ===
def disassemble_code():
    with open('python_workloads.py', 'r') as f:
        code = f.read()
    dis.dis(code)

# === Instruction Counting ===
def count_instructions():
    instructions = dis.Bytecode(solve_ode).dis()
    instr_count = {}
    for instr in instructions:
        instr_count[instr.opname] = instr_count.get(instr.opname, 0) + 1
    print(instr_count)

# === Profiling ===
def profile_code():
    cProfile.run('solve_ode()')
    cProfile.run('train_cnn()')
    cProfile.run('solve_tsp()')

# === Parallelism Analysis ===
def parallel_ode():
    with multiprocessing.Pool(4) as pool:
        results = pool.map(dydx, np.linspace(0, 5, 100))
        print(results)

# === Run Disassembly on Script ===
def disassemble_script():
    with open("python_workloads.py", "r") as f:
        code = f.read()
    dis.dis(code)

if __name__ == "__main__":
    solve_ode()
    train_cnn()
    solve_tsp()
    compile_code()
    disassemble_code()
    count_instructions()
    profile_code()
    parallel_ode()
    disassemble_script()
