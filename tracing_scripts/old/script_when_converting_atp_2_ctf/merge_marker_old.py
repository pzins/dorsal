import sys



path = "/home/pierre/"

with open(path + "apitrace.atp", "r") as f:
    first_line = ""
    while "hsa API Trace Output" not in first_line:
        first_line = f.readline()
    tid = f.readline()

with open(path + "apitrace.atp", "a") as f:
    f.write("=====Perfmarker Output=====\n")
    f.write(tid)
    f.write("200000\n")

    for i in sys.argv[1:]:
        with open(i, "r") as ff:
            for line in ff:
                #if not "hipLaunchKernel" in line:# and not "Synchronize" in line:
                f.write(line)

    # for i in sys.argv[1:]:
    #     with open(i, "r") as ff:
    #         for line in ff:
    #             if "HIP" in line or not "TF_kernel" in line:
    #                 f.write(line)

    # for i in sys.argv[1:]:
    #     with open(i, "r") as ff:
    #         for line in ff:
    #             if "TF_kernel" in line:
    #                 f.write(line)

    # for i in sys.argv[1:]:
    #     with open(i, "r") as ff:
    #         for line in ff:
    #             if "TF_kernel_async" in line:
    #                 f.write(line)
