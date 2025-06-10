 Challenge 16 – CUDA vs PyTorch on a 4 → 5 → 1 FeedForward Network

<kbd>Google Colab · Tesla K80 · CUDA 12.x · PyTorch 2.x</kbd>



 1  Problem statement
Write two GPU implementations of a toy fullyconnected network


 Version A: handcoded CUDA C++ using cuBLAS + a custom ReLU kernel.  
 Version B: PyTorch layers (nn.Linear + ReLU).  
Benchmark both, verify the outputs match, and discuss any speed gap.



 2  Repo contents
| File | Purpose |
|||
| weights.bin | Deterministic input x, weights W1,W2, biases b1,b2 (rowmajor) |
| ffnet.cu | Custom CUDA forward pass (CUBLAS_OP_T GEMV + inplace ReLU) |
| pytorch_bench.py | PyTorch reference implementation & timing harness |
| cuda_vs_pytorch_results.pptx | Fourslide summary deck |
| README.md | this file |



 3  How to reproduce — Colab in 90 sec

bash
 (1) switch runtime → GPU, then run these:
!git clone https://github.com/<yourhandle>/<thisrepo>.git
%cd <thisrepo>

 (2) regenerate deterministic weights & compile CUDA
!python pytorch_bench.py writeweights           writes weights.bin
!nvcc O3 ffnet.cu lcublas o ffnet

 (3) benchmark
!./ffnet        run twice: 1st warms context, 2nd is clean timing
!python pytorch_bench.py                          prints PyTorch result
Both programs should print the same output value (≈ −2.48749) to 1 × 10⁻⁵
and the following latencies on a free Tesla K80:

Implementation	Single pass (ms)	1 000pass avg (µs)
CUDA (custom)	≈ 8.6	≈ 8.6
PyTorch	≈ 11.6	≈ 11.5

4 Key results

Custom kernel beats PyTorch by ≈ 25 % on this toy layer.

Once hidden width ≥ 128, PyTorch’s cuBLASfused kernels catch up and the
gap vanishes (see log–log scaling plot).

5 Lessons learned
Orientation matters.
cuBLAS expects columnmajor; storing weights rowmajor means every GEMV
must use CUBLAS_OP_T to stay numerically identical to PyTorch.

Launch overhead is huge for tiny kernels.
A single GEMV on Colab’s virtualised K80 takes ~8 ms to launch.
Averaging over many passes (~8 µs each) reveals the real compute cost.

PyTorch is “free” performance tuning.
For layers big enough to saturate memory bandwidth (>128 × 128), PyTorch
equals or beats handwritten code thanks to heavilytuned cuBLAS calls.
