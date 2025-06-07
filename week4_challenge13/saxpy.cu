#include <cstdio>
#include <cstdlib>
#include <cuda_runtime.h>

__global__ void saxpy(int n, float a, const float *x, float *y)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = a * x[i] + y[i];
}

int main(int argc, char **argv)
{
    int pow = (argc > 1) ? atoi(argv[1]) : 20;   // default N = 2^20
    int N   = 1 << pow;
    size_t bytes = N * sizeof(float);

    // Host buffers
    float *h_x = (float*)malloc(bytes);
    float *h_y = (float*)malloc(bytes);
    for (int i = 0; i < N; ++i) { h_x[i] = 1.0f; h_y[i] = 2.0f; }

    // Device buffers
    float *d_x, *d_y;
    cudaMalloc(&d_x, bytes);
    cudaMalloc(&d_y, bytes);

    cudaEvent_t start, stop;
    float h2d_ms, kernel_ms, d2h_ms;
    cudaEventCreate(&start); cudaEventCreate(&stop);

    // ---------------- Host ➜ Device copy ----------------
    cudaEventRecord(start);
    cudaMemcpy(d_x, h_x, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_y, h_y, bytes, cudaMemcpyHostToDevice);
    cudaEventRecord(stop);  cudaEventSynchronize(stop);
    cudaEventElapsedTime(&h2d_ms, start, stop);

    // ---------------- Kernel launch ----------------
    int threads = 256;
    int blocks  = (N + threads - 1) / threads;
    cudaEventRecord(start);
    saxpy<<<blocks, threads>>>(N, 3.0f, d_x, d_y);
    cudaEventRecord(stop);  cudaEventSynchronize(stop);
    cudaEventElapsedTime(&kernel_ms, start, stop);

    // ---------------- Device ➜ Host copy ----------------
    cudaEventRecord(start);
    cudaMemcpy(h_y, d_y, bytes, cudaMemcpyDeviceToHost);
    cudaEventRecord(stop);  cudaEventSynchronize(stop);
    cudaEventElapsedTime(&d2h_ms, start, stop);


    printf("N=%d  H2D=%.3f ms  kernel=%.3f ms  D2H=%.3f ms\n",
           N, h2d_ms, kernel_ms, d2h_ms);

    // Quick correctness check
    float max_err = 0.0f;
    for (int i = 0; i < N; ++i) max_err = fmax(max_err, fabs(h_y[i] - 5.0f));
    printf("Max error: %f\n", max_err);

    cudaFree(d_x); cudaFree(d_y); free(h_x); free(h_y);
    return 0;
}

