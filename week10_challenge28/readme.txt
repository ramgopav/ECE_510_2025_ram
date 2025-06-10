 Challenge 28 – Memristor Modeling & Simulation

This repository documents my solution to Challenge 28: Model and simulate a memristor.



  Objective

1. Implement the Biolek‐window memristor model in pure Python.
2. Drive the device with a sinusoidal source and reproduce the hallmark pinched hysteresis loop in the I–V plane.
3. Explore how drive frequency (freq) and drift constant (k) change the loop shape.
4. Document code, equations, and results so the work is reproducible.



  Repository Structure

| Path                       | Purpose                                            |
|  |  |
| memristor_biolek.py      | Minimal script: single loop for default parameters |
| iv_loops.png             | Sample output from the demo script                 |
| README.md                | This file                                          |



 Model Summary

| Symbol | Meaning                                         | Typical value  |
|  |  |  |
| Ron  | Low‑resistance state (Ω)                        | 100 Ω          |
| Roff | High‑resistance state (Ω)                       | 16 kΩ          |
| x(t) | Fraction of low‑R region $0 ≤ x ≤ 1$            | 0.25 (initial) |
| k    | Drift constant (controls speed of state change) | 10 – 200       |
| p    | Window exponent (Biolek)                        | 1              |

 Equations


M(x)        = Ron·x + Roff·(1 − x)          memristance
V(t)        = V0·sin(2π·freq·t)             drive source
I(t)        = V(t) / M(x(t))
dx/dt       = k · I(t) · [1 − (2x − 1)^(2p)]    Biolek window




 Quick Start

bash
python m venv .venv && source .venv/bin/activate    optional
pip install numpy matplotlib

 1 simple loop
python memristor_biolek.py      shows one hysteresis curve

 4 curves with different (freq,k) pairs
python memristor_demo_biolek.py


The demo script will generate iv_loops.png that looks like this:

![Example output](iv_loops.png)



 Results & Analysis

| Curve label | Parameters                  | Observation                                                |
|  |  |  |
| wide loop | freq = 0.05 Hz, k = 50  | Very broad lobes because the state has ample time to drift |
| moderate  | freq = 0.20 Hz, k = 50  | Classic "figure‑8"                                         |
| fatter    | freq = 0.20 Hz, k = 200 | Same frequency, bigger k → loop inflates                 |
| collapsed | freq = 1.00 Hz, k = 50  | High frequency; loop shrinks to ohmic line                 |

Key conclusions:

 Drive period is critical: as freq ↑, the loop narrows → memristor behaves like a resistor at very high freq (Chua’s prediction).
 Drift constant k scales how “memristive” the device looks at a given freq.
 The loop always pinches at the origin $(0,0)$, confirming purely dissipative behaviour.

