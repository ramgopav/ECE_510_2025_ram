# ode_solver.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def dydx(x, y):
    return y - x**2 + 1

def solve_ode():
    sol = solve_ivp(dydx, (0, 5), [0.5], t_eval=np.linspace(0, 5, 100))
    plt.plot(sol.t, sol.y[0])
    plt.show()

if __name__ == "__main__":
    solve_ode()
