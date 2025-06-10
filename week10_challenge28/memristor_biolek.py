"""
memristor_demo_biolek.py
---------------------------------------------------------------
Pinched-hysteresis loops for a Biolek memristor model.
Each curve is produced with a different (freq, k) pair so
you can see how the loop expands, distorts, or collapses.
"""

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------
# Biolek model simulator
# ----------------------------------------------------------------
def iv_biolek(
    V0=1.0, freq=0.2,              #   source amplitude & freq
    Ron=100.0, Roff=16_000.0,      #   device resistances
    k=50.0, p=1,                   #   drift constant & window exponent
    x0=0.25,                       #   initial low-R fraction
    dt=1e-3, n_periods=1):         #   resolution & span
    ω = 2*np.pi*freq
    t = np.arange(0, n_periods/freq, dt)
    V = V0 * np.sin(ω*t)

    x = np.full_like(t, x0)
    I = np.zeros_like(t)

    def W(xx, cur):
        return 0 if cur == 0 else 1 - (2*xx - 1)**(2*p)

    for i in range(1, len(t)):
        R    = Ron*x[i-1] + Roff*(1-x[i-1])
        I[i] = V[i] / R
        x[i] = np.clip(x[i-1] + k*I[i]*W(x[i-1], I[i])*dt, 0, 1)

    I[0] = V[0] / (Ron*x[0] + Roff*(1-x[0]))
    return V, I


# ----------------------------------------------------------------
# Parameter sets chosen to LOOK different on a single graph
# ----------------------------------------------------------------
cases = [
    #  freq,  k,   colour,  label
    (0.05,   50,  "tab:blue",   "wide loop  (0.05 Hz, k=50)"),
    (0.20,   50,  "tab:orange", "moderate   (0.20 Hz, k=50)"),
    (0.20,  200,  "tab:green",  "fatter     (0.20 Hz, k=200)"),
    (1.00,   50,  "tab:red",    "collapsed  (1.00 Hz, k=50)"),
]

plt.figure(figsize=(7,6))

for f, k, c, lbl in cases:
    V, I = iv_biolek(V0=1.0, freq=f, k=k, dt=1e-3, n_periods=2)
    plt.plot(V, I, color=c, label=lbl)

plt.title("Biolek Memristor – Clearly Different Hysteresis Loops")
plt.xlabel("Voltage  (V)")
plt.ylabel("Current  (A)")
plt.grid(alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()
