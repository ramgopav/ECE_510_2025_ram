#include <cstdio>
#include <cublas_v2.h>
#include <cuda_runtime.h>
#define CHECK(x) do{auto e=(x); if(e!=CUBLAS_STATUS_SUCCESS){printf("cuBLAS %d\n",e); return 1;}}while(0)
__global__ void relu(float* x,int n){int i=blockIdx.x*blockDim.x+threadIdx.x; if(i<n&&x[i]<0) x[i]=0;}
int main(){
    const int NI=4,NH=5,NO=1; float hx[NI],W1[NH*NI],b1[NH],W2[NO*NH],b2[NO];
    FILE*fp=fopen("weights.bin","rb");
    fread(hx,4,NI,fp); fread(W1,4,NH*NI,fp); fread(b1,4,NH,fp); fread(W2,4,NO*NH,fp); fread(b2,4,NO,fp); fclose(fp);
    float *dx,*dW1,*db1,*dW2,*db2; cudaMalloc(&dx,16); cudaMalloc(&dW1,4*NH*NI); cudaMalloc(&db1,4*NH);
    cudaMalloc(&dW2,4*NO*NH); cudaMalloc(&db2,4*NO);
    cudaMemcpy(dx,hx,16,cudaMemcpyHostToDevice);
    cudaMemcpy(dW1,W1,4*NH*NI,cudaMemcpyHostToDevice);
    cudaMemcpy(db1,b1,4*NH,cudaMemcpyHostToDevice);
    cudaMemcpy(dW2,W2,4*NO*NH,cudaMemcpyHostToDevice);
    cudaMemcpy(db2,b2,4*NO,cudaMemcpyHostToDevice);
    cublasHandle_t h; CHECK(cublasCreate(&h));
    const float a=1.f,b=1.f;
    for(int i=0;i<5;++i) CHECK(cublasSgemv(h,CUBLAS_OP_T,NI,NH,&a,dW1,NI,dx,1,&b,db1,1));
    cudaMemcpy(db1,b1,4*NH,cudaMemcpyHostToDevice);
    cudaMemcpy(db2,b2,4*NO,cudaMemcpyHostToDevice);
    cudaEvent_t t0,t1; cudaEventCreate(&t0); cudaEventCreate(&t1); cudaEventRecord(t0);
    CHECK(cublasSgemv(h,CUBLAS_OP_T,NI,NH,&a,dW1,NI,dx,1,&b,db1,1));
    relu<<<1,32>>>(db1,NH);
    CHECK(cublasSgemv(h,CUBLAS_OP_T,NH,NO,&a,dW2,NH,db1,1,&b,db2,1));
    cudaEventRecord(t1); cudaEventSynchronize(t1); float ms; cudaEventElapsedTime(&ms,t0,t1);
    float out; cudaMemcpy(&out,db2,4,cudaMemcpyDeviceToHost);
    printf("CUDA out %.6f | %.3f µs\n",out,ms*1000);
}
