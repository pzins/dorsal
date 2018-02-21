# check if two output of RCP collecting the performance counters are equal (just the name and order of the kernel)
# just skip the first lines coresponding to the index or delete them manually in the csv files

out1, out2 = [], []
with open("kernels_1.csv", "r") as f:
    lines = f.readlines()
    for l in lines:
        out1.append(l.split("gfx803")[0])
        
with open("kernels_3.csv", "r") as f:
    lines = f.readlines()
    for l in lines:
        out2.append(l.split("gfx803")[0])


print(len(out1), len(out2))
for i in range(len(out1)):
    print(out1[i] == out2[i])
    print(out1[i])
    # input()
    if out1[i] != out2[i]:
        print("not success")
        exit(-1)