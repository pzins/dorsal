#include "cuda_runtime.h"
#include "kernel.h"
#include <iostream>

#define BLOCKDIMX 128
#define GRIDDIMX 100


__global__ void add(int* a, int* b, int* c){
    int idx = blockIdx.x * BLOCKDIMX + threadIdx.x;
    c[idx] = a[idx] + b[idx];
}


int main()
{
    int NB_BLOCK = GRIDDIMX;
    int SIZE = 1*NB_BLOCK  ;
    int h_a[SIZE], h_b[SIZE], h_c[SIZE];
    int *d_a, *d_b, *d_c;
    int *d_d, *d_e, *d_f;
    // int* h_c = (int*)malloc(sizeof(int)*SIZE);
    for(int i = 0; i < SIZE; ++i){
        h_a[i] = i;
        h_b[i] = SIZE-i;
    }

    cudaStream_t stream1;
    cudaStream_t stream2;

    cudaStreamCreate(&stream1);
    cudaStreamCreate(&stream2);


    cudaMalloc((void**)&d_a, SIZE * sizeof(int));
    cudaMalloc((void**)&d_b, SIZE * sizeof(int));
    cudaMalloc((void**)&d_c, SIZE * sizeof(int));

    cudaMalloc((void**)&d_d, SIZE * sizeof(int));
    cudaMalloc((void**)&d_e, SIZE * sizeof(int));
    cudaMalloc((void**)&d_f, SIZE * sizeof(int));

    cudaMemcpyAsync(d_a, h_a, SIZE*sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpyAsync(d_b, h_b, SIZE*sizeof(int), cudaMemcpyHostToDevice);

    cudaMemcpy(d_d, h_a, SIZE*sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(d_e, h_b, SIZE*sizeof(int), cudaMemcpyHostToDevice);

    add<<<NB_BLOCK, BLOCKDIMX, 0, stream1>>>(d_a, d_b, d_c);
    add<<<NB_BLOCK, BLOCKDIMX, 0, stream2>>>(d_d, d_e, d_f);
    // add<<<1, 1>>>(0,0,0);

    cudaMemcpy(h_c, d_c, SIZE*sizeof(int), cudaMemcpyDeviceToHost);
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    cudaFree(d_d);
    cudaFree(d_e);
    cudaFree(d_f);
    int i = 0;
    for(i = 0; i < SIZE; ++i){
        std::cout << h_c[i] << " ";
    }
    std::cout << std::endl << i << std::endl;

    return 0;
}
