// add this in CMakeList file line 218 to build the wrapper library
/*
include_directories(${PROJECT_SOURCE_DIR}/include)
add_library(mylib SHARED
    include/hip.cpp
)
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -shared -ldl -fPIC -Wl,-Bsymbolic")
*/
// to build place this file in /home/pierre/dev/HIP/include

#include <iostream>

#include <stdint.h>
#include <stddef.h>
#include <iostream>

#include <hip/hcc_detail/host_defines.h>
#include <hip/hip_runtime_api.h>
#include <hip/hcc_detail/driver_types.h>
#include <hip/hcc_detail/hip_texture_types.h>
#include <dlfcn.h>
// #include <grid_launch.h>
// #include "hc_printf.hpp"
// 
// 
hipError_t hipStreamCreateWithFlags(hipStream_t *stream, unsigned int flags) {
    std::cout << "LYON" << std::endl;
    void *handle;
    typedef hipError_t (*hipStreamCreateWithFlags_)(hipStream_t*, unsigned int);

    char *error;
    handle = dlopen ("/opt/rocm/hip/lib/libhip_hcc.so", RTLD_LAZY);
    if (!handle) {
        fputs (dlerror(), stderr);
        exit(1);
    }
    hipStreamCreateWithFlags_ hh = (hipStreamCreateWithFlags_) dlsym(handle, "hipStreamCreateWithFlags");
    if ((error = dlerror()) != NULL)  {
        fputs(error, stderr);
        exit(1);
    }
    return hh(stream, flags);
    dlclose(handle);
}

hipError_t hipEventRecord(hipEvent_t event, hipStream_t stream) {
    std::cout << 1111111111111111111111 << std::endl;
}


hipError_t hipMemcpyHtoDAsync(hipDeviceptr_t dst, void* src, size_t sizeBytes, hipStream_t stream) {
    std::cout << "3333333333333333" << std::endl;
}

// hipError_t hipStreamCreate(hipStream_t *stream) {
//     std::cout << "FEKIR" << std::endl;
//     void *handle;
//     typedef hipError_t (*hipStreamCreate_)(hipStream_t*);
// 
//     char *error;
//     handle = dlopen ("/opt/rocm/hip/lib/libhip_hcc.so", RTLD_LAZY);
//     if (!handle) {
//         fputs (dlerror(), stderr);
//         exit(1);
//     }
//     hipStreamCreate_ hh = (hipStreamCreate_) dlsym(handle, "hipStreamQuery");
//     if ((error = dlerror()) != NULL)  {
//         fputs(error, stderr);
//         exit(1);
//     }
//     return hh(stream);
//     dlclose(handle);
// }

// 
// hipError_t hipMemcpyDtoHAsync(void* dst, hipDeviceptr_t src, size_t sizeBytes, hipStream_t stream) {
//     hipError_t t;
//     return t;
//     std::cout << "MEMPHIS" << std::endl;
//     void *handle;
//     typedef hipError_t (*hipMemcpyDtoHAsync_)(void*, hipDeviceptr_t, size_t, hipStream_t);
// 
//     char *error;
//     handle = dlopen ("/opt/rocm/hip/lib/libhip_hcc.so", RTLD_LAZY);
//     if (!handle) {
//         fputs (dlerror(), stderr);
//         exit(1);
//     }
//     hipMemcpyDtoHAsync_ hh = (hipMemcpyDtoHAsync_) dlsym(handle, "hipStreamQuery");
//     if ((error = dlerror()) != NULL)  {
//         fputs(error, stderr);
//         exit(1);
//     }
//     return hh(dst, src, sizeBytes, stream);
//     dlclose(handle);
// }
// 
// 
// hipStream_t ihipPreLaunchKernel(hipStream_t stream, dim3 grid, dim3 block, grid_launch_parm *lp, const char *kernelNameStr) {
// 
//     std::cout << "MEMPHIS" << std::endl;
// }
// 
// void ihipPostLaunchKernel(const char *kernelName, hipStream_t stream, grid_launch_parm &lp) {
// 
//     std::cout << "LYONLYONLYON" << std::endl;
// }









hipError_t hipStreamWaitEvent(hipStream_t stream, hipEvent_t event, unsigned int flags) {
    std::cout << "4444444444444444" << std::endl;
    hipError_t e;
    return e;
}





hipError_t hipStreamCreateWithFlags(hipStream_t *stream, unsigned int flags) { 
std::cout << "LLYYOONN" << std::endl;
}


// 
// hipError_t hipStreamSynchronize(hipStream_t stream) { 
// std::cout << "O L" << std::endl;
// }







hipError_t hipStreamQuery(hipStream_t stream) {
    std::cout << "OLOLOL" << std::endl;
    void *handle;
    typedef hipError_t (*hipStreamQuery_)(hipStream_t);
    
    char *error;
    handle = dlopen ("/opt/rocm/hip/lib/libhip_hcc.so", RTLD_LAZY);
    if (!handle) {
        fputs (dlerror(), stderr);
        exit(1);
    }
    hipStreamQuery_ hh = (hipStreamQuery_) dlsym(handle, "hipStreamQuery");
    if ((error = dlerror()) != NULL)  {
        fputs(error, stderr);
        exit(1);
    }
    return hh(stream);
    dlclose(handle);
}
