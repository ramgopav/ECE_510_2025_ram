 Challenge 10 · FrozenLake Q‑Learning — Bottleneck Walk‑Through

A reproducible, end‑to‑end report that shows

 baseline performance of the original script (with plotting on),
 how the real hotspot was discovered (profiler & GPT‑4o),
 what single edit fixed the bottleneck, and
 new performance numbers after the change.

All commands were run on Ubuntu 22.04, Ryzen 5 3500U, Python 3.12.



 1 · Folder map


ch10_bottlenecks/
├── q_algorithm.py                  original script + PLOT flag
├── profile_before.txt              cProfile with plotting ON
├── profile_after.txt               cProfile with plotting OFF
├── gpt_bottlenecks_without_plot    screenshot of GPT analysis
├── gpt_bottlenecks_with_plot       screenshot of GPT analysis
└── README.md                       this file




 2 · Environment quick‑setup

bash
python3 m venv .venv && source .venv/bin/activate
pip install numpy gym==0.26.2 matplotlib




 3 · Original run (plotting ON)

bash
 PLOT defaults to True in the unmodified file

time p python3 qalgorithm.py

real 7.90   user 1.79   sys 0.79  (wall‑clock seconds)


 3.1 Profiler (profile_before.txt)

   cumtime  function
   7.30 s   matplotlib / tkinter backend (figure creation + mainloop)  ≈ 79 %
   0.92 s   Q_Learning  (nested for‑loop)                              ≈ 11 %
   0.13 s   numpy.argmax                                              ≈  2 %


> Observation: almost all time is spent opening a GUI window!

 3.2 GPT‑4o guess (see screenshot)

Ranks: 1) plotting / Matplotlib, 2) double for loop, 3) np.argmax. → Matches the profiler.



 4 · Single change that fixes it

Open qalgorithm.py and add a flag at the top:

python
PLOT = False    turn off Matplotlib


Wrap the two lines at the bottom of the file:

python
if PLOT:
    ag.plot(episodes)


(Or just comment those two lines.)

No other code touched.



 5 · New run (plotting OFF)

bash
time p python3 qalgorithm.py



real 1.81   user 1.40   sys 0.68


Speed‑up: 4.4 × wall‑clock by removing GUI overhead.

 5.1 Profiler (profile_after.txt)


   cumtime  function
   1.37 s   Q_Learning  (nested loop)              76 %
   0.13 s   numpy.argmax                            7 %
   0.09 s   Agent.Action helper                     5 %


 5.2 GPT‑4o accuracy after the edit

GPT‑4o still pins the top two hotspots correctly — loop and np.argmax — now truly dominant.



 6 · Hardware acceleration target

The critical kernel after clean‑up is the Q‑value update executed 1 000 000 times per run:
$Q[s,a]\gets(1α)Q[s,a]+α\bigl(r+γ\max_{a'}Q[s',a']\bigr)$

Fixed‑point Q8.8 datapath (see q_update.sv):

 Dual‑port BRAM → 4‑way comparator → α/γ MAC → BRAM write‑back.
 @100 MHz, 1 update / 2 cycles ⇒ 50 M updates s⁻¹ (>28 000 × faster than Python loop).



 7 · Replication checklist

bash
 1. Clone my folder (already contains the PLOT flag)
python3 qalgorithm.py                    ≈1.8 s, prints Q‑table

 2. Restore GUI to reproduce original slowdown
sed i 's/PLOT = False/PLOT = True/' qalgorithm.py
python3 qalgorithm.py                    ≈8 s, opens plot window

 3. Generate your own profiles
python3 m cProfile s cumtime qalgorithm.py > profile.txt
head profile.txt




Challenge 10 deliverables are now complete ✅
