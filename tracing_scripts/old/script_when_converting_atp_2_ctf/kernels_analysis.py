import sys


prefix = "/home/pierre/"

if len(sys.argv) > 1:
    atp_filename = prefix + sys.argv[1]
else:
    atp_filename = prefix + "apitrace.atp"

# helper classes
class Kernel():
    def __init__(self, name, handle, start, end, agentName, agentHandle, index, queueHandle):
        self.name = name
        self.handle = handle
        self.start = start
        self.end = end
        self.agentName = agentName
        self.agentHandle = agentHandle
        self.index = index
        self.queueHandle = queueHandle

    def __str__(self):
        return self.name + " " + self.start + " " + self.end + " " + self.index
    def output(self):
        return self.name + " " + self.handle + " " + self.start + " " + self.end + " " + self.agentName + " " + self.agentHandle + " " + self.index + " " + self.queueHandle + "\n"

class HIPMarker():

    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp

    def __str__(self):
        return self.name + " " + self.timestamp

# datastructures
# list which contain the kernels and the hip api call corresponding to the kernel
HIP = []
KERNELS = []


nb_read = -2
begin_kernel_section = 0

 # read apittrace.atp and save lines with hipLaunchKernel in HIP and lines corresponding to kernel time execution into KERNELS
 # so we can map kernel execution to launch command (assuming kernels are executed in order)
 # kernels are in the kernel section
 # and hip api calls are in the perfmarker section 
with open(atp_filename, "r", encoding="ISO-8859-1") as f:
    lines = f.readlines()

    idx = 0
    
    # go to the kernel section
    while "hsa Kernel Timestamp Output" not in lines[idx]:
        idx += 1
        if idx == len(lines):
            print("No kernel section")
            exit(-1)
    
    # reach kernel section name line
    idx += 1
    # get number of kernels and pass this line
    number_kernel = int(lines[idx])
    idx += 1
    
    # save kernel line section start, for deletion after
    begin_kernel_section = idx 
    for i in range(number_kernel):
        tmp = lines[idx].strip().split()
        KERNELS.append(Kernel(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7]))
        idx += 1
    
    # reach perfmarkers section name line and pass it
    idx += 1
    
    while idx < len(lines):
        # if perfmarker hipLaunchKernel or hipMemset => save it because it match with a kernel execution
        if "hipLaunchKernel" in lines[idx] or "hipMemset" in lines[idx]:
            tmp = lines[idx].strip().split()
            HIP.append(HIPMarker(tmp[1], tmp[2]))
        idx += 1
    
print(len(HIP))
print(len(KERNELS))

# sort
KERNELS.sort(key=lambda x: x.start, reverse=False)
HIP.sort(key=lambda x: x.timestamp, reverse=False)

# for i in range(len(KERNELS)):
#     if "Memset" in HIP[i].name:
#         print(HIP[i].name, KERNELS[i])
#         input()

# check order
old = 0
for i in KERNELS:
    if old > int(i.start):
        print("KERNELS: OUT OF ORDER !!!")
    old = int(i.start)
old = 0
for i in HIP:
    if old > int(i.timestamp):
        print("HIP: OUT OF ORDER !!!")
    old = int(i.timestamp)


print(len(HIP))
print(len(KERNELS))

# change the long awful name with the name of the correponding hipLaunchKernel
for i in range(len(HIP)):
    KERNELS[i].name = HIP[i].name

# kernel time should be at the same place and cannot be at the end
# so delete old kernel time lines
for i in range(number_kernel):
    del lines[begin_kernel_section]

# save the first part (all before kernel time)
first_part = lines[:begin_kernel_section]

# append the new kernel time section
for j in KERNELS:
    first_part.append(j.output())

# append the last missing part (perf markers)
first_part.extend(lines[begin_kernel_section:])

# write in a new file
open(atp_filename[:-4] + "_new.atp", 'w').writelines(first_part)
