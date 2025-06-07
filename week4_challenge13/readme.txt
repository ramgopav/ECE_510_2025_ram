
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
