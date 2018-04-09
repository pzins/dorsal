

def correlation_cbid():
    driver_dic = {}
    runtime_dic = {}

    with open("/usr/local/cuda-9.0/extras/CUPTI/include/cupti_driver_cbid.h") as f:
        lines = f.readlines()
        for l in lines:
            if "CUPTI_DRIVER_TRACE_CBID" in l:
                tmp = l.split("=")
                fct = tmp[0].strip()[24:]
                id = tmp[1].strip()[:-1]
                driver_dic[id] = fct

    with open("/usr/local/cuda-9.0/extras/CUPTI/include/cupti_runtime_cbid.h") as f:
        lines = f.readlines()
        for l in lines:
            if "CUPTI_RUNTIME_TRACE_CBID" in l:
                tmp = l.split("=")
                fct = tmp[0].strip()[25:]
                id = tmp[1].strip()[:-1]
                runtime_dic[id] = fct
    return driver_dic, runtime_dic
