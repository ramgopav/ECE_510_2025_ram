
scales on an NVIDIA GPU.

 Goals of the challenge
  

 Tooling  Set up a CUDA environment (Google Colab’s free Tesla K80) 
 Coding  Write / modify CUDA C++, launch a kernel, and time it with cudaEvent 
 Analysis  Sweep problem sizes 2^15–2^25, log hosttodevice (H2D), kernel, and devicetohost (D2H) latencies 
 Visuals  Create bar plots of kernel time, endtoend time, and effective memorybandwidth 

All artifacts—source, logs, plots—live in this repo.

2  Repository contents
 File  What it is 

 saxpy.cu             Selfcontained CUDA SAXPY program with event timing & correctness check 
 timings.txt          Raw benchmark output (N, H2D ms, Kernel ms, D2H ms) 
 plot_kernel.png      Bar chart – kernel time only 
 plot_total.png       Bar chart – total time (copies + kernel) 
 plot_bandwidth.png   Bar chart – effective GB/s (derived)
 plot_bandwidth.py    used to create plot_bandwidth.png

 3  How to reproduce

 A. Google Colab (zero local setup)
1. Open Colab → Runtime ▸ Change runtime type ▸ GPU.  
2. Clone this repo:  
   bash
   !git clone https://github.com/<yourhandle>/<repo>.git
   %cd <repo>
3.Compile & run:
!nvcc -O3 saxpy.cu -o saxpy
for p in range(15, 26):
    !./saxpy $p >> timings.txt
4.Re-generate plots:
!python plot_saxpy.py        # or run plot_saxpy.ipynb



I spun up a fresh Google Colab notebook, flipped the runtime to GPU, and confirmed the Tesla K80 and CUDA were ready to roll. Then I wrote saxpy.cu, a tiny CUDA program that runs the SAXPY math (y = a·x + y) on the GPU. I wrapped the data copy-in, the kernel launch, and the copy-out with CUDA event timers, so every run told me exactly how many milliseconds each stage took.

Next I swept that program across ten vector sizes—from 2¹⁵ up to 2²⁵ numbers—and saved the timings to timings.txt. With those raw numbers in hand I used a short Python notebook to draw two quick bar charts: one showing just the kernel time and another showing the total time (copies plus kernel).

To turn those milliseconds into something more meaningful, I added a little helper script called plot_bandwidth.py. It reads timings.txt, skips the slow first launch, converts each kernel time into effective memory bandwidth in GB/s, prints a clean table, and saves a third plot (plot_bandwidth.png). That plot lets you see at a glance how performance climbs until the K80’s memory pipeline saturates at about 120–130 GB/s.

Finally, I bundled everything—the CUDA source, the log file, all three plots, the bandwidth script, and a README—so anyone can clone the repo, run the notebook, and reproduce the exact same story.
