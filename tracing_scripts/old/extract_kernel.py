# extrace kernels timestamp from the file generated by hcc if HCC_PROFILE = 2
# write the result in another file 
# can juste copy paste to replace original kernel section in atp file

def add_kernel(line):
    tmp = line.split(";")
    name = tmp[1].strip().replace(" ", "_")
    begin = tmp[3].strip()
    end = tmp[4].strip()
    kernels.append(name + " 0x904B5C000 " + begin + " " + end + " gfx803 " + "{140535589261488} 3 0 \n")

kernels = []

with open("out", "r") as f:
    lines = f.readlines()
    for line in lines:
        if "profile:  kernel;" in line:
            add_kernel(line)

with open("kernels_hc", "w") as f:
    for i in kernels:
        f.write(i)
    print(len(kernels))